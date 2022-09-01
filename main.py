import interactions
import os
import dotenv
from interactions.ext.wait_for import setup

dotenv.load_dotenv()

CLIENT = interactions.Client(token=os.environ.get('key'), intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

CLIENT.load("commands.misc.uptime")
CLIENT.load("commands.misc.announce")

setup(CLIENT)
CLIENT.start()