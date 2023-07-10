from datetime import datetime as dt
import json

def input_config(ip_router, username, password):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip_router,
        'username': username,
        'password': password,
        'session_log': f'./logs/netmiko_session.log'
    }

    with open(".config.json", "w") as jsonfile:
        json.dump(device, jsonfile)