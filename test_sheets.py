import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("config/credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
client = gspread.authorize(creds)

# Try to open the spreadsheet
sheet = client.open_by_key("1ibKIvKfKhavnNKTEAHIpZBiuweKhmMFsshaFtC38ALQ")
print("✅ Access successful!")
