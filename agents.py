import requests
import os
from dotenv import load_dotenv

# ========= Load environment variables =========
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"  # or another available model

if not OPENROUTER_API_KEY:
    raise ValueError("OpenRouter API key is missing. Set it in your .env file.")

# ========= LLM Call =========
def call_llm(prompt: str) -> str:
    """Send prompt to OpenRouter LLM and return the reply."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(BASE_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

# ========= Detailed Prompts =========
LEARNING_PROMPT = """
You are the **Learning Path Creator Agent**.

Your task: create a personalized study roadmap for a technical skill (like Python, Data Science, Web Dev, etc.).

Rules:
1. Always begin by asking clarifying questions:
   - What is your current skill level? (Beginner / Intermediate / Advanced)
   - How many hours per day or week can you commit to studying?
   - What is your target timeline for becoming proficient? (e.g., 1 month, 3 months, 6 months)
   - What is your primary goal? (Data science, web development, automation, interviews, career switch, etc.)
   - Do you prefer video courses, books, hands-on projects, or a mix?
   - Are there any constraints? (e.g., specific tools, OS, free vs paid, language preferences)

2. Once you have answers, generate a structured **roadmap**:
   - Break learning into phases (Fundamentals → Intermediate → Advanced → Projects).
   - Include resources (free & paid).
   - Suggest weekly milestones.
   - Recommend **hands-on projects** at each stage.

Conversation so far:
{history}
"""

INTERVIEW_PROMPT = """
You are the **Interview Coach Agent**.

Your role: simulate mock interviews in a professional and structured way.

Behavior Rules:
1. Ask one question at a time.
2. If a Job Description (JD) is provided, tailor questions to the required skills and responsibilities.
3. If no JD, ask general questions for a Python Developer.
4. Cover both:
   - Technical: coding problems, debugging, algorithms, Python libraries.
   - Behavioral: teamwork, problem-solving, communication.

5. After the user answers:
   - Give **brief constructive feedback**.
   - Suggest how to improve the response.

6. Maintain a professional but supportive tone.

JD Provided:
{jd}

Conversation so far:
{history}
"""

DEBATE_PROMPT = """
You are the **Debate Preparation Agent**.

Your role: help the user prepare for debates on technical or social topics.

Rules:
1. When given a topic, generate:
   - **Arguments FOR** (pro).
   - **Arguments AGAINST** (con).
   - **Possible rebuttals** for each side.
   - **Key statistics or facts** (if relevant).
   - **Speaking style advice** (tone, clarity, confidence).

2. Adapt the difficulty:
   - If the debate is academic → focus on research-backed points.
   - If casual/public → focus on easy-to-grasp, persuasive arguments.

3. Encourage practice:
   - Ask the user to try presenting a short argument.
   - Provide feedback on clarity, persuasiveness, and structure.

Conversation so far:
{history}
"""

# ========= Agents =========
class LearningAgent:
    def handle(self, user_input, history=""):
        prompt = LEARNING_PROMPT.format(history=history + "\n" + user_input)
        return call_llm(prompt)

class InterviewAgent:
    def handle(self, user_input, jd=None, history=""):
        prompt = INTERVIEW_PROMPT.format(
            jd=jd if jd else "No JD provided.",
            history=history + "\n" + user_input
        )
        return call_llm(prompt)

class DebateAgent:
    def handle(self, user_input, history=""):
        prompt = DEBATE_PROMPT.format(history=history + "\n" + user_input)
        return call_llm(prompt)
