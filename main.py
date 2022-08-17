import interactions
import os
import dotenv

dotenv.load_dotenv()

CLIENT = interactions.Client(token=os.environ.get('jet2botkey'))

CLIENT.load("commands.uptime")

CLIENT.start()