import os
import sys
import streamlit as st
import pandas as pd
from datetime import datetime

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from src.wow_boosting_leads.tools.lead_utils import load_existing_leads, save_leads
except ImportError:
    try:
        from tools.lead_utils import load_existing_leads, save_leads
    except ImportError:
        # Direct local fallback
        from src.wow_boosting_leads.tools.lead_utils import load_existing_leads, save_leads

def generate_email_with_llm(lead: dict) -> str:
    try:
        from src.wow_boosting_leads.crew import get_llm, HAS_CREW_LLM
        llm = get_llm()
    except Exception:
        llm = None
        HAS_CREW_LLM = False
        
    fallback_text = (
        f"Subject: Help climbing WoW PvP rating!\n\n"
        f"Hey {lead.get('username')},\n\n"
        f"I saw you are struggling as a {lead.get('class', 'WoW Player')} at {lead.get('current_rating', 'low')} rating due to {lead.get('pain_points', 'bad randoms')}.\n\n"
        f"I offer personalized coaching and self-play sessions to help you reach {lead.get('desired_rating', 'your goal')} safely and learn strategies you can keep. "
        f"Let me know if you would be open to a quick, free 15-minute VOD review/consultation!\n\n"
        f"Best regards,\nWoW Coaching Team"
    )
    
    if not llm:
        return fallback_text
        
    prompt = (
        f"You are a professional World of Warcraft PvP Arena Coach.\n"
        f"Generate a personalized, highly appealing marketing email to a potential client.\n"
        f"Details about the client:\n"
        f"- Username: {lead.get('username')}\n"
        f"- Current Rating: {lead.get('current_rating', 'N/A')}\n"
        f"- Desired Rating / Goal: {lead.get('desired_rating', 'N/A')}\n"
        f"- Class / Spec: {lead.get('class', 'N/A')}\n"
        f"- Pain Points: {lead.get('pain_points', 'N/A')}\n\n"
        f"Write a friendly, value-first, non-spammy marketing email. Reference their specific spec/pain points. "
        f"Offer a free 15-minute coaching consultation/VOD review first, then introduce your services (self-play coaching). "
        f"Format the output strictly as:\n"
        f"Subject: <Subject Line>\n\n"
        f"<Body Line 1>\n"
        f"<Body Line 2>\n..."
    )
    
    try:
        if HAS_CREW_LLM:
            if hasattr(llm, "call"):
                response = llm.call([{"role": "user", "content": prompt}])
                return response
            elif hasattr(llm, "invoke"):
                response = llm.invoke(prompt)
                if hasattr(response, "content"):
                    return response.content
                return str(response)
        else:
            response = llm.invoke(prompt)
            if hasattr(response, "content"):
                return response.content
            return str(response)
    except Exception as e:
        print(f"Error during LLM generate: {e}")
        return fallback_text

def load_env_keys() -> dict:
    env_path = os.path.join(PROJECT_ROOT, ".env")
    keys = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    parts = line.split("=", 1)
                    k = parts[0].strip()
                    v = parts[1].strip()
                    if v.startswith(('"', "'")) and v.endswith(('"', "'")):
                        v = v[1:-1]
                    keys[k] = v
    return keys

