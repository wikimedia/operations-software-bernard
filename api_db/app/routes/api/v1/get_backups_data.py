from fastapi import APIRouter, HTTPException
from app.config import app_config, config_loader
from app.controller import crud
from datetime import datetime

router = APIRouter()


@router.get("/api/v1/backups/recent/all")
async def get_recent_backups_data():
    return await crud.get_recent_backups()


# TODO
@router.get("/api/v1/backups/recent/{section}")
async def get_backups_data_by_section(section: str):
    # Check max length
    max_length = 32
    if len(section) > max_length:
        error_message = "Parameter too long - Size limit of " \
                        + str(max_length) \
                        + " characters reached for Section"
        raise HTTPException(status_code=500, detail=error_message)

    # Check if any uppercase
    if any(character.isupper() for character in section):
        error_message = "Parameter cannot contain uppercase letters"
        raise HTTPException(status_code=500, detail=error_message)

    # Check if section exist in YAML file
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_alerting_hosts(global_config.ALERTING_HOST_FILE)
    if section not in backup_sections:
        error_message = "Section " \
                        + str(section) \
                        + " does not exist"
        raise HTTPException(status_code=404, detail=error_message)

    return await crud.get_backup_data_by_section(section)


@router.get("/api/v1/backups/datacenters/all")
async def get_all_datacenters():
    unique_datacenters = []
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_alerting_hosts(global_config.ALERTING_HOST_FILE)
    for section in backup_sections:
        for backup_type in backup_sections[section]:
            for datacenter in backup_sections[section][backup_type]:
                if datacenter not in unique_datacenters:
                    unique_datacenters.append(datacenter)
    return unique_datacenters


@router.get("/api/v1/backups/types/all")
async def get_all_backup_types():
    unique_types = []
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_alerting_hosts(global_config.ALERTING_HOST_FILE)
    for section in backup_sections:
        for backup_type in backup_sections[section]:
            if backup_type not in unique_types:
                unique_types.append(backup_type)
    return unique_types


@router.get("/api/v1/backups/sections/all")
async def get_all_section_types():
    unique_sections = []
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_alerting_hosts(global_config.ALERTING_HOST_FILE)
    for section in backup_sections:
        if section not in unique_sections:
            unique_sections.append(section)
    return unique_sections


@router.get("/api/v1/backups/check/freshness/all")
async def check_all_backup_freshness():
    results = []
    recent_backups = await crud.get_recent_backups()
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_freshness_config(global_config.ALERTING_HOST_FILE)
    max_freshness_dump = backup_sections['dump']
    max_freshness_snapshot = backup_sections['snapshot']

    for backup in recent_backups:
        section = backup['section']
        backup_type = backup['type']
        # An assumption is made on datacenter format
        datacenter = backup['source'].split('.')[1]
        end_date = backup['end_date']
        if type(end_date) != str:
            end_date_string = end_date.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            end_date_string = end_date
            end_date = datetime.strptime(end_date_string, '%Y-%m-%d %H:%M:%S')

        time_delta = datetime.now() - end_date
        time_delta_string = "{d} days, {h} hours, {m} minutes ago".format(d=time_delta.days,
                                                                          h=time_delta.seconds // 3600,
                                                                          m=time_delta.seconds % 3600 // 60)

        freshness_fail = False
        if backup_type == "snapshot":
            if time_delta.total_seconds() > max_freshness_snapshot:
                freshness_fail = True

        elif backup_type == "dump":
            if time_delta.total_seconds() > max_freshness_dump:
                freshness_fail = True
        if freshness_fail:
            results.append({"section": section,
                            "freshness": "fail",
                            "type": backup_type,
                            "datacenter": datacenter,
                            "last_backed_up": end_date_string,
                            "ago": time_delta_string})
        else:
            results.append({"section": section,
                            "freshness": "ok",
                            "type": backup_type,
                            "datacenter": datacenter,
                            "last_backed_up": end_date_string,
                            "ago": time_delta_string})

    return results
