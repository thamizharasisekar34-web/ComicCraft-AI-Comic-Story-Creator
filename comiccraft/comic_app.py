import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()

# Connect to Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# --------------------------------------------------
# Generate comic panel image
# --------------------------------------------------

def generate_panel_image(image_prompt, panel_number):

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-image",
            contents=image_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"]
            )
        )

        for part in response.parts:

            if part.inline_data:

                image = part.as_image()

                image_path = f"comic_panel_{panel_number}.png"

                image.save(image_path)

                return image_path

        return None

    except Exception as e:

        st.error(
            f"Image generation error for Panel {panel_number}: {e}"
        )

        return None


# --------------------------------------------------
# Page settings
# --------------------------------------------------

st.set_page_config(
    page_title="ComicCraft",
    page_icon="🎨"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🎨 ComicCraft")

st.write(
    "Create your own AI comic story!"
)

st.caption(
    "✨ Turn your imagination into a 5-panel comic story with AI!"
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("🎨 About ComicCraft")

    st.write(
        "ComicCraft uses Gemini AI to transform "
        "your story idea into a 5-panel comic story."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("📖 AI Story Generation")
    st.write("🖼️ AI Comic Images")
    st.write("💬 Character Dialogues")
    st.write("🎭 Character Consistency")
    st.write("📥 Story Download")


st.divider()


# --------------------------------------------------
# Story input
# --------------------------------------------------

story_idea = st.text_area(
    "💡 Enter your comic story idea:",
    placeholder="Example: A village girl discovers a magical book..."
)

st.info(
    "🎭 Characters will stay consistent across all 5 panels."
)


# --------------------------------------------------
# Clear button
# --------------------------------------------------

if st.button("🗑️ Clear"):

    st.rerun()


# --------------------------------------------------
# Generate Comic
# --------------------------------------------------

if st.button("🚀 Generate My Comic"):

    if story_idea.strip():

        # ------------------------------------------
        # Generate Story
        # ------------------------------------------

        with st.spinner(
            "Creating your comic story..."
        ):

            prompt = f"""
Create a short comic story based on this idea:

{story_idea}

Give the story in exactly 5 comic panels.

Use these exact headings:

Panel 1
Panel 2
Panel 3
Panel 4
Panel 5

For each panel, provide:

1. Scene
2. Character action
3. Dialogue
4. Image prompt

Make the image prompt detailed enough for an AI image generator.

The image prompt must include:

- Character appearance
- Character clothing
- Background
- Character pose and action
- Facial expression
- Lighting
- Comic art style

Keep the same characters consistent across all 5 panels.

For each character, maintain the same:

- Name
- Age
- Appearance
- Hairstyle
- Clothing
- Personality

Do not change the character's appearance or clothing
between panels.
"""

            try:

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

            except Exception as e:

                error_message = str(e)

                if "503" in error_message:

                    st.error(
                        "⚠️ Gemini is temporarily busy. "
                        "Please wait and try again."
                    )

                elif "429" in error_message:

                    st.error(
                        "⚠️ Gemini API quota has been reached. "
                        "Please try again later."
                    )

                elif "404" in error_message:

                    st.error(
                        "⚠️ Gemini model was not found. "
                        "Please check the model name."
                    )

                else:

                    st.error(
                        "⚠️ Gemini Error:"
                    )

                    st.code(
                        error_message
                    )

                st.stop()


        # ------------------------------------------
        # Story ready
        # ------------------------------------------

        st.success(
            "🎨 Your ComicCraft story is ready!"
        )

        st.markdown(
            "## 📖 Your Comic Story"
        )

        st.markdown(
            "### 🖼️ Comic Panels"
        )

        st.info(
            "✨ ComicCraft will now create an image "
            "for each panel."
        )


        # ------------------------------------------
        # Split panels
        # ------------------------------------------

        panels = response.text.split("Panel ")


        # ------------------------------------------
        # Display each panel
        # ------------------------------------------

        for panel_number, panel in enumerate(
            panels[1:],
            start=1
        ):

            st.markdown("---")


            # --------------------------------------
            # Get Image Prompt
            # --------------------------------------

            panel_image = None

            # Get Image Prompt
            panel_image = None

            image_prompt = ""

            if "Image Prompt:" in panel:
                image_prompt = panel.split("Image Prompt:", 1)[1].strip()

            elif "Image prompt:" in panel:
                image_prompt = panel.split("Image prompt:", 1)[1].strip()

            elif "4. Image prompt" in panel:
                image_prompt = panel.split("4. Image prompt", 1)[1].strip()

            elif "4. Image Prompt" in panel:
                image_prompt = panel.split("4. Image Prompt", 1)[1].strip()


            if image_prompt:

                with st.spinner(
                    f"🎨 Generating Panel {panel_number} image..."
                ):

                    panel_image = generate_panel_image(
                        image_prompt,
                        panel_number
                    )


            if panel_image:

                st.image(
                    panel_image,
                    caption=f"🖼️ Comic Panel {panel_number}",
                    use_container_width=True
                )

                with st.spinner(
                    f"🎨 Generating Panel {panel_number} image..."
                ):

                    panel_image = generate_panel_image(
                        image_prompt,
                        panel_number
                    )


            # --------------------------------------
            # Display Image
            # --------------------------------------

            if panel_image:

                st.image(
                    panel_image,
                    caption=f"🖼️ Comic Panel {panel_number}",
                    use_container_width=True
                )


            # --------------------------------------
            # Panel box
            # --------------------------------------

            lines = panel.split(
                "\n",
                1
            )


            st.markdown(
                f"""
                <div style="
                    padding: 20px;
                    border-radius: 15px;
                    border: 2px solid #dddddd;
                    margin-bottom: 20px;
                ">
                <h3>📖 Panel {lines[0]}</h3>
                """,
                unsafe_allow_html=True
            )


            if len(lines) > 1:

                content = lines[1]


                content = content.replace(
                    "1. Scene",
                    "🎬 Scene"
                ).replace(
                    "Scene:",
                    "🎬 Scene:"
                )


                content = content.replace(
                    "2. Character action",
                    "🎭 Character Action"
                ).replace(
                    "Character action:",
                    "🎭 Character Action:"
                )


                content = content.replace(
                    "3. Dialogue",
                    "💬 Dialogue"
                ).replace(
                    "Dialogue:",
                    "💬 Dialogue:"
                )


                content = content.replace(
                    "4. Image prompt",
                    "🖼️ Image Prompt"
                ).replace(
                    "Image prompt:",
                    "🖼️ Image Prompt:"
                )


                st.markdown(
                    content
                )


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # ------------------------------------------
        # Final message
        # ------------------------------------------

        # ------------------------------------------
        # Save story
        # ------------------------------------------

        with open(
            "comic_story.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                response.text
            )


        # ------------------------------------------
        # Download story
        # ------------------------------------------

        st.download_button(
            "📥 Download Your Comic Story",
            response.text,
            file_name="ComicCraft_Story.txt"
        )


    else:

        st.warning(
            "💡 Please enter a story idea to create your comic!"
        )