def save_env_keys(updated_keys: dict):
    env_path = os.path.join(PROJECT_ROOT, ".env")
    existing_lines = []
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()
            
    processed_keys = set()
    new_lines = []
    
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in line:
            parts = line.split("=", 1)
            k = parts[0].strip()
            if k in updated_keys:
                new_lines.append(f"{k}={updated_keys[k]}\n")
                processed_keys.add(k)
                continue
        new_lines.append(line)
        
    for k, v in updated_keys.items():
        if k not in processed_keys:
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines[-1] = new_lines[-1] + "\n"
            new_lines.append(f"{k}={v}\n")
            
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# Page configuration for a premium dashboard layout
st.set_page_config(
    page_title="WoW PvP Leads Control Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styling for a premium dark mode with neon accents
st.markdown("""
<style>
    /* Styling headers and custom premium look */
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .lead-card {
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.375rem;
        margin-right: 0.5rem;
    }
    .badge-reddit {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .badge-discord {
        background-color: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .badge-other {
        background-color: rgba(107, 114, 128, 0.2);
        color: #9ca3af;
        border: 1px solid rgba(107, 114, 128, 0.3);
    }
    .badge-score {
        background-color: rgba(234, 179, 8, 0.2);
        color: #facc15;
        border: 1px solid rgba(234, 179, 8, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for view mode
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "leads"

# Navigation at the top of the page
col_title, col_nav = st.columns([3, 1])
with col_title:
    st.markdown('<div class="main-title">🚀 WoW PvP Lead Control Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Intelligent lead generation & qualification hub for WoW Arena Coaching & Self-Play</div>', unsafe_allow_html=True)
with col_nav:
    st.write("") # Spacer
    st.write("") # Spacer
    if st.session_state.view_mode == "leads":
        if st.button("⚙️ Manage API Keys & Settings", use_container_width=True):
            st.session_state.view_mode = "settings"
            st.rerun()
    else:
        if st.button("📋 Back to Lead Registry", use_container_width=True):
            st.session_state.view_mode = "leads"
            st.rerun()

# If view_mode is settings, render the settings page and stop
if st.session_state.view_mode == "settings":
    st.subheader("⚙️ Configure API Keys & Environment Variables")
    st.markdown("Use this form to securely update the environment variables in your `.env` file. Existing values are hidden for security.")
    
    current_env = load_env_keys()
    
    with st.form("env_config_form"):
        col_env1, col_env2 = st.columns(2)
        
        updated_env = {}
        has_updates = False
        
        with col_env1:
            st.markdown("#### 🤖 LLM & Scraping APIs")
            
            # Gemini Key
            has_gemini = "GEMINI_API_KEY" in current_env and current_env["GEMINI_API_KEY"]
            gemini_placeholder = "Configured (Hidden) - Enter new key to override" if has_gemini else "Enter Gemini API Key"
            gemini_val = st.text_input("Google Gemini API Key", type="password", placeholder=gemini_placeholder)
            if gemini_val:
                updated_env["GEMINI_API_KEY"] = gemini_val
                has_updates = True
                
            # Reddit Client ID
            has_reddit_id = "REDDIT_CLIENT_ID" in current_env and current_env["REDDIT_CLIENT_ID"]
            reddit_id_placeholder = "Configured (Hidden) - Enter new ID to override" if has_reddit_id else "Enter Reddit Client ID"
            reddit_id_val = st.text_input("Reddit Client ID", type="password", placeholder=reddit_id_placeholder)
            if reddit_id_val:
                updated_env["REDDIT_CLIENT_ID"] = reddit_id_val
                has_updates = True
                
            # Reddit Client Secret
            has_reddit_secret = "REDDIT_CLIENT_SECRET" in current_env and current_env["REDDIT_CLIENT_SECRET"]
            reddit_secret_placeholder = "Configured (Hidden) - Enter new Secret to override" if has_reddit_secret else "Enter Reddit Client Secret"
            reddit_secret_val = st.text_input("Reddit Client Secret", type="password", placeholder=reddit_secret_placeholder)
            if reddit_secret_val:
                updated_env["REDDIT_CLIENT_SECRET"] = reddit_secret_val
                has_updates = True
                
            # Reddit User Agent
            has_reddit_ua = "REDDIT_USER_AGENT" in current_env and current_env["REDDIT_USER_AGENT"]
            reddit_ua_placeholder = current_env.get("REDDIT_USER_AGENT", "WoWLeadAgent/1.0 (by /u/YourRedditUsername)")
            reddit_ua_val = st.text_input("Reddit User Agent", value=reddit_ua_placeholder if not has_reddit_ua else "", placeholder="Enter User Agent (or leave blank to keep configured)")
            if reddit_ua_val:
                updated_env["REDDIT_USER_AGENT"] = reddit_ua_val
                has_updates = True
                
            # Discord Bot Token
            has_discord = "DISCORD_BOT_TOKEN" in current_env and current_env["DISCORD_BOT_TOKEN"]
            discord_placeholder = "Configured (Hidden) - Enter new token to override" if has_discord else "Enter Discord Bot Token"
            discord_val = st.text_input("Discord Bot Token", type="password", placeholder=discord_placeholder)
            if discord_val:
                updated_env["DISCORD_BOT_TOKEN"] = discord_val
                has_updates = True
                
        with col_env2:
            st.markdown("#### 📧 SMTP Email Outreach Settings")
            
            # SMTP Email
            has_smtp_email = "SMTP_EMAIL" in current_env and current_env["SMTP_EMAIL"]
            smtp_email_placeholder = current_env.get("SMTP_EMAIL", "your_smtp_email@gmail.com")
            smtp_email_val = st.text_input("SMTP Email address", value=smtp_email_placeholder if not has_smtp_email else "", placeholder="Enter Sender Email (or leave blank to keep configured)")
            if smtp_email_val:
                updated_env["SMTP_EMAIL"] = smtp_email_val
                has_updates = True
                
            # SMTP Password
            has_smtp_pass = "SMTP_PASSWORD" in current_env and current_env["SMTP_PASSWORD"]
            smtp_pass_placeholder = "Configured (Hidden) - Enter new password to override" if has_smtp_pass else "Enter SMTP Password"
            smtp_pass_val = st.text_input("SMTP Password / App Password", type="password", placeholder=smtp_pass_placeholder)
            if smtp_pass_val:
                updated_env["SMTP_PASSWORD"] = smtp_pass_val
                has_updates = True
                
            # SMTP Server
            has_smtp_server = "SMTP_SERVER" in current_env and current_env["SMTP_SERVER"]
            smtp_server_placeholder = current_env.get("SMTP_SERVER", "smtp.gmail.com")
            smtp_server_val = st.text_input("SMTP Server", value=smtp_server_placeholder if not has_smtp_server else "", placeholder="Enter SMTP Server (or leave blank to keep configured)")
            if smtp_server_val:
                updated_env["SMTP_SERVER"] = smtp_server_val
                has_updates = True
                
            # SMTP Port
            has_smtp_port = "SMTP_PORT" in current_env and current_env["SMTP_PORT"]
            smtp_port_placeholder = current_env.get("SMTP_PORT", "587")
            smtp_port_val = st.text_input("SMTP Port", value=smtp_port_placeholder if not has_smtp_port else "", placeholder="Enter SMTP Port (or leave blank to keep configured)")
            if smtp_port_val:
                updated_env["SMTP_PORT"] = smtp_port_val
                has_updates = True

        submitted_env = st.form_submit_button("💾 Save Environment Configurations")
        if submitted_env:
            if has_updates:
                save_env_keys(updated_env)
                st.success("Successfully updated configurations in `.env` file!")
                st.rerun()
            else:
                st.info("No modifications made to save.")
    
    st.stop()

leads = load_existing_leads()

# ----------------- SIDEBAR FILTERS & STATS -----------------
st.sidebar.header("📊 Controls & Settings")

if leads:
    df_temp = pd.DataFrame(leads)
    total_leads = len(df_temp)
    contacted_count = df_temp.get("contacted", pd.Series([False]*total_leads)).sum()
    pending_count = total_leads - contacted_count
else:
    total_leads, contacted_count, pending_count = 0, 0, 0

st.sidebar.markdown(f"""
- **Total Leads Collected**: `{total_leads}`
- **Pending Outreach**: `{pending_count}`
- **Contacted Clients**: `{contacted_count}`
""")

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Agent Actions")

if st.sidebar.button("🔍 Run Agents Scan", help="Instruct the Gemini CrewAI agents to scan Reddit and Discord for coaching leads"):
    with st.spinner("Gemini agents are scouring Reddit and Discord... this may take 1-2 minutes."):
        try:
            # Import dynamically to avoid loading latency on startup
            from src.wow_boosting_leads.main import run as run_crew
            run_crew()
            st.sidebar.success("Scan complete! Leads list updated.")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Scan failed: {e}")

if st.sidebar.button("📧 Email Top Leads (Top 5%)", help="Send Gemini-customized emails to the top 5% leads by score"):
    if not leads:
        st.sidebar.info("No leads available to email. Run the scan first!")
    else:
        with st.spinner("Generating and sending emails to top leads..."):
            try:
                from send_email import send_personalized_email
                
                # Sort leads by score descending
                sorted_leads = sorted(leads, key=lambda x: x.get("lead_score", 0), reverse=True)
                top_count = max(1, int(len(sorted_leads) * 0.05))
                top_leads = sorted_leads[:top_count]
                
                sent_count = 0
                skipped_leads = []
                
                for lead in top_leads:
                    to_email = lead.get("email")
                    if not to_email:
                        skipped_leads.append(lead.get("username"))
                        continue
                    
                    email_text = generate_email_with_llm(lead)
                    
                    subject = "Help climbing WoW PvP rating!"
                    body = email_text
                    if "Subject:" in email_text:
                        parts = email_text.split("\n\n", 1)
                        sub_line = parts[0]
                        subject = sub_line.replace("Subject:", "").strip()
                        if len(parts) > 1:
                            body = parts[1]
                    
                    success = send_personalized_email(to_email, subject, body)
                    if success:
                        # Update lead in local leads list to contacted
                        target_user = lead.get("username")
                        target_url = lead.get("url") or lead.get("jump_url")
                        for main_lead in leads:
                            lead_url = main_lead.get("url") or main_lead.get("jump_url")
                            if main_lead.get("username") == target_user and lead_url == target_url:
                                main_lead["contacted"] = True
                                break
                        sent_count += 1
                
                save_leads(leads)
                
                if sent_count > 0:
                    st.sidebar.success(f"Sent {sent_count} email(s) successfully!")
                if skipped_leads:
                    st.sidebar.warning(f"No email addresses set for top leads: {', '.join(skipped_leads)}")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Email process failed: {e}")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

min_score = st.sidebar.slider("Min Lead Score", min_value=1, max_value=10, value=6)

platforms = ["All"]
if total_leads > 0 and "platform" in df_temp.columns:
    platforms += sorted(df_temp["platform"].dropna().unique().tolist())
selected_platform = st.sidebar.selectbox("Platform Filter", platforms)

contact_status = st.sidebar.radio(
    "Contact Status",
    ["Pending Only", "Contacted Only", "All Leads"]
)

st.sidebar.markdown("---")

# ----------------- ADD MANUAL LEAD FORM -----------------
with st.sidebar.expander("➕ Add Manual Lead", expanded=False):
    with st.form("manual_lead_form", clear_on_submit=True):
        username = st.text_input("Username / Author *")
        platform = st.selectbox("Platform", ["Reddit", "Discord", "Other"])
        url = st.text_input("Post / Message URL")
        email = st.text_input("Email Address (optional)")
        current_rating = st.text_input("Current Rating (e.g., 1450)")
        desired_rating = st.text_input("Desired Rating (e.g., 1800)")
        class_spec = st.text_input("Class / Spec (e.g., Ret Paladin)")
        pain_points = st.text_area("Pain Points")
        personalized_message = st.text_area("Outreach Draft (optional)")
        score = st.slider("Lead Quality Score", 1, 10, 7)
        
        submitted = st.form_submit_button("Add Lead")
        if submitted:
            if not username:
                st.error("Username is required!")
            else:
                new_lead = {
                    "timestamp": datetime.now().isoformat(),
                    "username": username,
                    "platform": platform,
                    "url": url,
                    "email": email,
                    "current_rating": current_rating,
                    "desired_rating": desired_rating,
                    "class": class_spec,
                    "pain_points": pain_points,
                    "personalized_message": personalized_message or f"Hey {username}, saw you looking for rating tips...",
                    "lead_score": score,
                    "contacted": False
                }
                leads.append(new_lead)
                save_leads(leads)
                st.success("Lead added successfully!")
                st.rerun()

# ----------------- MAIN DISPLAY AREA -----------------
if not leads:
    st.info("No leads found in `wow_leads.json`. Execute the scraping crew to fetch leads, or add one manually in the sidebar!")
else:
    df = pd.DataFrame(leads)
    
    # Ensure contacted column exists
    if "contacted" not in df.columns:
        df["contacted"] = False
        
    # Apply filters
    filtered_df = df[df["lead_score"] >= min_score]
    
    if selected_platform != "All":
        filtered_df = filtered_df[filtered_df["platform"] == selected_platform]
        
    if contact_status == "Pending Only":
        filtered_df = filtered_df[filtered_df["contacted"] == False]
    elif contact_status == "Contacted Only":
        filtered_df = filtered_df[filtered_df["contacted"] == True]

    if filtered_df.empty:
        st.warning("No leads match the selected filter criteria.")
    else:
        # Display Overview Table
        st.subheader("📋 Lead Registry Summary")
        display_df = filtered_df.copy()
        
        # Clean columns for display table
        cols_to_show = ["timestamp", "username", "platform", "lead_score", "current_rating", "desired_rating", "class", "contacted"]
        cols_available = [c for c in cols_to_show if c in display_df.columns]
        
        st.dataframe(
            display_df[cols_available].sort_values(by="lead_score", ascending=False),
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("🔍 Detailed Outreach Review")

        for idx, row in filtered_df.iterrows():
            platform_str = str(row.get('platform', 'Other'))
            badge_class = f"badge-{platform_str.lower()}"
            
            # Create a card view for each lead
            with st.container():
                st.markdown(f"""
                <div class="lead-card">
                    <h4>
                        <span class="badge {badge_class}">{platform_str}</span>
                        <span class="badge badge-score">Score: {row.get('lead_score', 'N/A')}/10</span>
                        User: {row.get('username')}
                    </h4>
                    <p style="font-size:0.9rem; color:#64748b;">Collected: {row.get('timestamp', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_left, col_right = st.columns([1, 2])
                
                with col_left:
                    st.write(f"**Current Rating:** `{row.get('current_rating') or 'N/A'}`")
                    st.write(f"**Target Rating:** `{row.get('desired_rating') or 'N/A'}`")
                    st.write(f"**Class / Spec:** `{row.get('class') or 'N/A'}`")
                    st.write(f"**Target URL:** [Open Link]({row.get('url') or row.get('jump_url') or '#'})")
                    st.write(f"**Pain Points:** {row.get('pain_points') or 'None mentioned'}")
                    
                    # Email editing field
                    email_val = st.text_input("📧 Client Email", value=row.get("email", ""), key=f"email_{idx}")
                    if email_val != row.get("email", ""):
                        target_user = row.get("username")
                        target_url = row.get("url") or row.get("jump_url")
                        for lead in leads:
                            lead_url = lead.get("url") or lead.get("jump_url")
                            if lead.get("username") == target_user and lead_url == target_url:
                                lead["email"] = email_val
                                break
                        save_leads(leads)
                        st.success(f"Updated email for {target_user}!")
                        st.rerun()
                    
                    # Persist contacted state back to database
                    is_contacted = bool(row.get("contacted", False))
                    button_label = "Mark Pending" if is_contacted else "Mark Contacted"
                    
                    if st.button(button_label, key=f"btn_contact_{idx}"):
                        # Locate lead in main list and flip contacted state
                        target_user = row.get("username")
                        target_url = row.get("url") or row.get("jump_url")
                        
                        for lead in leads:
                            lead_url = lead.get("url") or lead.get("jump_url")
                            if lead.get("username") == target_user and lead_url == target_url:
                                lead["contacted"] = not is_contacted
                                break
                        save_leads(leads)
                        st.success(f"Updated contacted status for {target_user}!")
                        st.rerun()

                with col_right:
                    message_draft = row.get('personalized_message') or ""
                    st.text_area("✍️ Personalized Message Draft", value=message_draft, height=140, key=f"txt_{idx}")
                    st.caption("Review, edit, and copy the draft above to reach out via their native platform.")

                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'/>", unsafe_allow_html=True)
