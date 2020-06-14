import unittest
from app import app
from models.dbmodel import setup_db, db_drop_and_create_all, db, Actor, Movie
import json
import os
from faker import Faker
import random
import app_utils

# for cloud deployments - change test_db_url in setup.sh file.
DATABASE_PATH = os.getenv("TEST_DB_URL")
PRODUCER_TOKEN = os.getenv("PRODUCER_TOKEN")
DIRECTOR_TOKEN = os.getenv("DIRECTOR_TOKEN")
ASSISTANT_TOKEN = os.getenv("ASSISTANT_TOKEN")

fake = Faker()


class CastingAgencyTestCase(unittest.TestCase):
    '''This class includes test cases for testing endpoints'''

    def prepare_test_bed(self):
        for i in range(5):
            actor = Actor(name=fake.name(), gender=app_utils.get_gender_char(),
                          age=random.randint(18, 99),
                          identifier=app_utils.generate_guid())
            actor.insert()

        movie = Movie(title="Avengers", identifier=app_utils.generate_guid(),
                      release_date=app_utils.get_datetime("29/06/2020"),
                      production_house="Marvel Studios",
                      ott_partner="Hotstar Disney+")
        movie1 = Movie(title="Aquaman", identifier=app_utils.generate_guid(),
                       release_date=app_utils.get_datetime("29/06/2021"),
                       production_house="DC",
                       ott_partner="Prime Video")
        movie2 = Movie(title="Avengers EndGame", identifier=app_utils.generate_guid(),
                       release_date=app_utils.get_datetime("29/06/2022"),
                       production_house="Marvel Studios",
                       ott_partner="Hotstar Disney+")
        movie.insert()
        movie1.insert()
        movie2.insert()

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_path = DATABASE_PATH
        setup_db(app=self.app, database_path=self.database_path)

        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
            self.prepare_test_bed()

        self.actor = {
            "name": fake.name(),
            "age": 45,
            "gender": "male"
        }

        self.movie = {
            "title": "Gulabo Sitabo",
            "release_date": "29/06/2020",
            "production_house": "RK Productions",
            "ott_partner": "Amazon Prime"
        }

        self.movie2 = {
            "title": "Ek Tha Tiger",
            "release_date": "29/06/2020",
            "production_house": "RK Productions",
            "ott_partner": "Hotstar"
        }

        self.producer_header = {"Authorization": "Bearer {}".format(PRODUCER_TOKEN)}
        self.assistant_heaer = {"Authorization": "Bearer {}".format(ASSISTANT_TOKEN)}
        self.director_header = {"Authorization": "Bearer {}".format(DIRECTOR_TOKEN)}

    def tearDown(self):
        pass

    def test_check_health(self):
        response = self.client().get("/health")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Welcome to Casting Agency")

    # -----------------------Testcases for Casting Assistant-------------------------------
    # Testcase: To get All actors infotmation
    def test_get_all_actors_casting_assistant(self):
        response = self.client().get("/actors", headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: to get particular actor information
    def test_get_actor_info_casting_assistant(self):
        response = self.client().get("/actors/1", headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get all movies information
    def test_get_all_movies_casting_assistant(self):
        response = self.client().get("/movies", headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get movie information
    def test_get_movie_info_casting_assistant(self):
        response = self.client().get("/movies/1", headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase(Negative): To add movie with role as casting assistant
    def test_add_movie_casting_assistant(self):
        response = self.client().post("/movies", json=self.movie, headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    # Testcase(Negative): To delete actor with role as casting assistant
    def test_delete_actor_casting_assistant(self):
        response = self.client().delete("/actors/1", headers=self.assistant_heaer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    # -----------------------Testcases for Casting Director-------------------------------
    # Testcase: To get All actors infotmation
    def test_get_all_actors_casting_director(self):
        response = self.client().get("/actors", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: to get particular actor information
    def test_get_actor_info_casting_director(self):
        response = self.client().get("/actors/1", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get all movies information
    def test_get_all_movies_casting_director(self):
        response = self.client().get("/movies", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get movie information
    def test_get_movie_info_casting_director(self):
        response = self.client().get("/movies/1", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Add Actor
    def test_add_actor_casting_director(self):
        response = self.client().post("/actors", json=self.actor, headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Update Actor
    def test_update_actor_casting_direcotr(self):
        response = self.client().patch("/actors/1", json={'name': fake.name()}, headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Update Movie
    def test_update_movie_casting_director(self):
        response = self.client().patch("/movies/1", json={'ott_partner': 'Netflix'}, headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Delete actor
    def test_delete_actor_casting_director(self):
        response = self.client().delete("/actors/1", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase(Negative): To add movie with role as casting director
    def test_add_movie_casting_director(self):
        response = self.client().post("/movies", json=self.movie, headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    # Testcase(Negative) : To delete movie with role as casting director
    def test_delete_movie_casting_director(self):
        response = self.client().delete("/movies/1", headers=self.director_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    # -----------------------Testcases for Casting Producer-------------------------------
    # Testcase: To get All actors infotmation
    def test_get_all_actors_casting_producer(self):
        response = self.client().get("/actors", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: to get particular actor information
    def test_get_actor_info_casting_producer(self):
        response = self.client().get("/actors/2", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get all movies information
    def test_get_all_movies_casting_producer(self):
        response = self.client().get("/movies", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To get movie information
    def test_get_movie_info_casting_producer(self):
        response = self.client().get("/movies/2", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Add Actor
    def test_add_actor_casting_producer(self):
        response = self.client().post("/actors", json=self.actor, headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Update Actor
    def test_update_actor_casting_producer(self):
        response = self.client().patch("/actors/2", json={'name': fake.name()}, headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Update Movie
    def test_update_movie_casting_producer(self):
        response = self.client().patch("/movies/2", json={'ott_partner': 'Netflix'}, headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: Delete actor
    def test_delete_actor_casting_producer(self):
        response = self.client().delete("/actors/2", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase: To add movie
    def test_add_movie_casting_producer(self):
        response = self.client().post("/movies", json=self.movie2, headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Testcase : To delete movie with role as casting director
    def test_delete_movie_casting_producer(self):
        response = self.client().delete("/movies/2", headers=self.producer_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
