# Trivia API Backend

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/pavponn/trivia/blob/master/LICENSE)

## Getting Started
[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/pavponn/trivia/blob/master/LICENSE)

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Working within a virtual environment is recommended. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Documentation

### Endpoints

- GET `/categories`
- GET `/questions?page=<page_number>`
- GET `/categories/<category_id>/questions`
- POST `/questions`
- POST `/questions/search/`
- POST `/quizzes`
- DELETE `/questions/<question_id>`

#### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. Response example:

```
{
  '1' : "Science",
  '2' : "Art",
  '3' : "Geography",
  '4' : "History",
  '5' : "Entertainment",
  '6' : "Sports"
}
```

#### GET `/questions?page=<page_number>`

- Fetches a list of questions by pages of size 10. Each question is stored as a map with keys `id`, `question`, `answer`, `category`, `difficulty`.
- Request Arguments: page number (optional)
- Returns an object, that stores list of questions and all categories. Response example:

```
{
  "categories": {
    "1": "Science",
    "2": "Entertainment"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 2,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ]
}
```

#### GET `/categories/<category_id>/questions`

- Fetches questions from specified category.
- `category_id` - id of category to fetch questions for.
- Returns an object that stores questions for given category. Response example:

```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ]
}
```

#### POST `/questions`

- Adds a new question to the database of available questions that are used in the game.
- Request body example:

```
{
  question: "question description",
  answer: "anwser to the question",
  difficulty: 1,
  category: 1
}
```

- Response example:

```
{
  "success": true,
  "created_question": 100
}
```

#### POST `/questions/search/`

- Fetches all the questions that contain specified substring in the question.
- Request body:

```
{
  "searchTerm" : "how many"
}
```

- Response example:

```
{
  "questions": [
    {
      "answer": "24",
      "category": 3,
      "difficulty": 1,
      "id": 30,
      "question": "How many hours in a day?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### POST `/quizzes`

- Fetches one random question within a specified category. A random question is taken from the question are not in `previous_questions` list.
- Request body example:

```
{
  "previous_questions": [1, 3],
  "quiz_category": {"id": 1, type:"Scince"}
}
```

- Returns a randomly picked question. Response example:

```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

#### DELETE `/questions/<question_id>`

- Deletes question with specified id from question database.
- `category_id` - id of question to be deleted.
- Response example:

```
{
  "deleted_question": 309,
  "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
