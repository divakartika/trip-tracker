# trip-tracker
Simple tracker to track daily transportation option

## Google Sheets persistence
This app writes each submission to a Google Sheet so the data is stored persistently when deployed to Streamlit Cloud.

### Setup
1. Create a Google Cloud project.
2. Enable the Google Sheets API.
3. Create a service account and download the JSON key.
4. Share your Google Sheet with the service account email.
5. Copy the spreadsheet ID from the sheet URL:
   `https://docs.google.com/spreadsheets/d/<sheet_id>/edit`

### Streamlit Cloud secrets
Add the following secrets in Streamlit Cloud:

```toml
sheet_id = "<your-sheet-id>"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

In the app, `sheet_id` and `gcp_service_account` must be available in `st.secrets`.

### Local development
For local development, you can also create a `.streamlit/secrets.toml` file with the same values, but keep credentials private and never commit them to version control.

### Notes
- The app appends rows to the first worksheet (`sheet1`).
- Submissions shown in the app are session-local, but the Google Sheet stores data persistently.
