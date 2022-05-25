# :dog: Bernard - a database backups monitoring dashboard

This is the repository that will be used for the codebase of Bernard 
(back-end API and front-end app)

This application is written in Python and works well with version 3.7, using FastAPI as backend
This application consists of two components, api_db and web_app

api_db is the component that interacts with the database 
(using MySQL or SQLite or Postgres)
and exposes the databases metadata through API endpoints

web_app is the component that interacts with api_db and presents 
the data in HTML using Jinja2

## Quick start - running it locally

### Setting up api_db

You must have Python version 3.7 or higher installed on your machine as a 
prerequisite. 

- Clone this repository using the following command

`git clone https://github.com/wikimedia/operations-software-bernard`

- Install all the libraries present in all the requirements files 
(assuming you are in the same directory as the cloned repo)

`pip3 install -r test-requirements.txt`

This file contains all the libraries used for the unit tests, and therefore should 
contain all the dependancies

We need to run api_db first. This requires a few environment variables

- Set the following environment variables (different ways to do it, depending on your OS)

`ENV=dev`

This uses the dev configuration, which lets you set the following parameters

`DB_URI=sqlite:///tests/test.db`

This lets you use the sample data from the unit tests. This can be used to run it

If you are using MariaDB/MYSQL, use the following example 
`DB_URI=mysql:///username:pass@127.0.0.1:3306/databasename`

Replace username, pass, IP address and databasename with that of your instance

Please ensure the database has a table called backups, as described in the file below

https://phabricator.wikimedia.org/diffusion/OSWB/browse/master/sql/dbbackups.sql

After the environment variables have been set, run the following command to 
start api_db. Assuming that you have cd'ed into the api_db directory, run the following

`python3 -m app.main`

This should start the application on local port 8282. This port is hardcoded, it can be changed in app/app.py
on the first line.

To obtain API documentation, follow this URL after starting api_db
`http://localhost:8282/docs`

This should provide you a page with all the APIs for the program.

Example

`api/v1/backups/check/freshness/all` should provide the freshness data for all the 
recent backups

If the API returns a response, well done, api_db is working

### Setting up web_app

Assuming you have already followed the instructions above

- In web_app, copy the folder named `static` into app. This is to avoid any path issues
caused by different OS. (Both Windows and Unix behave in a different way)

- Also copy the folder called `templates` from the root folder into app/routes as well.

While keeping api_db running, and using the same environment variables,
execute the following command to run web_app
Assuming you have cd'ed into web_app directory, run

`python3 -m app.main`

If you get an error like /static not mounted or /template not found, check that you have followed
the steps above to copy the templates and static files from the root folder.

The python application should start on port 8181. The default dev configuration connects to the
api_db host on http://localhost:8282. This can be changed by using `ENV=prod` and then supplying 
the environment variables `API_URL=<url here, without / at end>`

Navigate to `http://localhost:8181` to see the homepage



## Quick start - running it on WMF Cloud

- Create the following instances

app-vm (This virtual machine will host our applications, 
both api_db and web_app)

db1 (For MariaDB database)

- Set up MariaDB on db1 instance with SQL data as detailed here
https://phabricator.wikimedia.org/diffusion/OSWB/browse/master/sql/dbbackups.sql

- Create an account with READ only privileges for the table `backups`

- Set up Security groups to allow connections from app-vm to db1 MariaDB SQL port

- Following the same instructions as for running locally, ssh into app-vm and set up the applications.
Set the ENV var for DB_URI to your MariaDB host. 

At the time of writing, the application can be tested under the following internet accessible FQDNs

https://app-bernard.wmcloud.org - Dashboard

https://api-bernard.wmcloud.org/docs - API_DB Docs



