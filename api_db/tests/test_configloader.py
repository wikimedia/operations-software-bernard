import os
from app.config import app_config
from app.config.config_loader import get_freshness_config, get_alerting_host_config
from app.config.app_config import ConfigException
from tests.test_data.host_config_yaml_data import DBBACKUPS_PROFILE_TEST_DATA, DBBACKUPS_FRESHNESS_TEST_DATA


def test_config_loader_throws_exception_when_env_not_present():
    os.environ["ENV"] = ""
    error = False
    try:
        test_config = app_config.get_settings()
        print(test_config)
    except ConfigException:
        error = True

    assert error


def test_config_loader_throws_exception_when_env_is_invalid():
    os.environ["ENV"] = "t3st"
    error = False
    try:
        test_config = app_config.get_settings()
        print(test_config)
    except ConfigException:
        error = True

    assert error


def test_config_loader_loads_test_env_from_env_var():
    os.environ["ENV"] = "test"
    error = False
    try:
        test_config = app_config.get_settings()
        print()
        print(test_config)
    except ConfigException:
        error = True

    assert not error


def test_config_contains_correct_parameters():
    os.environ["ENV"] = "test"
    error = False
    try:
        test_config = app_config.get_settings()
        print(test_config)
    except ConfigException:
        error = True

    assert not error


def test_config_loader_loads_freshness_config_correctly():
    os.environ["ENV"] = "test"
    expected_output = DBBACKUPS_FRESHNESS_TEST_DATA
    test_config = app_config.get_settings()
    freshness_config = get_freshness_config(test_config.ALERTING_HOST_FILE)
    assert freshness_config == expected_output


def test_config_loader_loads_hosts_config_correctly():
    os.environ["ENV"] = "test"
    expected_config_profile_backup = 'profile::dbbackups::check::backups'
    expected_config_profile_freshness = 'profile::dbbackups::check::freshness'

    test_config = app_config.get_settings()
    configs = get_alerting_host_config(test_config.ALERTING_HOST_FILE)
    for config in configs:
        if expected_config_profile_freshness in config:
            assert expected_config_profile_freshness == config
            assert configs[config] == DBBACKUPS_FRESHNESS_TEST_DATA
        elif expected_config_profile_backup in config:
            assert expected_config_profile_backup == config
            assert configs[config] == DBBACKUPS_PROFILE_TEST_DATA
        else:
            raise Exception('Either freshness or backup profile were missing from configs')
