def parse_log():
    with open('./logs/netmiko_session.log', 'r') as file:
        log_snippet = file.read()

    pattern = '.*\(config\)#([\s\S]+?).*\(config\)#end'

    matches = re.findall(pattern, log_snippet)

    string = ''.join(matches)
    
    return string