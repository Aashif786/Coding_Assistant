<div align="center">

# 🎙️ VOICE TO CODE ASSISTANT

### Hands-Free Programming for Visual Studio Code

**Code at the speed of speech.  
Accessible by design. Developer-grade by default.**

<br/>

![Platform](https://img.shields.io/badge/Platform-VS%20Code-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Speech](https://img.shields.io/badge/Speech-OpenAI%20Whisper-orange)
![Status](https://img.shields.io/badge/Mode-Offline%20%26%20Private-success)

</div>

---

## 🚀 Overview

**Voice to Code Assistant** is a voice-driven development tool that transforms spoken commands into precise coding actions inside **Visual Studio Code**.

Designed with an **accessibility-first philosophy**, the assistant enables developers to navigate, edit, and control their IDE entirely through voice commands. Using the **OpenAI Whisper** model, this system operates **fully offline**, ensuring privacy, high accuracy for technical terms, and low latency.

Whether you're optimizing ergonomics, recovering from repetitive strain injury, or exploring next-generation developer workflows, this assistant turns speech into a first-class programming interface.

---

## 🧠 System Architecture

The system follows a **decoupled client–server architecture**, enabling scalability, modularity, and easy future enhancements.

### 🔧 Backend Core (Speech & Intelligence Layer)

**Tech Stack:** Python · FastAPI · OpenAI Whisper · SoundDevice

The backend acts as the cognitive engine of the assistant.

- **Speech-to-Text Engine**  
  Uses **OpenAI Whisper (Base)**, a state-of-the-art offline speech recognition model. Audio is captured in real time via **SoundDevice**, providing superior accuracy for technical programming terminology.

- **Intent Classification Engine**  
  Transcribed text is normalized to resolve common speech ambiguities. Commands are mapped using structured rules and pattern matching into dozens of VS Code actions.

- **API Gateway**  
  **FastAPI** exposes a clean JSON-based interface between the speech engine and VS Code, maintaining low latency and strong separation of concerns.

---

### 🧩 VS Code Extension (Execution Layer)

**Tech Stack:** TypeScript · VS Code Extension API

The frontend integrates directly with the editor.

- **Context Awareness**  
  Continuously tracks cursor position, active language, and editor state to provide context to the backend.

- **Command Execution**  
  Translates backend responses into native VS Code actions using the extension API and command palette.

---

## 🎤 Command Reference

### 🧭 Navigation

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Line [number]"** | Cursor jumps to the specified line number. | "Line 25" |
| **"Top"** | Moves cursor to the start of the file. | "Top" |
| **"Bottom"** | Moves cursor to the end of the file. | "Bottom" |
| **"Start of line"** | Moves cursor to the beginning of the current line. | "Start of line" |
| **"End of line"** | Moves cursor to the end of the current line. | "End of line" |
| **"Go to [symbol]"** | Searches for a function, class, or symbol definition. | "Go to login_user" |
| **"Find [name]"** | Same as symbol search. | "Find UserProfile" |

### ✍️ Editing & Selection

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Remove line"** | Deletes the current line. | "Remove line" |
| **"Remove line [N]"** | Deletes a specific line number. | "Remove line 15" |
| **"Delete word"** | Deletes the word to the right of the cursor. | "Delete word" |
| **"Select line"** | Selects the entire current line. | "Select line" |
| **"Select word"** | Selects the word at the cursor. | "Select word" |
| **"Duplicate"** | Duplicates the current line downwards. | "Duplicate" |
| **"Comment"** | Comments out the current line. | "Comment" |
| **"Uncomment"** | Uncomments the current line. | "Uncomment" |
| **"Toggle comment"**| Toggles comment on current line or selection. | "Toggle comment" |
| **"New line above"** | Inserts a new line above the current one. | "New line above" |
| **"New line below"** | Inserts a new line below the current one. | "New line below" |

### 📂 File & Workspace

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Create file [X]"** | Creates and opens a new file in the workspace. | "Create file app.py" |
| **"Open file [X]"** | Searches and opens an existing file. | "Open file main.ts" |
| **"Save file"** | Saves the active document. | "Save file" |
| **"Close file"** | Closes the active editor tab. | "Close file" |

### 📋 Clipboard

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Select all"** | Selects the entire contents of the file. | "Select all" |
| **"Copy"** | Copies the current selection to the clipboard. | "Copy" |
| **"Cut"** | Cuts the current selection to the clipboard. | "Cut" |
| **"Paste"** | Pastes content from the clipboard. | "Paste" |

### ⚡ AI-Powered Generation

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Code [prompt]"** | Uses AI to generate raw code based on prompt. | "Code a for loop over a list" |
| **"Create function [X]"** | Generates a language-specific function template. | "Create function calculate" |
| **"Create class [X]"** | Generates a language-specific class template. | "Create class Vehicle" |
| **"Print [text]"** | Inserts a print statement. | "Print database connected" |

### 🧠 AI Intelligence & Debugging

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Debug [line]"** | Analyzes a specific line for potential errors via AI. | "Debug line 42" |
| **"Explain error"** | Provides a natural language explanation of the error. | "Explain error" |
| **"Fix error"** | Uses AI to propose and apply a fix for current error. | "Fix error" |

### ⚙️ System & Workflow

| Command | Action | Example |
| :--- | :--- | :--- |
| **"Run code"** | Executes the current file. | "Run code" |
| **"Undo"** | Reverses the last action. | "Undo" |
| **"Redo"** | Re-applies the last undone action. | "Redo" |
| **"Find"** | Opens the VS Code find widget. | "Find" |
| **"Replace"** | Opens the find and replace widget. | "Replace" |
| **"Stop listening"** | Deactivates the voice mode loop. | "Stop listening" |

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
