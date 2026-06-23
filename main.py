import json
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


def get_gsheet_client():
    creds_info = st.secrets.get("gcp_service_account")
    if creds_info is None:
        st.error(
            "Google Sheets credentials are not configured. Add `gcp_service_account` to Streamlit secrets."
        )
        return None

    if isinstance(creds_info, str):
        creds_info = json.loads(creds_info)

    credentials = Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return gspread.authorize(credentials)


def append_submission(sheet_id: str, sheet_name: str, row: list[str]) -> bool:
    client = get_gsheet_client()
    if client is None:
        return False

    try:
        spreadsheet = client.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_row(row, value_input_option="USER_ENTERED")
        return True
    except Exception as exc:
        st.error(f"Failed to write to Google Sheets: {exc}")
        return False


def read_sheet_records(sheet_id: str, sheet_name: str) -> list[dict[str, str]] | None:
    client = get_gsheet_client()
    if client is None:
        return None

    try:
        spreadsheet = client.open_by_key(sheet_id)
        sheet = spreadsheet.worksheet(sheet_name)
        return sheet.get_all_records()
    except Exception as exc:
        st.error(f"Failed to read from Google Sheets: {exc}")
        return None


def main():
    st.title("Trip Tracker")

    jakarta_tz = ZoneInfo("Asia/Jakarta")
    now_jakarta = datetime.now(tz=jakarta_tz)

    st.write(now_jakarta.strftime("%A, %d %B %Y %H:%M:%S %Z"))
    st.write("### Which transportation option would you use today?")

    transport_option_display = st.radio(
        "**Choose a transportation option:**",
        ["**🛵 Ojol + 🚝 LRT**", 
         "**🚙 Mikrotrans + 🚝 LRT**", 
         "**🚍 Transjakarta Bus**"],
    )
    transport_option = transport_option_display.replace("*", "")

    sheet_id = st.secrets.get("sheet_id")
    write_sheet_name = st.secrets.get("sheet_name", "Sheet1")
    read_sheet_name = st.secrets.get("read_sheet_name", "Latest Transport")

    if st.button("Submit"):
        submitted_time = datetime.now(tz=jakarta_tz).strftime("%Y-%m-%d %H:%M:%S")
        if sheet_id:
            success = append_submission(sheet_id, write_sheet_name, [submitted_time, transport_option])
            if success:
                st.success("Submission recorded to Google Sheets.")
        else:
            st.error(
                "Missing `sheet_id` in Streamlit secrets. Please add `sheet_id` and `gcp_service_account`."
            )

    if sheet_id:
        records = read_sheet_records(sheet_id, read_sheet_name)
        if records is not None:

            # Count Ojol + LRT usage in the read sheet and show quota info
            ojol_label = "🛵 Ojol + 🚝 LRT"
            ojol_count = sum(
                1 for r in records if any(str(v).strip() == ojol_label for v in r.values())
            )
            remaining = max(0, 15 - ojol_count)
            if ojol_count >= 15:
                st.warning(
                    f"You already used up all of your Ojol quota, please choose other transportation options for the rest of the month"
                )
            elif ojol_count >= 10:
                st.info(
                    f"You already used up {ojol_count} days of Ojol quota, you only have {remaining} days left"
                )
            st.write("### Daily Transportation")
            st.table(records)
    else:
        st.error(
            "Missing `sheet_id` in Streamlit secrets. Please add `sheet_id` and `gcp_service_account`."
        )

    # st.write(
    #     "---\nTo persist submissions in Streamlit Cloud, set `sheet_id` and `gcp_service_account` in your Streamlit secrets."
    # )


if __name__ == "__main__":
    main()
