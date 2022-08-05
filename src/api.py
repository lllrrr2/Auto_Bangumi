import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging

from core import APIProcess
from dataset import *
from conf import settings
from utils import json_config

logger = logging.getLogger(__name__)
app = FastAPI()
api_func = APIProcess()

origins = [
    "http://localhost",
    "http://localhost:7892",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


# HTML
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


# Main page info
@app.get("/api/v1/info/Rules")
def get_all_rules() -> list:
    return api_func.get_all_rules()


@app.get("/api/v1/info/Log")
async def get_log():
    log_path = settings.log_path
    return FileResponse(log_path)


@app.get("/api/v1/info/Config")
def get_config():
    return json_config.load(settings.config_path)


# Set config
@app.post("/api/v1/set/Config")
def set_config(config: SetConf):
    api_func.set_config(config)
    return "Success"


# Change Rule settings.config
@app.post("/api/v1/set/Rule")
def change_rule(rule: ChangeRule):
    api_func.change_rule(rule)
    return "Success"


# Delete rule
@app.get("/api/v1/set/removeRule/{id}")
def remove_rule(id: str):
    return api_func.remove_rule(id)


@app.get("/api/v1/set/resetRule")
def reset_rule():
    return api_func.reset_rule()


@app.post("/api/v1/add/Collection")
async def collection(link: RssLink):
    return api_func.download_collection(link.rss_link)


@app.post("/api/v1/add/Subscribe")
async def subscribe(link: RssLink):
    return api_func.add_subscribe(link.rss_link)


@app.post("/api/v1/add/Rule")
async def add_rule(info: AddRule):
    return api_func.add_rule(info.title, info.season)


def run():
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "[%(asctime)s] %(levelprefix)s %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=settings.config.webui_port)


if __name__ == "__main__":
    run()

