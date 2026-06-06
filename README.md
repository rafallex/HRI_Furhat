# HRI Furhat — a social robot for student mental-health check-ins

A [Furhat](https://furhatrobotics.com/) social robot that runs a short, empathetic, LLM-driven **mental-health check-in** with university students. It greets the student, asks a sequence of check-in questions, listens to spoken answers, reads the sentiment of each response, and replies with brief empathetic acknowledgements — with facial gestures and expressive LED cues throughout.

Built for a **Human-Robot Interaction** course project at Uppsala University.

## What it does

- **Spoken dialogue on a Furhat robot** — connects to the Furhat real-time API, configures the voice, and drives a greet → ask → listen → respond loop with LED state cues (`main.py`, `furhat_client.py`, `furhat_controller.py`).
- **LLM-driven empathetic responses** — a system prompt frames the robot as a social agent conducting a 3-minute student check-in, and each answer gets a short, empathetic acknowledgement (`LLMmodule.py`, `prompts.py`).
- **Pluggable LLM backends** — Groq, OpenAI, or Google **Gemini** can drive the conversation, selected via environment variables.
- **Sentiment sensing** — each student response is scored with a RoBERTa sentiment model (`cardiffnlp/twitter-roberta-base-sentiment-latest`) so the interaction can respond to how the student is feeling (`SentimentEmoModule.py`).
- **Facial gestures** — expressive gestures are triggered during the interaction (`facial_gestures.py`).

## Architecture

| File | Role |
|---|---|
| `main.py` | Orchestrates the greet → ask → listen → respond loop |
| `furhat_client.py` / `furhat_controller.py` | Furhat real-time API connection, voice, listen/speak, LED cues |
| `LLMmodule.py` | LLM dialogue (Groq / Gemini) and the check-in logic |
| `openai_helper.py` | OpenAI backend |
| `SentimentEmoModule.py` | RoBERTa sentiment scoring of student responses |
| `facial_gestures.py` | Furhat facial-gesture triggers |
| `prompts.py` | System and turn-level prompts for the check-in |

## The study it was built for

The system was the apparatus for a between-subjects HRI study: **does empathetic robot behaviour change how a social robot is perceived during a wellbeing check-in?** Two versions of the check-in were produced from identical scripts — an **empathetic** one (supportive language, smiles, eyebrow movement, reflective nods, attentive gaze, slowed prosody) and a **neutral** one (task-focused acknowledgements, steady gaze, no emotional expression).

Twenty-three Uppsala students were randomly assigned to one condition (empathetic *n* = 12, neutral *n* = 11) and rated the robot on the **Robotic Perceived Empathy (RoPE)** scale and the **Godspeed** likability/intelligence subscales. Mann–Whitney U tests found **no significant scale-level difference** between the conditions (RoPE *U* = 70.0, *p* = .49; likability *U* = 69.5, *p* = .34) — a useful reminder that for a short, clearly-structured check-in, a simpler neutral style can be about as acceptable as an expressive one.

## Team and my contribution

Group project for **1MD043 Human–Robot Interaction** (Uppsala) by **Dan Zhang**, **Venkatesh Akhouri**, **Rafael Proença**, and **Sami Mnif**.

My part: I assisted with the experimental design and the report, helped structure the interaction flow and the analysis, and added a **Google Gemini backend** to the system as an alternative to the OpenAI/Groq path.

## Running it

You need a Furhat robot (or the Furhat SDK desktop launcher) and API keys in a `.env` file at the project root:

```
FURHAT_AUTH_KEY=<your-furhat-key>
GROQ_API_KEY=<your-groq-key>        # for the Groq backend
OPENAI_API_KEY=<your-openai-key>    # for the OpenAI backend
GEMINI_API_KEY=<your-google-ai-key> # for the Gemini backend
```

```bash
pip install -r requirements.txt
python main.py
```

Keys are read from the environment — nothing is hard-coded. This repo is a fork of the group's shared project.
