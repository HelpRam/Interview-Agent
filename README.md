
# Interview Agents – Agentic AI Mock Interview System

**Interview Agents** is a LangChain-based multi-agent system that mimics intelligent, structured interviews. It integrates **large language models**, **resume/job description tools**, and dynamic agents like Q/A, Evaluation, Follow-Up, and Chitchat agents – all orchestrated in a seamless workflow.

This system is ideal for:

* AI-powered **mock interviews**
* **HR screening bots**
* Learning or upskilling platforms
* Agentic AI showcases

---

##  Interview Agent Project Flow (Short Summary)

1.  **PDF Extraction**: Resumes and Job Descriptions are passed to tools that extract structured info.
2.  **Tool Creation**:

   * `ResumeParserTool` and `JDParserTool` wrap this logic as LangChain Tools.
3.  **LLM Orchestration**: A Large Language Model (e.g., Gemini or GPT-4) dynamically uses these tools to understand user-job context.
4.  **Agent Execution**: Q/A Agent asks questions, Follow-Up Agent digs deeper, Evaluation Agent scores answers, and Chitchat Agent keeps it friendly.

---

##  System Architecture Diagram

![System Architecture](https://i.postimg.cc/65R0q0nt/Untitled-diagram-Mermaid-Chart-2025-07-02-171151.png)



##  Key Components

###  Tools (Used by LLM)

* **ResumeParserTool**

  * Extracts name, experience, skills, education, certifications, and projects.
  * Used to tailor questions to a candidate's profile.

* **JDParserTool**

  * Extracts job role, required skills, tools, responsibilities.
  * Helps align interview flow with job requirements.

>  These tools are LangChain-compatible and exposed to the LLM using `tool` decorators or LangChain's Tool abstraction.

---

###  Agents Overview

####  Q/A Agent

* **Role**: Drives the conversation with job- and resume-aligned questions.
* **Context**: Uses parsed data via LLM tool calls.

####  Evaluation Agent

* **Role**: Evaluates answer quality using scoring rubrics and semantic similarity.

####  Follow-Up Agent

* **Role**: Generates clarification or deep-dive questions if the initial answer is vague or shallow.

####  Chitchat Agent

* **Role**: Humanizes the interaction; detects tone or breaks the ice.

---

##  Tech Stack

| Layer               | Tools Use                      |
| ------------------- | ---------------------------------- |
| LLM                 | Gemini Pro          |
| Agent Framework     | LangChain                          |
| Resume/JD Tools     | `ResumeParserTool`, `JDParserTool` |
| File Handling       | pdfplumber              |
| Backend / Interface | Python / Streamlit (optional)      |

---

##  Sample Output

```
 JD Skill Match: NLP, LangChain, Docker
 Resume Skill Match: OCR, LLM, API deployment

Q/A Agent: Can you explain how you used OCR in your last project?
User: I used Tesseract with custom preprocessing for scanned PDFs.
Evaluation Agent: 9.1/10 – Accurate and well-articulated.
Follow-Up Agent: What kind of preprocessing techniques did you use?
Chitchat Agent: Sounds like you’ve got solid project experience!
```

---

## Folder Structure

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

* 🔹 Job interview preparation
* 🔹 Screening assistant for recruiters
* 🔹 AI companion for career coaching
* 🔹 Personalized learning assessments

---

##  Future Plans

*  Visual evaluation dashboards
*  Voice input + speech feedback
*  Multilingual mode (Nepali, Hindi, English)
*  Integration with real job boards

---

##  Author

**Ramdular Yadav**
AI Fellow @ Fusemachines




