from utils import permissions
from discord.ext.commands import AutoShardedBot
from collections import Counter

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = Counter()
        self.color = 0x254d16

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)
        self.counter["cmds_ran"] += 1
