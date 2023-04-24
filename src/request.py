def send_request(input_text, url):

    with open(".config.json", "r") as jsonfile:
        device = json.load(jsonfile)

    logs = []
    logs.append(f"[{dt.now()}] Predicting commands from text input")

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

    logs.append(f"[{dt.now()}] Processing ML Outputs")

    result['commands'].remove('configure terminal')

    print(result['commands'])

    with ConnectHandler(**device) as net_connect:
    # Send the commands
        command = "\n".join(result['commands'])
        logs.append(f"[{dt.now()}] Sending \n{command} \nto {device['ip']}")
        net_connect.send_config_set(result['commands'])

    router_log = parse_log()

    return "\n".join(logs), router_log