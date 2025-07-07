import os
import json
from dotenv import load_dotenv
from main import extract_text_from_pdf

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Import your custom tools 
from pipeline.tools.jd_tool import JDExtractorTool
from pipeline.tools.resume_tool import ResumeExtractorTool



# --- Tool Setup ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Tool Binding
tools = [JDExtractorTool(), ResumeExtractorTool()]


# create a prompt template for the agent
prompt  = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI assistant that specializes in identifying documents types."
                   "You have access to tools that can identify if a document is a Job Description or a Resume."
                   "Your goal is to use the correct tool to classify the input text."
                   "You will return the structured information extracted from the document as a JSON string."),
    
            ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),

    ]
)

# Create the agent
agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent = agent,
    tools = tools,
    verbose=True

)

pdf_text = extract_text_from_pdf("Dataset\\Ram_Resume_DS.pdf")  # Make sure to provide the correct path
result = agent_executor.invoke({"input": pdf_text})
print(result)
