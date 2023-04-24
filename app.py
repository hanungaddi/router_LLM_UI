import requests
import json
import gradio as gr
import re
from datetime import datetime as dt
from netmiko import ConnectHandler

def input_config(ip_router, username, password):
    device = {
        'device_type': 'cisco_ios',
        'ip': ip_router,
        'username': username,
        'password': password,
        'session_log': 'netmiko_session.log'
    }

    with open(".config.json", "w") as jsonfile:
        json.dump(device, jsonfile)

def parse_log():
    with open('netmiko_session.log', 'r') as file:
        log_snippet = file.read()

    pattern = '.*\(config\)#([\s\S]+?).*\(config\)#end'

    matches = re.findall(pattern, log_snippet)

    # Print the matched string
    for match in matches:
        print(match.strip())


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


if '__main__' == __name__:

    # Create Gradio interface
    with gr.Blocks() as demo:
        gr.Markdown("Contoh proof of concept Tugas Akhir NLP Router Configuration.")
        with gr.Tab("Settings"):
            with gr.Row():
                with gr.Column():
                    ml_backend = gr.Textbox(label="Masukkan URL API ML:", type="text")
                    ip_input = gr.Textbox(label="Masukkan IP address Router:", type="text")
                    username_input = gr.Textbox(label="Masukkan username Router:", type="text")
                    password_input = gr.Textbox(label="Masukkan password Router:", type="password")
                
        with gr.Tab("Chatbot"):
            with gr.Column():
                with gr.Row():
                    output_chatbot = gr.Textbox(label="Logs:")
                    router_logs = gr.Textbox(label="Router Log:")
                input_chatbot = gr.Textbox(label="Masukkan prompt:", type="text", default="Masukkan perintah konfigurasi di sini")
            chat_button = gr.Button("Send")
    
        chat_button.click(input_config, [ip_input, username_input, password_input]).then(send_request, [input_chatbot, ml_backend], [output_chatbot, router_logs])
            
    demo.launch(debug=True)