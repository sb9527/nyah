# Full Stack Capstone Project Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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

## Database Setup
To setup database, go to /src/database/models.py to find details.

## Running the server

From within the `backend/src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
. setup.sh
flask run
```
## API Reference

### Intro
This reference documents every object and method available in this project.

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Errors
Errors are returned as JSON objects in the following format:

```javascript
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will return two error types when requests fail:

- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### POST /users
- General
	- create a user record in database
- Sample
	```bash
		curl -X POST http://127.0.0.1:5000/users -d '{"auth0_user_id":"","nickname":"",picture_url":""}'
	```
```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /questions
- General
	- Returns a list of questions, total_questions, current_category, categories, success value
	- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample
	```bash
		curl http://127.0.0.1:5000/questions?page=2
	```
```javascript
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "my first answer", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "my first question"
    }
  ], 
  "success": true, 
  "total_questions": 18
}
```

#### DELETE /questions/{question_id}
- General
	- Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.
- Sample
	```bash
		curl -X DELETE http://127.0.0.1:5000/questions/22?page=2
	```
```javascript
{
  "deleted": 22, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 15
}
```

#### POST /questions
- General
	- Creates a new question using the submitted question, answer, difficulty and category. Returns the id of the created question, success value.
- Sample
	```bash
		curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"example Q", "answer":"example A", "difficulty":"3","category":"2"}'
	```
```javascript
{
  "created": 27, 
  "success": true
}
```

#### POST /questions/search 
- General
	- Creates a new search using the search term. Returns a list of questions meet the term, total_questions, current_category and success value.
- Sample
	```bash
		curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"movie"}'
	```
```javascript
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

#### GET /categories/{category_id}/questions
- General
	- Returns a list of questions in the specific category, total_questions, current_category and success value.
- Sample
	```bash
		curl http://127.0.0.1:5000/categories/4/questions
	```
```javascript
{
  "current_category": 4, 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

```

#### POST /quizzes
- General
	- Create a quiz using categery and completed questions. Return a new question and success value.
- Sample
	```bash
		curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions":[17],"quiz_category":{"type":"Art","id":"2"}}'
	```
```javascript
{
  "question": {
    "answer": "second1", 
    "category": 2, 
    "difficulty": 3, 
    "id": 26, 
    "question": "second1"
  }, 
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

## Deployment

## Authors