import pandas as pd
import json

def assign_deliveries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assign deliveries to drivers (max 35 per driver)
    """
    with open("data/drivers.json") as f:
        drivers = json.load(f)

    assigned_data = []
    driver_index = 0
    deliveries_per_driver = 35

    for _, group in df.groupby("Pincode"):
        for i in range(0, len(group), deliveries_per_driver):
            driver = drivers[driver_index % len(drivers)]
            batch = group.iloc[i:i + deliveries_per_driver].copy()
            batch["Driver"] = driver["name"]
            batch["Vehicle"] = driver["vehicle"]
            assigned_data.append(batch)
            driver_index += 1

    return pd.concat(assigned_data).reset_index(drop=True)
