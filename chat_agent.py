import os
import json
from dotenv import load_dotenv

# LangChain imports
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser

# Custom tools
from pipeline.tools.jd_tool import JDExtractorTool
from pipeline.tools.resume_tool import ResumeExtractorTool
from pipeline.tools.parsing_engine import ParsingTool

# --------------------- Environment Setup ---------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --------------------- LLM Initialization ---------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# --------------------- Tool Binding ---------------------
tools = [ParsingTool(),JDExtractorTool(), ResumeExtractorTool()]

# --------------------- Prompt Template ---------------------
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an AI assistant that determines whether a given text is a resume or a job description.\n"
     "You have access to two tools: one for resumes and one for job descriptions.\n"
     "Once the correct tool is selected, the full text will be passed to it.\n"
     "Your goal is to extract structured data in JSON format.\n\n"
     "If it's a **resume**, extract: name, contact info, education, skills, experience, certifications, projects, and summary.\n"
     "If it's a **job description**, extract: job title, required skills, soft skills, degree, certifications, experience, and tools/platforms.\n\n"
     "**Important:** Return only the JSON object. Do not include markdown (```json), explanations, or extra text."
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# --------------------- Agent Setup ---------------------
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# --------------------- Agent Executor ---------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Output Parser 
parser = JsonOutputParser()
extract_output = RunnableLambda(lambda x: x["output"])

# Chain 
chain = agent_executor | extract_output | parser


