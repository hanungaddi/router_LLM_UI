from src.config import input_config
from src.logging import parse_log
from src.request import send_request
import gradio as gr
from datetime import datetime as dt
from netmiko import ConnectHandler
import requests
import json
import re


def ui():
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
    
    return demo