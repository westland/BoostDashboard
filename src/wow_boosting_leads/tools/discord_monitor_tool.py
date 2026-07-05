import os
import asyncio
from typing import List, Dict, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import discord

class DiscordSearchInput(BaseModel):
    guild_id: int = Field(..., description="Discord Server (Guild) ID")
    channel_ids: List[int] = Field(..., description="List of channel IDs to search")
    keywords: List[str] = Field(
        default=["WTB boost", "need carry", "stuck at", "arena help", "LF boost", "rating push"],
        description="Keywords to search for"
    )
    limit_per_channel: int = Field(default=50)

class DiscordWoWMonitorTool(BaseTool):
    name: str = "Discord WoW Boost Lead Monitor"
    description: str = (
        "Searches recent messages in specified Discord channels for players looking for WoW arena boosts/carries. "
        "Requires bot to be in the server with Read Message History permission."
    )
    args_schema: Type[BaseModel] = DiscordSearchInput

    def _run(self, guild_id: int, channel_ids: List[int], keywords: List[str] = None, limit_per_channel: int = 50) -> List[Dict]:
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            print("Discord bot token not set. Skipping Discord search.")
            return []

        if keywords is None:
            keywords = ["WTB boost", "need carry", "stuck at", "arena help", "LF boost", "rating push"]

        results = []

        async def search_discord():
            intents = discord.Intents.default()
            intents.message_content = True
            client = discord.Client(intents=intents)

            @client.event
            async def on_ready():
                try:
                    guild = client.get_guild(guild_id)
                    if not guild:
                        print(f"Discord guild with ID {guild_id} not found.")
                        await client.close()
                        return

                    for channel_id in channel_ids:
                        channel = guild.get_channel(channel_id)
                        if not channel:
                            print(f"Channel {channel_id} not found in guild.")
                            continue

                        try:
                            async for message in channel.history(limit=limit_per_channel):
                                if message.author.bot:
                                    continue
                                content_lower = message.content.lower()
                                if any(kw.lower() in content_lower for kw in keywords):
                                    results.append({
                                        "platform": "Discord",
                                        "channel": channel.name,
                                        "author": str(message.author),
                                        "content": message.content[:500],
                                        "jump_url": message.jump_url,
                                        "created_at": str(message.created_at),
                                    })
                        except Exception as e:
                            print(f"Discord error in channel {channel_id}: {e}")
                except Exception as e:
                    print(f"Error during discord search: {e}")
                finally:
                    await client.close()

            try:
                # Add a timeout to ensure it doesn't block the crew forever if connection hangs
                await asyncio.wait_for(client.start(token), timeout=30.0)
            except asyncio.TimeoutError:
                print("Discord client search timed out.")
                if not client.is_closed():
                    await client.close()
            except Exception as e:
                print(f"Discord client failed: {e}")

        try:
            # Check if there is an active running event loop to avoid RuntimeError in different runner configurations
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If running in Jupyter or streamlit where loop is already running, run as task or thread
                import nest_asyncio
                nest_asyncio.apply()
            asyncio.run(search_discord())
        except Exception as e:
            print(f"Failed to run async discord task: {e}")

        return results
