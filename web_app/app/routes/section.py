from fastapi import APIRouter, Request
from app.util.helper import make_api_call
from fastapi.templating import Jinja2Templates
from app.config import app_config
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="/templates")


@router.get("/sections/{section}")
async def show_dashboard(request: Request, section: str):
    global_config = app_config.get_settings()
    sections_api_url = global_config.SECTIONS_API_ENDPOINT
    datacenters_api_url = global_config.DATACENTERS_API_ENDPOINT
    freshness_check_api_url = global_config.FRESHNESS_CHECK_API_ENDPOINT
    sections, types, datacenters, freshness_results = [], [], [], []

    # API calls to our endpoints
    freshness_results = await make_api_call(freshness_check_api_url)
    datacenters = await make_api_call(datacenters_api_url)
    sections = await make_api_call(sections_api_url)
    section_result = [result for result in freshness_results if result['section'] == section]

    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    types = ["snapshot", "dump"]  # TODO get this from an API
    if section not in sections:
        return {"error": "This section does not exist or is not monitored"}
    return templates.TemplateResponse("section.html",
                                      {"request": request,
                                       "section": section,
                                       "results": freshness_results,
                                       "datacenters": datacenters,
                                       "types": types,
                                       "section_result": section_result,
                                       "system_time": current_time})
