import os
import json
import re
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def fallback_recommendation(query: str):
    """Fallback if Gemini fails."""
    q = query.lower()
    if any(k in q for k in ["chill", "relax", "calm", "sunset"]):
        return {"title": "Sunset Lover", "artist": "Petit Biscuit"}
    if any(k in q for k in ["workout", "energy", "pump", "gym"]):
        return {"title": "Till I Collapse", "artist": "Eminem"}
    if any(k in q for k in ["romantic", "love", "date", "valentine"]):
        return {"title": "All of Me", "artist": "John Legend"}
    if any(k in q for k in ["sad", "heartbreak", "lonely"]):
        return {"title": "Someone Like You", "artist": "Adele"}
    if any(k in q for k in ["party", "dance", "club", "fun"]):
        return {"title": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars"}
    return {"title": "Blinding Lights", "artist": "The Weeknd"}

def recommend_title_artist(query: str):
    """Return {title, artist} using Gemini given any keyword(s)."""
    query = (query or "popular").strip()

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
You are a music recommendation assistant.
Given any keywords, topics, or themes, recommend ONE real song that fits.

Respond ONLY as JSON with two fields:
"title" and "artist".

User input: "{query}"
Example output:
{{"title": "Shape of You", "artist": "Ed Sheeran"}}
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # Try to extract JSON
        match = re.search(r"\{.*\}", text, re.DOTALL)
        json_text = match.group(0) if match else text

        try:
            data = json.loads(json_text)
            title = data.get("title", "").strip()
            artist = data.get("artist", "").strip()
            if title and artist:
                return {"title": title, "artist": artist}
        except json.JSONDecodeError:
            pass

    except Exception as e:
        print("Gemini error:", e)

    return fallback_recommendation(query)
