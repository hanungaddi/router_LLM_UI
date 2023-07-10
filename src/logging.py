from datetime import datetime as dt
import re

def parse_log():
    with open(f'./logs/netmiko_session.log', 'r') as file:
        log_snippet = file.read()

    pattern = '\(config\)#\n([\s\S]+?.*end)'

    matches = re.findall(pattern, log_snippet)

    string = ''.join(matches)
    
    return string