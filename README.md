# WoW Arena Boosting & Coaching Lead System

This application scans Reddit and Discord for players seeking arena rating pushes or coaching, qualifies the leads based on score thresholds, deduplicates them, and aggregates them into a Streamlit dashboard.

## Tech Stack
- **Framework**: CrewAI (for multi-agent research & copy Generation)
- **UI**: Streamlit
- **Platforms**: Reddit API (PRAW), Discord API (discord.py)
- **LLM**: Gemini (default priority), Grok (xAI), or OpenAI

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in the values:
   ```bash
   cp .env.example .env
   ```
   To use Gemini, define your API key:
   ```env
   GEMINI_API_KEY=your-gemini-key
   ```

3. **Run the Scraping Crew**:
   ```bash
   python -m src.wow_boosting_leads.main
   ```

4. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

5. **Run Scheduler**:
   ```bash
   python scheduler.py
   ```

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

