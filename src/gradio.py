from src.config import input_config
from src.request import send_request, send_command
import gradio as gr

def ui():
    with gr.Blocks(theme='gradio/monochrome') as demo:
        gr.Markdown("Contoh proof of concept Tugas Akhir NLP Router Configuration.")
        with gr.Tab("Settings"):
            with gr.Row():
                with gr.Column():
                    ml_backend = gr.Textbox(label="Masukkan URL API ML:", type="text")
                    ip_input = gr.Textbox(label="Masukkan IP address Router:", type="text")
                    username_input = gr.Textbox(label="Masukkan username Router:", type="text")
                    password_input = gr.Textbox(label="Masukkan password Router:", type="password")
                
        with gr.Tab("Chatbot"):
            commands = gr.State()
            with gr.Column():
                with gr.Row():
                    output_chatbot = gr.Textbox(label="Logs:")
                    router_logs = gr.Textbox(label="Router Log:")
                ml_output = gr.HighlightedText(label="Commands:")
                input_chatbot = gr.Textbox(label="Masukkan prompt:", type="text", default="Masukkan perintah konfigurasi di sini")
            with gr.Row():
                generate_button = gr.Button("Generate Commands")
                send_button = gr.Button("Send Commands")
        
        generate_button.click(send_request, [input_chatbot, ml_backend], [commands, ml_output, output_chatbot])
        send_button.click(input_config, [ip_input, username_input, password_input]).then(send_command, [commands, output_chatbot], [router_logs])
    
    return demo