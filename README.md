# WoW Arena Boosting & Coaching Lead System

This application scans Reddit and Discord for players seeking arena rating pushes or coaching, qualifies the leads based on score thresholds, deduplicates them, and aggregates them into a Streamlit dashboard.

## Tech Stack
- **Framework**: CrewAI (for multi-agent research & copy Generation)
- **UI**: Streamlit
- **Platforms**: Reddit API (PRAW), Discord API (discord.py)
- **LLM**: Gemini (default priority), Grok (xAI), or OpenAI

## ⚙️ Step-by-Step Local Installation (Windows 11)

1. **Download and Extract Release**:
   Download the latest release ZIP bundle (`WoWBoost_Release.zip`) from GitHub and extract the folder to your preferred local drive path (e.g. `C:\WoWBoost`).

2. **Run the PowerShell Installer**:
   Open a PowerShell window, navigate to the extracted directory, and run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\install.ps1
   ```
   *This automatically builds your local Python virtual environment (`.venv`), installs all requirements, creates configuration templates, and writes Windows batch shortcuts.*

3. **Configure Environment Secrets**:
   Open the generated `.env` file and insert your API credentials:
   - `GEMINI_API_KEY`: Paste your Gemini API key (already pre-loaded for your default workspace).
   - `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`: Put your Reddit Developer script credentials.
   - `DISCORD_BOT_TOKEN`: Put your Discord Bot token.
   - `SMTP_EMAIL` / `SMTP_PASSWORD`: Configure your sender email and password (e.g., Gmail App Password) to enable the automated outreach email sender.

---

## 🖥️ Running & Accessing the Dashboard

1. Double-click the **`start_dashboard.bat`** file in the root folder.
2. It will activate the virtual environment and start Streamlit.
3. Your default browser will open automatically to the control panel at:
   👉 **`http://localhost:8501`**

---

## 🤖 Directing Agents to Find Coaching Clients

Once on the dashboard:
1. **Trigger Scan**: Click **`🔍 Run Agents Scan`** in the sidebar. The Gemini-powered agents will scrape PvP communities (Reddit & Discord) for active rating climb struggles.
2. **Review Scoring**: Filter leads using the **Min Lead Score** slider to review qualified, high-intent prospective clients.
3. **Outreach**: View the custom outreach draft created by Gemini (personalized with their spec, rating goals, and packages), copy it, and DM them.
4. **Track Status**: Click **`Mark Contacted`** to update status logs in `wow_leads.json`.
5. **Automated Email Outreach**: Enter a prospective client's email under **Client Email** in their detailed view (or fill it in during manual lead creation). Click **`📧 Email Top Leads (Top 5%)`** in the sidebar. The Gemini agent will compile a custom email pitch using their spec/rating context and send it automatically using your configured SMTP settings.

---

## 🏆 WoW Coaching Business Playbook (Self-Play Focused)

This lead system is designed to acquire and qualify clients for a **legitimate coaching and self-play improvement model** which carries substantially lower ToS risks compared to piloting/RMT boosting.

### 1. Value Proposition
Help stuck, mid-rating players (1400–1800 rating) climb to 1700–2200+ in Arena / Solo Shuffle through personalized live coaching, VOD reviews, and queue sessions—without account sharing.
*Core Promise: "Get better, keep your account safe, and learn skills you can use long-term."*

### 2. Service Tiers & Packages

| Tier/Package | Price | Description |
| :--- | :--- | :--- |
| **Free Teaser** | $0 | 1 short VOD review or quick Discord tip to initiate outreach |
| **Hourly Coaching** | $35–$55/hr | Live queue sessions (self-play) with real-time feedback |
| **Basic Package** | $150–$250 | 5–8 hours + VOD reviews (target 1700 rating) |
| **Pro Package** | $400–$600 | 12–15 hours + comprehensive comp guide (target 2000+ rating) |
| **Gladiator Pathway** | $800–$1,500 | Ongoing multi-session support with high-profile coaches |
| **Monthly Subscription** | $99–$199/mo | Private Discord access + 4–6 hours of live coaching monthly |

### 3. Execution & Mitigation Strategies
- **WoW ToS Compliance**: Emphasize self-play coaching. Avoid piloting (sharing account details) which triggers win-trading detection. For gold services, keep advertisements within designated services channels.
- **Client Conversion**: Use the Streamlit dashboard message draft to offer value first (e.g. a free VOD review of one game). Convert responsive players to paid packages.
- **Payments**: Use PayPal or Stripe and label invoices as "Educational Tutoring" or "Coaching Services".

