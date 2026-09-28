from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🎨 Welcome to ComicCraft!")
print("Create your own AI comic story!\n")

story_idea = input("Enter your story idea: ")

prompt = f"""
Create a short comic story based on this idea:

{story_idea}

Give the story in 5 comic panels.

For each panel, provide:
1. Scene
2. Character action
3. Dialogue
4. Image prompt

For the image prompt, describe the characters, background,
actions, emotions and comic-book style clearly.
Keep the same characters consistent across all 5 panels.
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print("\n===== YOUR COMIC STORY =====\n")
print(response.text)
with open("comic_story.txt", "w", encoding="utf-8") as file:
    file.write(response.text)