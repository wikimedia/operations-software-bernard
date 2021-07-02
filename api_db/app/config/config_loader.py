import yaml

ALERTING_HOST_PROFILE = "profile::dbbackups::check::backups"
FRESHNESS_HOST_PROFILE = "profile::dbbackups::check::freshness"


def get_alerting_host_config(file):
    with open(file) as opened_file:
        alerting_host_config = yaml.safe_load(opened_file)
        return alerting_host_config


def get_freshness_config(file):
    freshness = get_alerting_host_config(file)[FRESHNESS_HOST_PROFILE]
    return freshness


def get_alerting_hosts(file):
    alerting_hosts = get_alerting_host_config(file)[ALERTING_HOST_PROFILE]
    return alerting_hosts
