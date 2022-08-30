import requests
import json
import os.path

CONFIG = json.load(open(os.path.dirname(__file__) + '/../config.json'))

def ROBLOX(discordID):
    extra = None
    jet2Group = None

    bloxlinkAPI = requests.get(f'https://v3.blox.link/developer/discord/{discordID}', headers={'api-key': 'd4be51ef-940e-4824-9fa3-ddb8f35f5ca7'})
    bloxlinkData = bloxlinkAPI.json()
    
    ROBLOXUserAPI = requests.get(f'https://users.roblox.com/v1/users/{bloxlinkData["user"]["primaryAccount"]}')
    ROBLOXUserData = ROBLOXUserAPI.json()

    ROBLOXGroupAPI = requests.get(f'https://groups.roblox.com/v2/users/{bloxlinkData["user"]["primaryAccount"]}/groups/roles')
    ROBLOXGroupData = ROBLOXGroupAPI.json()

    for group in ROBLOXGroupData['data']:
        if group['group']['id'] == CONFIG['groupID']:
            jet2Group = group
            role = group['role']['name']
            break
        else:
            role = None

    if role == None:
        output = {
            'username': ROBLOXUserData['name'],
            'role': 'Passenger',
            'extra': extra
        }
        return output
    else:
        if jet2Group['role']['rank'] > 250:
            extra = 'Executives'
        elif jet2Group['role']['rank'] > 5:
            extra = 'Directors'
        else:
            extra = None

        output = {
            'username': ROBLOXUserData['name'],
            'role': role,
            'extra': extra
        }

        return output