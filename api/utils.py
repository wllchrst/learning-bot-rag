from fastapi.responses import JSONResponse

def format_response(data=None, message="", success=True, status_code=200):
    return JSONResponse(
        content={
            "data": data,
            "message": message,
            "success": success
        },
        status_code=status_code
    )
