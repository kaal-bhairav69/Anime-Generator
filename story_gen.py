import json
from phi.agent import Agent
from phi.model.groq import Groq
import datetime
import db
import os
import crud
from generate import generate_image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

story_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    name="Storyteller",
    role="generate anime stories",
    instructions=[
        "You are a legendary anime storyteller.",
        "Start the story with a one-line poetic title prefixed with ###",
        "Write a fantasy story set in anime world of 6-7 lines",
        "Each story must vividly show a single character **experiencing the emotion** in a visually compelling anime scene.",
        "the story should be in such a way that it holds the interest of the reader",
        "the story should be like a fantasy , it should be entertaining."
        "No summaries. No explanations. Just the moment."
    ],
    show_tool_calls=True,
    markdown=True
)

visual_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    name="VisualPrompt",
    role="anime image prompt engineer",
instructions = [
    "You are an expert in generating Stable Diffusion prompts for anime-style scenes.",
    "Convert a poetic story into a vivid, concrete, and visual prompt.",
    "The character should be small, seen from a distance, and match the story’s mood.",
    "Focus on making the background beautiful,vibrant,wide,8k, cinematic, and alligned with story.",
    "Mention props and key emotional action if any.",
    "Use no more than 77 tokens in total.",
    "Return only the prompt — no titles, explanations, or summaries."
],
    show_tool_calls=False,
    markdown=False
)

def get_past_context(user_id,max_content=3):
    db_session = db.SessionLocal()  
    memory_scenes = crud.get_recent_episodes(db_session,user_id, limit=max_content)
    db_session.close()
    if not memory_scenes:
        return ""
    context=""
    for i in memory_scenes:
        context += i.story + "\n\n"

    return context.strip()


def get_story(emotion: str,user_id:int):
    context_of_story = get_past_context(user_id=user_id,max_content=3)
    
    # ✅ moved prompt construction inside the function
    prompt = f"""
    Emotion + gender of character: {emotion}

    Context: {context_of_story}
    Use the above emotion and context to generate the **next anime episode** in the this fantasy story.

    The story should now be cinematic,fantasy,entertaining, and emotionally engaging — like a **real anime episode**. Include dynamic visual moments, small actions, and a character reacting emotionally **within an unfolding event** (e.g. argument, flashback, conflict, performance, accident, discovery, mystery etc).

    ✦ Use the emotion and generate a fantasy story in a fantasy world of that.
    ✦ Keep the character at the center of the story.
    ✦ Title should be different everytime , it should not contain words from past context and should not contain moonlit
    ✦ Include light plot movement — something should change by the end of the scene.
    ✦ Always write with a sense of emotional weight, cinematic imagery, and immersive visuals.
    ✦ Avoid repetition of phrases or previous context lines.
    ✦ Avoid making scene exaclty given in the emotion , make a fantasy world.
    ✦ Keep it short (7–8 lines), tightly written, but full of **movement, subtle tension**, and **visual cues**.

    Start with a poetic one-line title prefixed with ###

    The story must feel like it's part of a real fantasy set in anime world — like a scene you'd watch — not just abstract emotion.

    "End the story with a feeling of suspense, revelation, or change — something that makes the reader want to see what happens next."

    Just write the story. No summaries. No explanation.
    """

    response = story_agent.run(prompt)
    return response.content.strip()


def get_character(story):
    response = visual_agent.run(story)
    return response.content.strip()

def extract_title(story):
    lines = story.strip().splitlines()
    for line in lines:
        if line.startswith("###"):
            return line.replace("###", "").strip()
    return "Untitled"

def generate_episode(emotion,user_id ,db=None):
    story = get_story(emotion,user_id)
    title = extract_title(story)
    story_lines = story.splitlines()
    if story_lines and story_lines[0].startswith("### "):
        story = '\n'.join(story_lines[1:])
    scene = get_character(story)
    image_data = generate_image(scene)
    return story.strip(), scene,title, image_data