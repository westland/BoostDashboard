import os
import sys

# Ensure project root is in sys.path to allow execution both as script and module
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
# Load .env file from the project root
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

try:
    from src.wow_boosting_leads.crew import WoWBoostingLeadsCrew
except ImportError:
    from wow_boosting_leads.crew import WoWBoostingLeadsCrew

def run():
    print("🚀 Starting WoW Boosting Lead Generation Crew...")
    try:
        crew_instance = WoWBoostingLeadsCrew()
        result = crew_instance.crew().kickoff()
        print("\n✅ Crew execution finished successfully!")
        print(result)
    except Exception as e:
        print(f"\n❌ Error during crew execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run()
