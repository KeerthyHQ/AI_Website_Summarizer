
import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Initialize Gemini client
gemini_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 3. Initialize Groq client
groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# 4. Common function to ask an LLM
def ask(client, model, user_prompt):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# 5. Battle function
def battle(user_prompt):

    # Ask Gemini
    try:
        a = ask(
            gemini_client,
            "gemini-3.8-flash",
            user_prompt
        )
    except Exception as e:
        a = f"Gemini Error: {str(e)}"

    # Ask Groq
    try:
        b = ask(
            groq_client,
            "openai/gpt-oss-120b",
            user_prompt
        )
    except Exception as e:
        b = f"Groq Error: {str(e)}"

    return a, b


# 6. Voting function
def vote(label):
    return f"🗳️ Thanks! You voted: **{label}**"


# 7. Create Gradio interface
with gr.Blocks(title="LLM Arena") as demo:

    gr.Markdown("# 🥊 LLM Arena — One Prompt, Two Models")

    prompt_box = gr.Textbox(
        label="Ask both models the same thing",
        placeholder="Enter your prompt here..."
    )

    go = gr.Button("⚔️ Battle!", variant="primary")

    with gr.Row():

        with gr.Column():
            gr.Markdown("### 🤖 Model A (Gemini)")
            out_a = gr.Markdown()

            with gr.Row():
                up_a = gr.Button("👍")
                down_a = gr.Button("👎")

        with gr.Column():
            gr.Markdown("### 🤖 Model B (Groq)")
            out_b = gr.Markdown()

            with gr.Row():
                up_b = gr.Button("👍")
                down_b = gr.Button("👎")

    verdict = gr.Markdown()

    # 8. Disable button when clicked
    battle_event = go.click(
        fn=lambda: gr.update(
            interactive=False,
            value="⏳ Generating..."
        ),
        outputs=go,
        queue=False
    )

    # 9. Run battle and show loading indicator
    battle_event = battle_event.then(
        fn=battle,
        inputs=prompt_box,
        outputs=[out_a, out_b],
        show_progress="full",
        show_progress_on=[go]
    )

    # 10. Enable button after completion
    battle_event.then(
        fn=lambda: gr.update(
            interactive=True,
            value="⚔️ Battle!"
        ),
        outputs=go,
        queue=False
    )

    # 11. Voting events
    up_a.click(
        lambda: vote("👍 Model A"),
        outputs=verdict
    )

    down_a.click(
        lambda: vote("👎 Model A"),
        outputs=verdict
    )

    up_b.click(
        lambda: vote("👍 Model B"),
        outputs=verdict
    )

    down_b.click(
        lambda: vote("👎 Model B"),
        outputs=verdict
    )


# 12. Launch application
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    demo.queue()

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )



#models = gemini_client.models.list()

#for model in models:
#    print(model.id)   