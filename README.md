# Trip Tracker

Welcome to **Trip Tracker**, a simple and fun app for logging your travel adventures and keeping your trip details organized in one place. It is made for beginners who want to learn how a small Python app can turn travel ideas into tracked memories.

## 🚀 Purpose of the App
This app helps you keep track of trips, destinations, dates, and notes in a friendly, easy-to-use interface. It is designed to show how a web app can connect your inputs to a backend storage system, all without needing complicated code.

## 📝 Background Story
I built Trip Tracker while doing a monthly budget plan. I realized that to keep my transport spending below budget, I had to limit my commute options to something like:
- 15x Ojol + LRT
- 4x Mikrotrans + LRT
- 3x Transjakarta bus

So I made this app to remind myself every day and log my commuting choices. Anyone can remake it and adjust it for their own needs, whether that means tracking trips, budgets, or daily routes.

## 🧠 How the App Works
- The app runs in your browser using **Streamlit**, so it feels like a mini website.
- You type in your trip info through the app's form fields.
- The app sends that information to a spreadsheet or storage backend using **gspread** and **google-auth**.
- Your trip is saved instantly, and you can keep adding new entries anytime.

> Think of it as a travel diary that lives on the web, powered by Python and a little spreadsheet magic.

## 📦 Requirements / Dependencies
To run Trip Tracker, you need:
- Python 3.12 or newer
- `streamlit`
- `gspread`
- `google-auth`

These packages are already listed in `pyproject.toml`, so the app is ready to install with standard Python tools.

## 🛠️ How to Remake the App
If you want to build this app again from scratch, follow these steps:

1. Clone this repo or create a new folder.
2. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install streamlit gspread google-auth
   ```
4. Get Google Sheets credentials if you want to save data to a sheet. See [Google Sheets setup instructions](GOOGLE_SHEETS_SETUP.md).
   - If you deploy on Streamlit Cloud, put your service account data or API keys in `.streamlit/secrets.toml` instead of hardcoding them.
5. Create a simple `main.py` that uses Streamlit for the UI and gspread for saving trip data.
6. Run the app:
   ```bash
   streamlit run main.py
   ```

## 🎉 Final Notes
This app is great for beginners because it combines a friendly interface with real Python packages. Once you understand the basics, you can expand it with new features like maps, photos, or shared trip lists.

Happy coding and happy travels! ✈️
