import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from chat_agent import chain

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    # Save the uploaded file to disk
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Pass the file path to the agent chain
    try:
        result = chain.invoke({
            "input": file_location,
            "agent_scratchpad": [],
            "chat_history": []
        })
        # Optionally, remove the file after processing
        os.remove(file_location)
        return JSONResponse(content={"result": result})
    except Exception as e:
        # Clean up file if error occurs
        if os.path.exists(file_location):
            os.remove(file_location)
        return JSONResponse(content={"error": str(e)}, status_code=500)