import json
import requests
from datetime import datetime as dt
from netmiko import ConnectHandler
from src.logging import parse_log

def send_request(input_text, url):
    logs = []
    result = {}
    if input_text:
        logs.append(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] Predicting commands from text input")

        url = url+"/predict"
        
        payload = json.dumps(
            {
            "input": f"{input_text}"
            }
        )
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        result = response.json()

        logs.append(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing ML Outputs")

        result['commands'].remove('configure terminal')

        command = "\n".join(result['commands'])
        logs.append(f"[{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] Commands Generated (press Send Commands to apply the command)")

        output = []
        z = 0
        for i in result['commands']:
            z += 1
            output.append((i, str(z)))
    else:
        logs.append(f"Berikan input pada kolom masukan prompt!")

    return result['commands'] if 'commands' in result else None,  output, "\n".join(logs)

def send_command(commands, logs):
    with open(".config.json", "r") as jsonfile:
        device = json.load(jsonfile)
    
    with ConnectHandler(**device) as net_connect:
    # Send the commands
        net_connect.send_config_set(commands)

    router_log = parse_log()

    return router_log