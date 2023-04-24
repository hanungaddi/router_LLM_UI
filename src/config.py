def input_config(ip_router, username, password):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip_router,
        'username': username,
        'password': password,
        'session_log': './logs/netmiko_session.log'
    }

    with open(".config.json", "w") as jsonfile:
        json.dump(device, jsonfile)