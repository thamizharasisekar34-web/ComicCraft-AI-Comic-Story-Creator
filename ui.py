import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(
    page_title="ComicCraft",
    page_icon="🎨"
)

st.title("🎨 ComicCraft")
st.subheader("AI Comic Story Creator")

story_idea = st.text_area(
    "Enter your story idea:",
    placeholder="Example: A girl discovers a magical book"
)

if st.button("✨ Create Comic Story"):

    if story_idea:

        with st.spinner("🤖 Creating your comic story..."):

            prompt = f"""
Create a short comic story based on this idea:

{story_idea}

Create exactly 5 comic panels.

For each panel provide:
1. Scene
2. Character
3. Dialogue
4. Image Prompt

Keep the characters consistent across all panels.
Make the story simple, creative and suitable for a comic.
"""

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
            except Exception as e:
                st.error("⚠️ Gemini is temporarily unavailable. Please try again later.")
                st.stop()

        st.success("🎉 Your comic story is ready!")

        st.markdown("## 📖 Your Comic Story")

        st.write(response.text)

        with open("comic_story.txt", "w", encoding="utf-8") as file:
            file.write(response.text)

        st.info("💾 Story saved as comic_story.txt")

    else:
        st.warning("⚠️ Please enter a story idea.")