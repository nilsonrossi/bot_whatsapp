import logging

import uvicorn
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from clients.whatsapp.whatapp_client import WhatsAppClient
from models.webhook_message_model import WebhookMessageModel
from schema import Message
from services.loro_service import LoroService
from services.nirsu_service import NirsuService
from settings import settings

logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)


def create_app() -> FastAPI:
    app = FastAPI(title="BOT API", docs_url="/docs", openapi_url="/openapi.json")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(exc.detail)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(exc.body)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.post("/loro/new_message")
async def twilio_new_message(form_data: Message = Depends()):
    LoroService(form_data).process_message()
    return form_data


@app.post("/nirsu/new_message")
async def whatsapp_new_message(message: WebhookMessageModel):
    print(message.dict())
    whatsapp_client = WhatsAppClient(settings.WHATSAPP_PHONE_NUMBER_ID)
    NirsuService(message, whatsapp_client).process_message()
    return {"success": True}


@app.get("/nirsu/new_message")
async def verify_endpoint(request: Request):
    if request.query_params.get("hub.verify_token") == settings.WHATSAPP_VERIFY_TOKEN:
        logging.info("Verified webhook")
        return Response(request.query_params.get("hub.challenge"))
    return Response("Invalid verification token", 400)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
