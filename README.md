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

## 🎤 Command Reference

### 🧭 Navigation

| Command             | Action                                                | Example                 |
| :------------------ | :---------------------------------------------------- | :---------------------- |
| **"Line [number]"** | Cursor jumps to the specified line number.            | "Line 25"               |
| **"Top"**           | Moves cursor to the start of the file.                | "Top"                   |
| **"Bottom"**        | Moves cursor to the end of the file.                  | "Bottom"                |
| **"Go to [name]"**  | Searches for a function, class, or symbol definition. | "Go to calculate_total" |
| **"Find [name]"**   | Same as "Go to".                                      | "Find user_model"       |

### ✍️ Editing & Manipulation

| Command                    | Action                                 | Example          |
| :------------------------- | :------------------------------------- | :--------------- |
| **"Remove line"**          | Deletes the current line.              | "Remove line"    |
| **"Remove line [number]"** | Deletes a specific line number.        | "Remove line 15" |
| **"Duplicate"**            | Duplicates the current line downwards. | "Duplicate"      |
| **"Comment"**              | Comments out the current line.         | "Comment"        |
| **"Uncomment"**            | Uncomments the current line.           | "Uncomment"      |
| **"Undo"**                 | Reverses the last action.              | "Undo"           |
| **"Redo"**                 | Re-applies the last undone action.     | "Redo"           |

### ⚡ Code Generation

| Command                      | Action                                              | Example                           |
| :--------------------------- | :-------------------------------------------------- | :-------------------------------- |
| **"Create function [name]"** | Generates a function template with the given name.  | "Create function login_user"      |
| **"Create class [name]"**    | Generates a class template.                         | "Create class PaymentProcessor"   |
| **"For"**                    | Inserts a for-loop template.                        | "For"                             |
| **"While"**                  | Inserts a while-loop template.                      | "While"                           |
| **"Print [text]"**           | Inserts a print statement with the text.            | "Print hello world"               |
| **"[Any other prompt]"**     | Uses AI to generate code based on your description. | "Create a binary search function" |

### ⚙️ System & Workflow

| Command              | Action                             | Example          |
| :------------------- | :--------------------------------- | :--------------- |
| **"Run code"**       | Runs the current file (or debugs). | "Run code"       |
| **"Stop listening"** | Deactivates voice mode loop.       | "Stop listening" |
| **"Exit / Kill"**    | Same as stopping listening.        | "Exit voice"     |

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
