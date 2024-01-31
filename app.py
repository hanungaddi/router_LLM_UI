from src.gradio import ui

if '__main__' == __name__:

    # Create Gradio interface  
    demo = ui()    

    # Run Gradio interface  
    demo.launch(debug=True, share=True)
