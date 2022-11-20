##### Quick summary
Challenge assignment for Morotech senior python engineer role

#####  Challenge description
Here at MoroTech we are always looking for ways to expand our general knowledge. A way to do this is
by reading books! There is a problem though, it�s very difficult to know whether a book is good or not
before reading it. So, we decided to create a book rating system! As part of this exercise you will create a
simple API that will help us rate and review the books we have read. You will be able to use your
technologies of choice to achieve this, unless otherwise explicitly stated.

#####  Stack 
* fastAPI web framework
* sqlite3 database

##### Docker installation and run (tests and server)
* `docker build -t morotechgutendex .`
* `docker run -d -p 9999:9999 morotechgutendex`
* Docker container will firstly run the automated tests and then deploy the web app
* Access the API at `localhost:9999/v1/`
* Access the API documentation at `localhost:9999/v1/documentation`


#####  Native installation and run (tests and server)
* Use an environment with `python3` installed
* Open a terminal and navigate to project's main folder
* Create a python virtual environment by running the following command:
`python3.9 -m venv python_venv`
* Activate the python virtual environment by running the command:
`source python_venv/bin/activate`
* Install requirements of testing environment by running the following command:
`pip3 install -r testing_requirements.txt`
* Install requirements of app by running the following command:
`pip3 install -r requirements.txt`
* Run the automated tests by invoking the `pytest` utility by running the following command:
`pytest --html=morotech_gutendex_api_report.html`
* When the test suite has been completed you can see the results by in the html report that has been generated at the same folder named `morotech_gutendex_api_report.html`
*  Run the server `python3 src/main.py`
*  Access the API at `localhost:9999/v1`
*  Access the API documentation at `localhost:9999/v1/documentation`





`
NOTE:
If the test suite has ran before, make sure to delete the derived sqlite3db named "books_reviews.db",
which in that case would be present in the same folder, so that the tests are not affected by any previous inserted records
`

#
#####  Who do I talk to  
* christos.karvouniaris247@gmail.com