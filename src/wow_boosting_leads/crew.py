import os
import json
from typing import List, Dict, Type
from datetime import datetime
from pydantic import BaseModel, Field

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool

from .tools.reddit_tool import RedditWoWSearchTool
from .tools.discord_monitor_tool import DiscordWoWMonitorTool
from .tools.lead_utils import load_existing_leads, save_leads, is_duplicate

# Try importing standard CrewAI LLM (introduced in crewai >= 0.50.0)
try:
    from crewai import LLM
    HAS_CREW_LLM = True
except ImportError:
    HAS_CREW_LLM = False
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        # Fallback to standard langchain if installed
        from langchain.chat_models import ChatOpenAI

def get_llm():
    """Initializes and returns the LLM configured in the environment."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("Initializing Gemini LLM...")
        if HAS_CREW_LLM:
            return LLM(
                model="gemini/gemini-1.5-flash",
                api_key=gemini_key
            )
        else:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=gemini_key
                )
            except ImportError:
                # If langchain-google-genai isn't available, we fallback to langchain_openai with api_key
                return ChatOpenAI(
                    model="gemini/gemini-1.5-flash",
                    openai_api_key=gemini_key
                )

    grok_key = os.getenv("GROK_API_KEY")
    if grok_key:
        print("Initializing Grok LLM via xAI endpoint...")
        if HAS_CREW_LLM:
            return LLM(
                model="xai/grok-2-1212",
                api_key=grok_key,
                base_url="https://api.x.ai/v1"
            )
        else:
            return ChatOpenAI(
                model="grok-2-1212",
                openai_api_key=grok_key,
                openai_api_base="https://api.x.ai/v1"
            )
            
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("Initializing OpenAI LLM...")
        if HAS_CREW_LLM:
            return LLM(model="gpt-4o", api_key=openai_key)
        else:
            return ChatOpenAI(model="gpt-4o", openai_api_key=openai_key)
            
    print("WARNING: No GEMINI_API_KEY, GROK_API_KEY, or OPENAI_API_KEY was found in environment.")
    return None


class SaveLeadsInput(BaseModel):
    leads_json: str = Field(..., description="A JSON-formatted string representing the list of qualified leads.")

class SaveLeadsTool(BaseTool):
    name: str = "Save Leads Database Tool"
    description: str = (
        "Deduplicates new leads and appends them to the wow_leads.json file. "
        "Input must be a JSON string of a list of dictionary objects representing leads."
    )
    args_schema: Type[BaseModel] = SaveLeadsInput

    def _run(self, leads_json: str) -> str:
        try:
            # Clean markdown formatting backticks if present
            cleaned = leads_json.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            leads = json.loads(cleaned)
            if not isinstance(leads, list):
                leads = [leads]
        except Exception as e:
            return f"Error parsing JSON input: {e}. Please ensure input is a valid JSON string. Input was: {leads_json[:200]}..."

        existing = load_existing_leads()
        new_leads_added = 0
        for lead in leads:
            if not isinstance(lead, dict):
                continue
            if "timestamp" not in lead:
                lead["timestamp"] = datetime.now().isoformat()
            if "contacted" not in lead:
                lead["contacted"] = False

            if not is_duplicate(lead, existing):
                existing.append(lead)
                new_leads_added += 1

        save_leads(existing)
        return f"Successfully saved {new_leads_added} new leads to database. Total leads in database: {len(existing)}."

@CrewBase
class WoWBoostingLeadsCrew:
    """WoW Arena Boosting Lead Generation Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Load yaml configs manually to support CrewBase decorator properly across versions
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(base_dir, self.agents_config), "r", encoding="utf-8") as f:
            import yaml
            self.agents_config_dict = yaml.safe_load(f)
            
        with open(os.path.join(base_dir, self.tasks_config), "r", encoding="utf-8") as f:
            self.tasks_config_dict = yaml.safe_load(f)

    @agent
    def lead_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config_dict["lead_researcher"],
            tools=[RedditWoWSearchTool(), DiscordWoWMonitorTool()],
            llm=get_llm(),
            verbose=True,
        )

    @agent
    def lead_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config_dict["lead_analyzer"],
            llm=get_llm(),
            verbose=True
        )

    @agent
    def message_generator(self) -> Agent:
        return Agent(
            config=self.agents_config_dict["message_generator"],
            llm=get_llm(),
            verbose=True
        )

    @agent
    def lead_archiver(self) -> Agent:
        return Agent(
            config=self.agents_config_dict["lead_archiver"],
            tools=[SaveLeadsTool()],
            llm=get_llm(),
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config_dict["research_task"],
            agent=self.lead_researcher()
        )

    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config_dict["analyze_task"],
            agent=self.lead_analyzer()
        )

    @task
    def generate_task(self) -> Task:
        return Task(
            config=self.tasks_config_dict["generate_task"],
            agent=self.message_generator()
        )

    @task
    def save_task(self) -> Task:
        return Task(
            config=self.tasks_config_dict["save_task"],
            agent=self.lead_archiver()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.lead_researcher(),
                self.lead_analyzer(),
                self.message_generator(),
                self.lead_archiver()
            ],
            tasks=[
                self.research_task(),
                self.analyze_task(),
                self.generate_task(),
                self.save_task()
            ],
            process=Process.sequential,
            verbose=True,
        )
