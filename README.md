
# Interview Agents – Agentic AI Mock Interview System

**Interview Agents** is an agentic, multi-agent interview simulation platform built using **LangChain**, **Large Language Models (LLMs - Gemini)**, and structured tools. It orchestrates intelligent interview flows through four core agents: **Question/Answering**, **Evaluation**, **Follow-Up**, and **Chitchat**.

---

## Interview Agent Project Workflow

1. **Resume & Job Description Parsing**
   Uses tools like `ResumeParserTool` and `JDParserTool` to extract structured data from PDFs.

2. **LLM Tool Integration**
   The LLM dynamically accesses the tools to understand context (skills, experience, job requirements).

3. **Agent Execution Pipeline**

   * **Q/A Agent** initiates interview questions.
   * **Follow-Up Agent** generates clarification or deeper questions.
   * **Evaluation Agent** scores user responses.
   * **Chitchat Agent** keeps the conversation natural and human-like.

---

##  Architecture of Question Answering Agent

This image shows the inner workflow of the Q/A Agent, including how parsed data and LLM prompts work together to generate context-aware questions:

![QA Agent Architecture](https://i.postimg.cc/Qx21fv3G/Architecture-QA.png)

---

##  System Architecture (Full Agentic Pipeline)

The high-level system overview showing tool integration, LLM decision logic, and agent orchestration:

![System Architecture](https://i.postimg.cc/65R0q0nt/Untitled-diagram-Mermaid-Chart-2025-07-02-171151.png)

---

##  Key Components

###  Tools (used by LLM)

* **ResumeParserTool**

  * Extracts: name, education, experience, skills, certifications, projects.
  * Helps personalize interview questions.

* **JDParserTool**

  * Extracts: job role, responsibilities, required skills/tools.
  * Aligns interview content with job expectations.

> These are LangChain-compatible tools exposed using decorators or `Tool` abstraction.

---

## 🧑‍💼 Agents Overview

###  Question Answering (Q/A) Agent

* **Function**: Generates tailored interview questions.
* **Input**: Resume, JD data, and conversation history.
* **LLM**: Constructs prompts based on tool outputs and user responses.

###  Evaluation Agent

* **Function**: Scores user responses using predefined rubrics, keyword match, and semantic similarity.

###  Follow-Up Agent

* **Function**: Probes for deeper insights or clarifications if answers are vague or short.

###  Chitchat Agent

* **Function**: Adds warmth, breaks the ice, or transitions naturally between questions.

---

##  Tech Stack

| Layer                   | Tools/Tech Used                |
| ----------------------- | ------------------------------ |
| **LLM**                 | Gemini Pro            |
| **Agent Framework**     | LangChain                      |
| **Parsing Tools**       | ResumeParserTool, JDParserTool |
| **PDF Handling**        | pdfplumber                     |
| **Frontend (optional)** | Streamlit                      |
| **Backend**             | Python                         |

---

##  Sample Interaction

```txt
JD Skill Match: NLP, LangChain, Docker  
Resume Skill Match: OCR, LLM, API deployment

Q/A Agent: Can you explain how you used OCR in your last project?  
User: I used Tesseract with custom preprocessing for scanned PDFs.  
Evaluation Agent: 9.1/10 – Accurate and well-articulated.  
Follow-Up Agent: What kind of preprocessing techniques did you use?  
Chitchat Agent: Sounds like you’ve got solid project experience!
```

---

## 📁 Folder Structure

```
interview-agents/
├── tools/
│   ├── resume_parser_tool.py
│   └── jd_parser_tool.py
├── agents/
│   ├── qa_agent.py
│   ├── evaluation_agent.py
│   ├── followup_agent.py
│   └── chitchat_agent.py
├── main.py
└── README.md
```

---

##  Use Cases

* 🔹 AI-powered mock interview system
* 🔹 HR screening and candidate pre-filtering
* 🔹 AI career mentor/chatbot
* 🔹 Personalized upskilling platforms

---

##  Future Enhancements

*  Visual dashboards for response evaluation
*  Voice input & speech feedback support
*  Multilingual interviews (Nepali, Hindi, English)
*  Integration with real-time job boards & resume scoring

---

##  Author

**Ramdular Yadav**
AI Fellow @ Fusemachines
📧 [077bct066@ioepc.edu.np](mailto:077bct066@ioepc.edu.np) | 📞 9819936338

---
