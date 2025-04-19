import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from utils.outlook_calendar import create_out_of_office_event, set_automatic_replies
from utils.outlook_auth import get_access_token
import datetime
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Outlook Calendar API!"}

@app.get("/.well-known/a2a.json")
def a2a_metadata():
    return {
        "id": "outlook-calendar-agent",
        "name": "Outlook Out of Office Setter",
        "description": "Creates Outlook calendar events and sets automatic replies based on date input from ticket.",
        "capabilities": ["create_out_of_office"]
    }

@app.post("/webhook")
async def webhook_handler(request: Request):
    payload = await request.json()
    action = payload.get("action")

    if action == "create_out_of_office":
        try:
            email = payload["email"]
            start_time = payload["from"]
            end_time = payload["to"]
            subject = payload["subject"]

            access_token = get_access_token()  # Obtain access token

            result = create_out_of_office_event(email, start_time, end_time, subject, access_token)
            set_automatic_replies(email, start_time, end_time, access_token)
            
            return {"status": "success", "detail": result}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Unsupported action.")

def main(req: func.HttpRequest) -> func.HttpResponse:
    # This converts the FastAPI app to be run by Azure Functions
    from fastapi import FastAPI
    from starlette.middleware.wsgi import WSGIMiddleware
    from .function_app import app as fastapi_app
    return func.AsgiMiddleware(fastapi_app).handle(req)
