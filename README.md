# Casting Agency Company

###description
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

#####Code Style
This project adheres to the python [PEP8](https://www.python.org/dev/peps/pep-0008/) Coding guidelines.


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. 
This keeps our dependencies for each project separate and organaized.
Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

####Local Deployment & Testing
Once all the dependencies are installed next we need to set up the database.
This project uses `Postgresql` database

Run below command on database terminal to create application database:
```
CREATE DATABASE <DATABASE_NAME>;
```

## Running the server

From  the `project` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --reload
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs file to find the application.

## Testing
Run the below command to test the application
Note: Remember to update the test db urls in setup.sh file
```
pytest castingagency_tests.py
```
## Live Server
Below the url for the Heroku deployed application.
```
URL Goes Here
```

## API Reference
- **Base URL**: At present this app can only be run locally. The backend app is hosted at the 
default, ```http://127.0.0.1:5000/```, which is set as a proxy to front end configuration.
- **Authentication**: This version of the application require jwt authentication or Bearer Tokens.

### Error Handling
Error handling are returned as JSON Objects in the below mentioned format.
```
{
  "error": 404,
  "message": "Request resource not found",
  "success": false
}
```
The API will return 3 types of error if request fails / for invalid requests:
- 404: Not Found
- 422: Unprocessable Entity
- 400: Bad Request

### Roles and Permissions
APIs in this project uses below roles and permissions
#####Roles:
- Casting Assistant
    - Can view actors and movies
- Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
- Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database

#####Permissions
|Permission|Permission details|
|----------|------------------|
|add:actors| Permission to add Actors|
|add:movie| Permission to add Movies|
|delete:actors| Permission to delete Actors|
|delete:movie| Permission to delete Movies|
|get:actors| Permission to get Actor details|
|get:movie| Permission to get Movie details|
|modify:actors|Permission to update Actor details|
|modify:movie|Permission to update Movie details|

### API Endpoints

#### GET /status & /health
- General: Return application health or status to check application is up and running
- Sample: ```curl http://127.0.0.1:8080/status```
            ```curl http://127.0.0.1:8080/health```
######Response           
```
{
    "message": "Welcome to Casting Agency"
}
```

#### GET /actors
- General: Return list of all actors
- Sample: 
```
curl --location --request GET 'http://127.0.0.1:8080/actors' --header 'Authorization: Bearer <auth_token>'
```

###### Sample Response           
```
{
    "actors": [
        {
            "age": 23,
            "gender": "Male",
            "id": 2,
            "identifier": "d184c618-f9e8-4176-ac7b-64016f54fd29",
            "name": "Ravi Kumar"
        }
    ],
    "page": 1,
    "success": true
}
```

#### GET /actors/<actor_id>
- General: Return actor information
- Sample: 
```
curl --location --request GET 'http://127.0.0.1:8080/actors/actor_id' --header 'Authorization: Bearer <auth_token>'
```

###### Sample Response           
```
{
    "actor_details": {
        "age": 23,
        "gender": "Male",
        "id": 2,
        "identifier": "d184c618-f9e8-4176-ac7b-64016f54fd29",
        "name": "Ravi Kumar"
    },
    "success": true
}
```

#### GET /movies
- General: Return list of all movies
- Sample: 
```
curl --location --request GET 'http://127.0.0.1:8080/movies' --header 'Authorization: Bearer <auth_token>'
```

###### Sample Response           
```
{
    "actors": [
        {
            "id": 1,
            "identifier": "72009062-8825-4f92-8609-af943addf905",
            "ott_partner": "Hotstar",
            "production_house": "RK Productions",
            "release_date": "29/06/2020",
            "title": "Ek Tha Tiger"
        }
    ],
    "page": 1,
    "success": true
}
```

#### GET /actors/<actor_id>
- General: Return movie information
- Sample: 
```
curl --location --request GET 'http://127.0.0.1:8080/movies/movie_id' --header 'Authorization: Bearer <auth_token>'
```

###### Sample Response           
```
{
    "movie_details": {
        "id": 1,
        "identifier": "72009062-8825-4f92-8609-af943addf905",
        "ott_partner": "Hotstar",
        "production_house": "RK Productions",
        "release_date": "29/06/2020",
        "title": "Ek Tha Tiger"
    },
    "success": true
}
```
#### POST /actors
- General: Create a actor
- Sample: 
```
curl --location --request POST 'http://127.0.0.1:8080/actors' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json' --data-raw '{"name": "Ravi Kumar","age": 45,"gender": "male"}'
```

###### Sample Response           
```
{
    "id": 15,
    "identifier": "03058ee9-ed35-449a-ab2e-835946058878",
    "success": true
}
```

#### POST /movies
- General: Create a Movie
- Sample: 
```
curl --location --request POST 'http://127.0.0.1:8080/movies' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json' --data-raw '{"title": "Ek Tha Tiger","release_date": "29/06/2020", "production_house": "RK Productions","ott_partner": "Hotstar"}'
```

###### Sample Response           
```
{
    "id": 3,
    "identifier": "2381d27e-0437-42d5-ab33-fab93e54e232",
    "success": true
}
```

#### DELETE /actors/<actor_id>
- General: Create a actor
- Sample: 
```
curl --location --request DELETE 'http://127.0.0.1:8080/actors/<actor_id>' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json'
```

###### Sample Response           
```
{
    "actor_id": 13,
    "status": "Deleted",
    "success": true
}
```

#### DELETE /movies/<movie_id>
- General: Delete a Movie
- Sample: 
```
curl --location --request DELETE 'http://127.0.0.1:8080/movies/<movie_id>' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json'
```

###### Sample Response           
```
{
    "movie_id": 3,
    "status": "Deleted",
    "success": true
}
```
        
#### PATCH /actors/<actor_id>
- General: Update a actor information
- Sample: 
```
curl --location --request PATCH 'http://127.0.0.1:8080/actors/<actor_id>' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json' --data-raw '{"name": "Ravi Kumar"}'
```

###### Sample Response           
```
{
   "success": True,
    "actor_id": 1
}
```

#### PATCH /movies/<movie_id>
- General: Delete a Movie
- Sample: 
```
curl --location --request PATCH 'http://127.0.0.1:8080/movies/<movie_id>' --header 'Authorization: Bearer <auth_token>' --header 'Content-Type: application/json --data-raw '{"name": "Ravi Kumar"}'
```

###### Sample Response           
```
{
    "movie_id": 3,
    "status": "Deleted",
    "success": true
}
```

