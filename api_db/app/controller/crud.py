from app.db import DatabaseConnection
from app.config import app_config
from app.config import config_loader


async def get_recent_backups():
    global_config = app_config.get_settings()
    backup_sections = config_loader.get_alerting_hosts(global_config.ALERTING_HOST_FILE)
    final_res = []
    for section in backup_sections:
        for backup_type in backup_sections[section]:
            for backup_source in backup_sections[section][backup_type]:
                query = """
                           SELECT id, name, status, source, host, type, section, start_date, end_date, total_size
                           FROM backups b
                           WHERE b.start_date =
                           (
                            SELECT MAX(start_date) FROM backups b2 where b2.section =:section_e1
                            AND b2.source LIKE :datacenter_e1
                            AND b2.type=:type
                            AND b2.status = 'finished'
                           )
                           AND b.section =:section_e2
                           AND b.source LIKE :datacenter_e2
                        """
                # append like % parameter to backup_source
                backup_source = "%" + backup_source + "%"

                # Normally, we don't need duplicates for section and datacenter, however we do it as otherwise SQLite
                # tests will cause an error for some reason
                values = {'section_e1': section, 'datacenter_e1': backup_source, 'type': backup_type,
                          'section_e2': section, 'datacenter_e2': backup_source}
                res = await DatabaseConnection.instance().database.fetch_one(query=query, values=values)
                if res:
                    final_res.append(res)
    return final_res

async def get_backup_data_by_section(section):
    pass



async def readiness_check():
    # Our definition of readiness is that it is able to query the database and get some rows of data
    query = """
               SELECT id, name, status, source, host, type, section, start_date, end_date, total_size 
               FROM backups b 
               WHERE b.start_date = (
                   SELECT MAX(start_date)
                   FROM backups b2
                   WHERE b2.section = b.section
               )
            """
    return await DatabaseConnection.instance().database.fetch_all(query=query)


# TODO
async def get_stale_backups():
    pass


# TODO
async def get_sections_with_no_recent_backups():
    pass
