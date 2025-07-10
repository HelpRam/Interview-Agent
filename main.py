import json
from chat_agent import chain

def run_chain(file_path, label=""):
    print(f"\n--- Running Chain on {label} ---")
    try:
        result = chain.invoke({
            "input": file_path,           # Pass the file path directly!
            "agent_scratchpad": [],
            "chat_history": []
        })
        print(f"\n--- Chain Output on {label} ---")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error running chain on {label}: {e}")

if __name__ == "__main__":
    file_path = input("Provide the path to your document (resume or job description): ").strip()
    if file_path:
        run_chain(file_path, label=file_path)