import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    page_questions = questions[start:end]

    return page_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/*": {"origin": "*"}})

    @app.after_request
    def add_header(response):
        # set up headers for CORS
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route("/categories", methods=['GET'])
    def get_categories():
        # get all categories
        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {category.id: category.type for category in categories}
        
        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(formatted_categories)
        })

    @app.route("/questions", methods=['GET'])
    def get_questions():
        # get all questions, paginated
        page = request.args.get('page', 1, type=int)
        questions = Question.query.order_by(Question.id).all()
        page_questions = paginate_questions(request, questions)
        formatted_questions = [question.format() for question in page_questions]

        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {category.id: category.type for category in categories}
        
        if len(page_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })

    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        # delete the given question
        try:
            question = Question.query.get(question_id)
            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    @app.route("/questions/new", methods=['POST'])
    def create_question():
        # create a new question
        body = request.get_json()
        try:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')

            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()

            return jsonify({
                'success': True,
                'created': question.format()
            })
        except:
            abort(422)

    @app.route("/questions", methods=['POST'])
    def search_questions():
        # search for a question
        body = request.get_json()
        try:
            search_term = body.get('searchTerm')

            results = Question.query.filter(
              Question.question.ilike(f'%{search_term}%')
            ).all()

            formatted_questions = [question.format() for question in results]

            categories = Category.query.order_by(Category.type).all()
            formatted_categories = {category.id: category.type for category in categories}

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(results),
                'categories': formatted_categories,
                'current_category': None
            })
        except:
            abort(422)

    @app.route("/categories/<category_id>/questions", methods=['GET'])
    def get_questions_by_category(category_id):
        # get questions by category
        questions = Question.query.filter(
          Question.category == category_id
        ).all()
        formatted_questions = [question.format() for question in questions]

        categories = Category.query.order_by(Category.type).all()
        formatted_categories = {category.id: category.type for category in categories}
        
        if len(questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': category_id
        })

    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        # play the quiz game
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions')
            quiz_category = body.get('quiz_category')

            if quiz_category['id'] == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions),
                    Question.category == quiz_category['id']
                ).all()

            if len(questions) > 0:
                question = questions[random.randrange(0, len(questions))].format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question
            })
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
  
    return app

    