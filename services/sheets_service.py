import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import json

SPREADSHEET_ID = "1ibKIvKfKhavnNKTEAHIpZBiuweKhmMFsshaFtC38ALQ"

def update_google_sheet(df: pd.DataFrame):
    """
    Updates existing Google Sheet with main + filtered tabs.
    """
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        # Load credentials securely from Streamlit Secrets
        creds_dict = json.loads(st.secrets["service_account_json"])

# Create Credentials object from the dictionary
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)

        # Open existing spreadsheet
        sheet = client.open_by_key(SPREADSHEET_ID)

        # Update main sheet (Sheet1)
        main_ws = sheet.sheet1
        main_ws.clear()
        main_ws.update([df.columns.values.tolist()] + df.values.tolist())

        # Update filtered tabs
        def update_tab(title, grouped_df):
            try:
                try:
                    ws = sheet.worksheet(title)
                    ws.clear()
                except gspread.WorksheetNotFound:
                    ws = sheet.add_worksheet(title=title, rows=str(len(grouped_df)+10), cols=str(len(grouped_df.columns)))
                ws.update([grouped_df.columns.values.tolist()] + grouped_df.values.tolist())
            except Exception as e:
                st.error(f"Failed to update tab {title}: {e}")

        # By Pincode
        update_tab("By Pincode", df.groupby("Pincode").apply(lambda x: x).reset_index(drop=True))
        # By Driver
        update_tab("By Driver", df.groupby("Driver").apply(lambda x: x).reset_index(drop=True))
        # By Vehicle
        update_tab("By Vehicle", df.groupby("Vehicle").apply(lambda x: x).reset_index(drop=True))

        return sheet.url

    except gspread.exceptions.APIError as e:
        st.error("⚠️ API Error: Could not update Google Sheet. Check API and permissions.")
        st.error(e)
    except Exception as e:
        st.error("⚠️ Unexpected Error:")
        st.error(e)
