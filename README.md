### What is it?

It is simple wsgi lib, just for experience.


### Technology

Python 3.6

requests, parse, pytest, click


### Plan
| # | Task | Estimate | Progress |
| ------------ | ------------ | ------------ | ------------ |
| 1 | Read [PEP3333](https://www.python.org/dev/peps/pep-3333/) for refreshing in mind | 2h | DONE |
| 2 | Design: wsgi, app, tests. Select the tools and dependencies | 3h | DONE |
| 3 | Create project and prepare environment | 2h | DONE |
| 4 | Implement server/gateway side + tests | 8h  | DONE |
| 5 | Implement application/framework side + tests | 8h | DONE |
| 6 | Improve server side + tests | 3h | DONE |
| 7 | Implement routing + tests | 5h | DONE |
| 8 | Write documentation | 2h | DONE |
| 9 | Create demo application which use implemented wsgi | 3h | DONE |


### Install

    git clone git@github.com:robin0371/mywsgi.git
    cd mywsgi
    activate env
    pip install -r requirements.txt


### Tests

    cd mywsgi
    activate env
    pytest  --mypy --mypy-ignore-missing-imports --cov=mywsgi/


### Demo application

*Notes:*
- Demo application located in example package
- App has three endpoints:
    * / - index
    * /get/{param} - endpoint with named param, returns string
    * /json/{param} - endpoint with named param, returns json

##### Launch

    cd path/to/mywsgi
    activate env
    python mywsgi/__main__.py example.__init__:app 127.0.0.1 8091

this command will start demo-application on localhost:8091

##### Using

1. curl -X GET http://localhost:8091/ -H 'Host: localhost:8091' - should return "index" as string
2. curl -X GET http://localhost:8091/get/555 -H 'Host: localhost:8091' - should return 555 (or requested) as string
3. curl -X GET http://localhost:8091/json/555 -H 'Host: localhost:8091' - should return {"p": 555} (or requested) as json
