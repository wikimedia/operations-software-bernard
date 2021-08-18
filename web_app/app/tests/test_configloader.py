import os
from app.config import app_config
from app.config.app_config import ConfigException


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
