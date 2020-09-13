# Full Stack Trivia API Backend

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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with two keys, `categories` and `total_categories`. The first key, `categories`, contains a object of `id: category_string` key:value pairs. The second key, `total_categories` contains an integer with the total number of categories. 
```
{
	categories: {
		'1' : "Science",
		'2' : "Art",
		'3' : "Geography",
		'4' : "History",
		'5' : "Entertainment",
		'6' : "Sports"
	},
	total_categories: 6
}
```

### GET '/questions'
- Fetches a paginated set of questions and their corresponding categories.
- Request Arguments: None
- Returns: An object with four keys: `questions`, `total_questions`, `categories`, and `current_category`. The first key, `questions`, is a list of dictionary objects, each corresponding to a single question, with keys:value pairs: `'id': question_id`, `'question': question_string`, `'answer': answer_string`, `'category': category_id`, and `'difficulty': difficulty_score`, with difficulty scores ranging from 1-5. The second key, `total_questions`, contains an integer with the total number of questions. The third key, `categories` is as in the `GET '/categories'` endpoint, and the fourth key, `current_category` will be None.
```
{
	questions: [
		{
			'id': 2,
			'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
			'answer': 'Apollo 13',
			'category': 5,
			'difficulty': 4
		},
		{
			'id': 5,
			'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
			'answer': 'Maya Angelou',
			'category': 4,
			'difficulty': 2
		}
	],
	total_questions: 2,
	categories: {
		'1' : "Science",
		'2' : "Art",
		'3' : "Geography",
		'4' : "History",
		'5' : "Entertainment",
		'6' : "Sports"
	},
	current_category: None
}
```

### DELETE '/questions/<question_id>'
- Deletes a specific question corresponding to the given question_id parameter.
- Request Arguments: None
- Returns: An object with one key:value pair, `'deleted': question_id`, with `question_id` corresponding to the deleted question.
```
{
	deleted: 2
}
```

### POST '/questions/new'
- Creates a new question and save to the database.
- Request Arguments: `'question'`, `'answer'`, `'category'`, and `'difficulty'` corresponding to the question string, answer string, category id and difficulty level (1-5) of the new trivia question.
- Returns: An object with one key, `created`, the value of which contains a question dictionary as described in the `GET /questions` endpoint.
```
	created: {
		'id': 5,
		'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
		'answer': 'Maya Angelou',
		'category': 4,
		'difficulty': 2
	}	
```

### POST '/questions'
- Fetches questions which match a user input string.
- Request Arguments: `searchTerm` containing the user's search query string
- Returns: Output of the same form as the `GET /questions` endpoint but restricted to questions which contain the user's input string, in a case-insensitive way.
```
{
	questions: [
		{
			'id': 2,
			'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
			'answer': 'Apollo 13',
			'category': 5,
			'difficulty': 4
		}
	],
	total_questions: 1,
	categories: {
		'1' : "Science",
		'2' : "Art",
		'3' : "Geography",
		'4' : "History",
		'5' : "Entertainment",
		'6' : "Sports"
	},
	current_category: None
}
```

### GET '/categories/<category_id>/questions'
- Fetches questions from a given category.
- Request Arguments: None
- Returns: Output of the same form as the `GET /questions` endpoint but restricted to questions from the given category. Additionally, the fourth key, `current_category`, will contain the id of the given category.
```
{
	questions: [
		{
			'id': 2,
			'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?',
			'answer': 'Apollo 13',
			'category': 5,
			'difficulty': 4
		}
	],
	total_questions: 1,
	categories: {
		'1' : "Science",
		'2' : "Art",
		'3' : "Geography",
		'4' : "History",
		'5' : "Entertainment",
		'6' : "Sports"
	},
	current_category: 5
}
```

### POST '/quizzes'
- Allows the user to play the trivia game for a given category, or all categories, by tracking the category (if applicable) as well as which questions have already been asked, and returns a random question from the given category (if applicable) which has not already been asked.
- Request Arguments: `previous_questions` and `quiz_category`
- Returns: An object with one key, `question`, the value of which contains a question dictionary as described in the `GET /questions` endpoint.
```
	question: {
		'id': 5,
		'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
		'answer': 'Maya Angelou',
		'category': 4,
		'difficulty': 2
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