import gradio as gr 

from summarizer import summarize

# UI function
gr.Interface(
    fn=summarize,                                  
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="🔎 AI Website Summarizer",
).launch(share=True)  # share=True → a public link you can post! 