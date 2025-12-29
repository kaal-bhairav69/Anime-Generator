# 🌌 SoulVerse — AI Anime Life Simulator

<p align="center">
  <img src="assets/Screenshot 2025-06-20 161018.png" width="85%">
</p>

**SoulVerse** is an AI-powered anime life simulator that generates **dynamic stories and anime-style visuals** in real time. Each run creates a **unique episode** — no hardcoded narratives, no static scenes.

---

## ✨ What It Does

- 🎭 Generates emotion-aware anime stories using AI
- 🖼️ Creates anime-style visuals from story context
- 🎶 Presents episodes in a **visual-novel style UI**
- 👤 Supports login/signup with **per-user episode history**
- 🗄️ Stores images directly in the database (binary storage)

---

## 🖼️ In-Game Experience

<p align="center">
  <img src="assets/Screenshot 2025-06-19 155915.png" width="45%">
  <img src="assets/Screenshot 2025-12-29 152926.png" width="45%">
</p>

---

## 🏗️ Architecture

```
User Interface (Visual Novel UI)
            ↓
    Flask Application Layer
            ↓
  AI Orchestration Layer (Agents)
            ↓
┌────────────────────────────────┐
│ Story Generation Agent (LLM)   │
│ - Emotion-aware narration      │
│ - Episodic coherence           │
└────────────────────────────────┘
            ↓
  Prompt Engineering Pipeline
            ↓
┌────────────────────────────────┐
│ Image Generation Engine        │
│ - Stable Diffusion + LoRA      │
│ - Anime-style visuals          │
└────────────────────────────────┘
            ↓
      Persistence Layer
            ↓
SQLAlchemy ORM → Database
(Users, Episodes, Image Blobs)
```

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI:** LLM-based story generation, anime image generation (LoRA)
- **Frontend:** HTML, CSS, JavaScript (visual novel UI)
- **Database:** SQL (user data, episodes, image blobs)

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/soulverse.git
cd soulverse

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

---

## 🎯 Why SoulVerse

- Not a static story generator
- Not just image generation
- A **full AI-driven narrative system** focused on immersion, emotion, and continuity

---

## 👨‍💻 Author

**Nimit Garg**  
AI / ML • Systems • Creative Engineering

Built with ❤️ using AI and creativity
---
