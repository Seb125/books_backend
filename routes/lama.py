from fastapi import APIRouter, Depends, HTTPException, status
import json
from llamaapi import LlamaAPI
from model import Request
import os
from auth import get_current_active_user;
from typing import Annotated
from model import User


router = APIRouter()

@router.get("/test")
def test():
    return {"message": "test"}

@router.post("/lama")
def api_request(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    print("here")
    # Initialize the SDK
    llama = LlamaAPI(os.getenv("API_KEY"))
    # prepare chat history for API request
    
    myFormattedList = [{"role": "user" if msg.role == "ME" else "assistant", "content": msg.msg} for msg in request.message]
    print(myFormattedList)
    # Build the API request
    api_request_json = {
        "messages": myFormattedList,
        "stream": False,
        "function_call": "get_current_weather",
        "response_format": {
        "title": "string",
        "author": "string",
        "abstract": "string"
    }
    }
    

    # Execute the Request
    try:
        response = llama.run(api_request_json)
        formatted_response = response.json()
        print(json.dumps(response.json(), indent=2))
        return {"answer": formatted_response}
    except Exception as e:
        print(f"An error occurred during the Llama request: {e}")

    #print(json.dumps(response.json(), indent=2))