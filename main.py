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
    st.set_page_config(
        page_title="Trip Tracker",
        page_icon="🚍",
    )

    st.title("Trip Tracker")

    jakarta_tz = ZoneInfo("Asia/Jakarta")
    now_jakarta = datetime.now(tz=jakarta_tz)

    st.write(now_jakarta.strftime("%A, %d %B %Y %H:%M:%S %Z"))
    st.write("### How would you commute today?")

    sheet_id = st.secrets.get("sheet_id")
    write_sheet_name = st.secrets.get("sheet_name", "Sheet1")
    read_sheet_name = st.secrets.get("read_sheet_name", "Latest Transport")

    transport_option_display = st.radio(
        "**Choose a transportation option:**",
        ["**🛵 Ojol + 🚝 LRT**",
         "**🚙 Mikrotrans + 🚝 LRT**",
         "**🚍 Transjakarta Bus**",
         ],
        index=None,
    )
    transport_option = (
        transport_option_display.replace("*", "")
        if transport_option_display else None
    )

    submit_button = st.button(
        "Submit",
        disabled=transport_option is None,
    )

    if submit_button:
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

            # Count Ojol usage
            ojol_quota = 15
            ojol_label = "🛵 Ojol + 🚝 LRT"
            ojol_count = sum(
                1 for r in records if any(str(v).strip() == ojol_label for v in r.values())
            )
            ojol_remaining = max(0, ojol_quota - ojol_count)

            # Count LRT usage
            lrt_quota = 19
            lrt_label = "🚙 Mikrotrans + 🚝 LRT"
            lrt_count = ojol_count + sum(
                1 for r in records if any(str(v).strip() == lrt_label for v in r.values())
            )
            lrt_remaining = max(0, lrt_quota - lrt_count)

            # Ojol info box & warning box
            if ojol_count >= ojol_quota:
                st.warning(
                    f"**Ojol** quota is **fully used** for this month. Let's choose other transportation options!",
                    icon="🚨"
                )
            elif ojol_count >= 10:
                st.info(
                    f"You already used up {ojol_count} days of **Ojol** quota, you only have {ojol_remaining} day(s) left!",
                    icon="⚠️"
                )
            
            # LRT info box & warning box
            if lrt_count >= lrt_quota:
                st.warning(
                    f"**LRT** quota is **fully used** for this month. Let's hop on a Transjakarta Bus!",
                    icon="🚨"
                )
            elif lrt_count >= 17:
                st.info(
                    f"You already used up {lrt_count} days of **LRT** quota, you only have {lrt_remaining} day(s) left!",
                    icon="⚠️"
                )
            
            col_11, col_12 = st.columns(2, border=True)
            # Ojol metric card
            ojol_color = "red" if ojol_remaining <= 0 else "blue" if ojol_remaining <= 5 else "off"
            col_11.metric(
                "**Ojol usage**",
                f"{ojol_count}/{ojol_quota}",
                delta=f"{ojol_remaining} day(s) left",
                delta_arrow="off",
                delta_color=ojol_color,
            )

            # LRT metric card
            lrt_color = "red" if lrt_remaining <= 0 else "blue" if lrt_remaining <= 2 else "off"
            col_12.metric(
                "**LRT usage**",
                f"{lrt_count}/{lrt_quota}",
                delta=f"{lrt_remaining} day(s) left",
                delta_arrow="off",
                delta_color=lrt_color,
            )

            st.write("### Daily Transport Log")
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
