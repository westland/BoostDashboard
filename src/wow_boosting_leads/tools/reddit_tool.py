from typing import List, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import praw
import os

class RedditSearchInput(BaseModel):
    query: str = Field(..., description="Search keywords for WoW arena players")
    subreddits: List[str] = Field(default=["worldofpvp", "CompetitiveWoW", "wow"])
    limit: int = Field(default=12)

class RedditWoWSearchTool(BaseTool):
    name: str = "Reddit WoW PvP Lead Search"
    description: str = "Finds players struggling with arena ratings on Reddit."
    args_schema: Type[BaseModel] = RedditSearchInput

    def _run(self, query: str, subreddits: List[str] = None, limit: int = 12) -> List[Dict]:
        if subreddits is None:
            subreddits = ["worldofpvp", "CompetitiveWoW", "wow"]

        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT")

        if not client_id or not client_secret:
            print("Reddit API credentials not fully set in environment. Skipping Reddit search.")
            return []

        try:
            reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent or "WoWLeadAgent/1.0",
            )

            results = []
            for sub in subreddits:
                try:
                    for post in reddit.subreddit(sub).search(query, limit=limit, sort="new"):
                        if post.author:
                            results.append({
                                "platform": "Reddit",
                                "subreddit": sub,
                                "title": post.title,
                                "url": f"https://reddit.com{post.permalink}",
                                "author": post.author.name,
                                "selftext": post.selftext[:1800] if post.selftext else "",
                                "score": post.score,
                            })
                except Exception as e:
                    print(f"Reddit error searching sub r/{sub}: {e}")
            return results
        except Exception as e:
            print(f"Failed to initialize Reddit client: {e}")
            return []
