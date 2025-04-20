import uvicorn
import tempfile
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from api.handlers import data_handler, llm_handler
from api.security import api_key_header, verify_api_key

app = FastAPI()

@app.get("/test")
async def test(api_key: str = Depends(verify_api_key)):
    return {"message": "You are authorized to access this data!"}

@app.post("/upload")
async def upload_session_ppt(material_code: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".pptx"):
        raise HTTPException(status_code=400, detail="Only .pptx files are supported")

    try:
        # Create a temporary file and keep it until processing is done
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name  # Store path before closing
            
        data_handler.handle_session_ppt(material_code, temp_file_path)
        return {"message": "Success reading file"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    finally:
        # Ensure the temporary file is deleted after use
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/ask")
async def ask_chatbot(question: str, chat_id: str):
    chat_id = chat_id.strip()
    try:
        response = llm_handler.ask_question(question, chat_id)
        return {'response': response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting question from LLM: {str(e)}")

def start_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)
