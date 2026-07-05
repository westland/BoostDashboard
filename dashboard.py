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

st.markdown('<div class="main-title">🚀 WoW PvP Lead Control Center</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Intelligent lead generation & qualification hub for WoW Arena Coaching & Self-Play</div>', unsafe_allow_html=True)

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
