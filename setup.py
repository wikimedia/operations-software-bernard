from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bernard",
    description="bernard",
    version="0.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=("api_db", "web_app"),
    entry_points={
        "console_scripts": [
            "start_api_db = api_db.app:main",
            "start_web_app = web_app.app:main"
        ]
    },
    test_suite="api_db.test",
)
