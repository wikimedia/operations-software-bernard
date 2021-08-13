from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.util.helper import make_api_call
from fastapi.templating import Jinja2Templates
from app.config import app_config

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    global_config = app_config.get_settings()
    sections_api_url = global_config.SECTIONS_API_ENDPOINT
    datacenters_api_url = global_config.DATACENTERS_API_ENDPOINT
    freshness_check_api_url = global_config.FRESHNESS_CHECK_API_ENDPOINT
    sections, types, datacenters, freshness_results, recent_backups = [], [], [], [], []

    # API calls to our endpoints
    freshness_results = await make_api_call(freshness_check_api_url)
    datacenters = await make_api_call(datacenters_api_url)
    sections = await make_api_call(sections_api_url)

    return templates.TemplateResponse("main_dashboard.html",
                                      {"request": request,
                                       "sections": sections,
                                       "datacenters": datacenters,
                                       "types": types,
                                       "results": freshness_results})
