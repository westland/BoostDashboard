# WoW Arena Boosting & Coaching Lead System - User Guide

This guide details the setup, configuration, running, and Git repository sync instructions for the WoW Arena Boosting and Coaching Lead System on Windows 11.

---

## 🛠️ Prerequisites

1. **Python 3.10+**: Ensure Python is installed and added to your Windows PATH.
2. **Git**: Installed and authenticated with your GitHub account.

---

## 🚀 Installation on Windows 11

We have provided a automated installer script `install.ps1` that sets up a Python virtual environment, installs dependencies, checks files, and creates quick-launch batch files.

### Steps:
1. Open **PowerShell** (or Terminal) and navigate to the project directory:
   ```powershell
   cd C:\Users\westl\.gemini\antigravity\scratch\wow_boosting_leads
   ```
2. Enable script execution for this process (if prompt appears):
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```
3. Run the installer:
   ```powershell
   .\install.ps1
   ```

This will generate three launch scripts in the root directory:
- `start_dashboard.bat` — Launches the Streamlit UI.
- `run_scraper.bat` — Starts a one-off scan.
- `start_scheduler.bat` — Runs a background scheduler checking daily at 09:00.

---

## ⚙️ Configuration (`.env`)

Configure your keys in the `.env` file at the root folder:

### 1. LLM API Key (Brains of the Crew)
Your active Gemini API key is already configured:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Reddit API Setup
To scrape Reddit (e.g. `r/worldofpvp`, `r/wow`):
1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps).
2. Click **Create another app...** (select **script** type).
3. Set Name to `WoWLeadAgent` and Redirect URI to `http://localhost:8080`.
4. Copy the Client ID (under the app name) and Secret.
5. Populate in `.env`:
   ```env
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   ```

### 3. Discord Bot Setup
To scrape Discord message history:
1. Go to [Discord Developer Portal](https://discord.com/developers/applications) and create an Application.
2. Under the **Bot** tab, generate a token and enable **Message Content Intent**.
3. Under **OAuth2 -> URL Generator**, select `bot` scope with `Read Message History` permission, then invite it to your target servers.
4. Populate in `.env`:
   ```env
   DISCORD_BOT_TOKEN=your_token
   ```

---

## 💻 Running the System

- **Streamlit Dashboard**: Double-click `start_dashboard.bat` (or run `streamlit run dashboard.py`).
  - View the collected leads list.
  - Filter by Score, Platform, and Contacted status.
  - Review and copy personalized outreach drafts.
  - Add or edit the **Client Email** field for any lead directly in their detail card.
  - Trigger **Gemini-personalized cold emails** to your top 5% highest-scoring leads by clicking **`📧 Email Top Leads (Top 5%)`** in the sidebar.
  - Mark leads as Contacted (persists directly in `wow_leads.json`).
  - Manually input leads with email addresses.
  
- **Lead Generation Scraper**: Double-click `run_scraper.bat` (or run `python -m src.wow_boosting_leads.main`).
  - Runs the CrewAI agents to scour Reddit/Discord, filter target leads, generate messages, and write them to the registry.

- **Background Scheduler**: Double-click `start_scheduler.bat` (or run `python scheduler.py`).
  - Keeps a lightweight scheduler open in the terminal, triggering the scraper automatically every morning at 09:00.

---

## 📂 Push to GitHub (`BoostDashboard` Repository)

We have provided a automated Git initializer script: `setup_git.ps1`.

### To initialize and push:
1. Ensure you have created the empty repository `BoostDashboard` on your GitHub account (`github.com/westland`).
2. Run the PowerShell script:
   ```powershell
   .\setup_git.ps1
   ```
   *Note: This script adds a `.gitignore` to prevent uploading your `.env` containing keys or `.venv` virtual environments.*
