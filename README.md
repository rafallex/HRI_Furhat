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

## Team and my contribution

Group project by **Sami Mnif**, **Venkatesh Akhouri**, and **Rafael Proença**.

My part: I added the **Google Gemini backend** as an alternative to the OpenAI/Groq path — so the robot can run on a free Google AI Studio key — and simplified the environment setup.

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
