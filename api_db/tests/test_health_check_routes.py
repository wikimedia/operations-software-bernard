def test_readiness_probe_ok_message(test_app):
    # Our definition of "ready" -- whether or not the app can successfuly connect to the database and retrieve data
    # TODO add database connection
    response = test_app.get("/health_check/readiness")
    assert response.status_code == 200
    assert response.json() == {"probe": "readiness", "status": "ok"}


def test_liveness_probe_ok_message(test_app):
    # Our definition of "alive" is whether the app is responding to any requests
    response = test_app.get("/health_check/liveness")
    assert response.status_code == 200
    assert response.json() == {"probe": "liveness", "status": "ok"}
