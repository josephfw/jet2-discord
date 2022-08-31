import interactions
import time
from functions import jfw

startTime = time.time()

class uptime(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name = 'uptime',
        description = 'Display the length of time the bot has been online for.'
    )
    async def uptime_command(self, ctx):
        endTime = time.time()
        duration = jfw.timeDuration(startTime, endTime)

        await ctx.send(
            embeds = [
                interactions.Embed(
                    color = 0x2F3136,
                    fields = [
                        interactions.EmbedField(
                            name = 'Bot Uptime',
                            value = f'{duration[0]} days, {duration[1]} hours, {duration[2]} minutes, {duration[3]} seconds'
                        )
                    ]
                )
            ],
            ephemeral = False
        )

def setup(client):
    uptime(client)