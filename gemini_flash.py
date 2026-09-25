import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outline(prompt: str):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Create a 5-panel comic outline for: {prompt}")
    outline = []
    for i, panel in enumerate(response.text.split("\n")):
        outline.append({
            "panel": i+1,
            "title": f"Panel {i+1}",
            "desc": panel,
            "image_prompt": f"{prompt} comic style scene {i+1}"
        })
    return outline
