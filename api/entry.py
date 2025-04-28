import uvicorn
import tempfile
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.handlers import data_handler, llm_handler
from api.security import verify_api_key
from api.utils import format_response  # Import the utility function

app = FastAPI()

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return format_response(data=None, message=exc.detail, success=False, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return format_response(data=None, message="Validation error", success=False, status_code=422)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return format_response(data=None, message="Internal server error", success=False, status_code=500)

@app.get("/test")
async def test(api_key: str = Depends(verify_api_key)):
    return format_response(data={"message": "You are authorized to access this data!"}, message="Authorization successful")

@app.post("/upload")
async def upload_session_ppt(material_code: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".pptx"):
        return format_response(data=None, message="Only .pptx files are supported", success=False, status_code=400)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        data_handler.handle_session_ppt(material_code, temp_file_path)
        return format_response(data={"file_path": temp_file_path}, message="File processed successfully")

    except Exception as e:
        return format_response(data=None, message=f"Error processing file: {str(e)}", success=False, status_code=500)

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/ask")
async def ask_chatbot(question: str, chat_id: str):
    chat_id = chat_id.strip()
    try:
        response = llm_handler.ask_question(question, chat_id)
        return format_response(data={"response": response}, message="Question processed successfully")
    except Exception as e:
        return format_response(data=None, message=f"Error getting question from LLM: {str(e)}", success=False, status_code=500)

def start_api():
    uvicorn.run(app, host="127.0.0.1", port=8000)
