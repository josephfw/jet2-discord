import interactions
import os
import dotenv
from interactions.ext.wait_for import setup

dotenv.load_dotenv()

CLIENT = interactions.Client(token=os.environ.get('key'), intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MESSAGE_CONTENT)

CLIENT.load("commands.uptime")
CLIENT.load("commands.announce")

setup(CLIENT)
CLIENT.start()