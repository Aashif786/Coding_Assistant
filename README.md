<div align="center">

# 🎙️ VOICE TO CODE ASSISTANT

### Hands-Free Programming for Visual Studio Code

**Code at the speed of speech.  
Accessible by design. Developer-grade by default.**

<br/>

![Platform](https://img.shields.io/badge/Platform-VS%20Code-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Speech](https://img.shields.io/badge/Speech-VOSK-orange)
![Status](https://img.shields.io/badge/Mode-Offline%20%26%20Private-success)

</div>

---

## 🚀 Overview

**Voice to Code Assistant** is a voice-driven development tool that transforms spoken commands into precise coding actions inside **Visual Studio Code**.

Designed with an **accessibility-first philosophy**, the assistant enables developers to navigate, edit, and control their IDE entirely through voice commands. Unlike cloud-based voice tools, this system operates **fully offline**, ensuring privacy, low latency, and reliability.

Whether you're optimizing ergonomics, recovering from repetitive strain injury, or exploring next-generation developer workflows, this assistant turns speech into a first-class programming interface.

---

## 🧠 System Architecture

The system follows a **decoupled client–server architecture**, enabling scalability, modularity, and easy future enhancements.

### 🔧 Backend Core (Speech & Intelligence Layer)

**Tech Stack:** Python · FastAPI · VOSK · SoundDevice

The backend acts as the cognitive engine of the assistant.

- **Speech-to-Text Engine**  
  Uses **VOSK**, a lightweight offline speech recognition framework. Audio is captured in real time via **SoundDevice**, ensuring fast and private transcription.

- **Intent Classification Engine**  
  Transcribed text is normalized to resolve ambiguities like  
  `"nine twenty" → "line 20"`  
  Commands are mapped using structured rules and pattern matching into actions such as:
  - `GOTO_LINE`
  - `REMOVE_LINE`
  - `DUPLICATE_LINE`
  - `GENERATE_CODE`

- **API Gateway**  
  **FastAPI** exposes a clean JSON-based interface between the speech engine and VS Code, maintaining low latency and strong separation of concerns.

---

### 🧩 VS Code Extension (Execution Layer)

**Tech Stack:** TypeScript · VS Code Extension API

The frontend integrates directly with the editor.

- **Context Awareness**  
  Continuously tracks cursor position, selected text, active language, and editor state to improve command accuracy.

- **Command Execution**  
  Translates backend responses into native VS Code actions, including:
  - Cursor navigation
  - Text manipulation
  - Editor shortcuts
  - Workflow commands

---

## ✨ Key Features

### 🧭 Navigation

_Move through code without touching the keyboard or mouse._

- “**Line 50**” → Jump to a specific line
- “**Top**” / “**Bottom**” → Navigate file boundaries

---

### ✍️ Editing & Manipulation

_Perform common coding actions using natural speech._

- “**Remove line**” → Delete current line
- “**Duplicate**” → Copy line downward
- “**Comment**” / “**Uncomment**”
- “**Undo**” / “**Redo**”

---

### ⚙️ Workflow Control

_Manage the IDE environment itself._

- “**Run code**” → Execute the current file
- “**Stop listening**” → Temporarily disable voice input
- “**Deactivate**” → Pause the assistant safely

---

## 🛠️ Installation & Setup

### Backend Setup

```bash
cd voice-backend

pip install fastapi uvicorn vosk sounddevice
```

Download the VOSK model (`vosk-model-small-en-us-0.15`) and extract it into the `models` folder.

Start the server:

```bash
uvicorn main:app --reload
```

---

### VS Code Extension Setup

```bash
cd voice-to-code
npm install
```

Press **F5** inside VS Code to launch the extension in a new development window.

---

## 👥 Contributors

We are a team of developers passionate about building accessible and efficient coding tools.

| Name                  | LinkedIn                                                                                                                                                                   | GitHub                                                                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Aashif Shadin K N** | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/aashifnoor)                      | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Aashif786)   |
| **Sharanya T**        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sharanya-thirumoorthi-6a47a8258) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sharanyazx)  |
| **Santhosh S**        | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/santhosh-s-37117823b)            | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/23-santhosh) |

---

<div align="center">

**“Technology should be an enabler, not a barrier.”**

</div>
