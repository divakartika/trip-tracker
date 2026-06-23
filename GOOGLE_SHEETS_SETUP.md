# Google Sheets Credentials and Streamlit Secrets

This guide explains how to get Google Sheets credentials for `gspread` and how to store them safely in Streamlit Cloud using `.streamlit/secrets.toml`.

## 1. Create a Google Cloud project

1. Open the Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or use an existing one.
3. Make sure billing is enabled if required for your project.

## 2. Enable the Google Sheets API

1. In the Cloud Console, go to `APIs & Services` > `Library`.
2. Search for `Google Sheets API`.
3. Click `Enable`.

## 3. Create service account credentials

1. Go to `APIs & Services` > `Credentials`.
2. Click `Create credentials` and choose `Service account`.
3. Fill in a name like `trip-tracker-service-account`.
4. Continue through the setup and finish without adding roles if you only need Sheets access.
5. After the service account is created, click it and go to the `Keys` tab.
6. Click `Add Key` > `Create new key` and choose `JSON`.
7. Download the JSON file and keep it safe.

## 4. Share your Google Sheet with the service account

1. Open the Google Sheet you want to use.
2. Click `Share`.
3. Add the service account email from the JSON file (it usually ends with `@<project>.iam.gserviceaccount.com`).
4. Give it `Editor` access so it can read and write rows.

## 5. Use the credentials in Streamlit Cloud

If you deploy to Streamlit Cloud, do not commit your JSON key into Git. Instead, store the key values in `.streamlit/secrets.toml`.

### Example `secrets.toml`

Create a folder called `.streamlit` and a file named `secrets.toml` inside it.

```toml
# .streamlit/secrets.toml

[google_sheets]
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "service-account-email@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/service-account-email%40your-project.iam.gserviceaccount.com"

sheet_id = "your-google-sheet-id"
```

> Tip: Replace line breaks in `private_key` with `\n` so the value stays valid in TOML.

## 6. Load secrets in `main.py`

In your Streamlit app, you can read the credentials like this:

```python
import json
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

secrets = st.secrets["google_sheets"]
credentials_dict = {
    "type": "service_account",
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"],
}

creds = Credentials.from_service_account_info(credentials_dict, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
])
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["google_sheets"]["sheet_id"])
```

## 7. Important security note

- Never commit your `service account` JSON file or `.streamlit/secrets.toml` to Git.
- Use `.gitignore` to exclude `.streamlit/secrets.toml`.

That’s it! Once your credentials are set up, the app can safely connect to Google Sheets without exposing secrets in your repository.