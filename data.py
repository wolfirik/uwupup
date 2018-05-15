from utils import permissions
from discord.ext.commands import AutoShardedBot
from collections import Counter

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = Counter()

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)
        self.counter["commands_ran"] += 1
