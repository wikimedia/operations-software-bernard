import json
import freezegun
from tests.test_data.get_recent_backups_response import RECENT_BACKUPS_EXPECTED_RESPONSE
from tests.test_data.freshness_check_response import FRESHNESS_CHECK_RESPONSE, FRESHNESS_CHECK_FAIL_RESPONSE


def test_get_recent_apps(test_app):
    response = test_app.get("/api/v1/get_recent_backups_data")
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == RECENT_BACKUPS_EXPECTED_RESPONSE


def test_get_all_datacenters(test_app):
    response = test_app.get("/api/v1/backups/datacenters/all")
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == ['eqiad', 'codfw']


def test_get_all_sections(test_app):
    response = test_app.get("/api/v1/backups/sections/all")
    response_json = json.loads(response.text)
    print(response_json)
    assert response.status_code == 200
    assert response_json == ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',
                             'x1', 'es4', 'es5', 'm1', 'm2', 'm3', 'm5',
                             'zarcillo', 'matomo', 'analytics_meta']


@freezegun.freeze_time("2021-06-03")
def test_freshness_check_passes(test_app):
    response = test_app.get("/api/v1/backups/check/freshness/all")
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == FRESHNESS_CHECK_RESPONSE


@freezegun.freeze_time("2021-07-14")
def test_freshness_check_fails(test_app):
    response = test_app.get("/api/v1/backups/check/freshness/all")
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == FRESHNESS_CHECK_FAIL_RESPONSE


def test_get_all_backup_types(test_app):
    response = test_app.get("/api/v1/backups/types/all")
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json == ['dump', 'snapshot']
