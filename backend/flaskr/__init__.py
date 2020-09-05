import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def format_categories(categories):
  return {category.id : category.type for category in categories}

def format_questions(questions):
  return [question.format() for question in questions]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Setting up CORS. Allows '*' for origins.
  '''
  CORS(app)

  '''
  The after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  The endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    
    # no need to throw an error if categories are empty. 
    # Seems absolutely valid from API perspective

    return jsonify({
      "success": True,
      "categories": format_categories(categories)
    })


  '''
  GET endpoint to handle requests for questions, 
  including pagination (every 10 questions). 
  This endpoint returns a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page, QUESTIONS_PER_PAGE).items
    
    categories = Category.query.order_by(Category.id).all()
    
    return jsonify({
      "success": True,
      "questions": format_questions(questions),
      "total_questions": Question.query.count(),
      "categories": format_categories(categories)
    })

  '''
  DELETE endpoint to delete question using a question ID. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
      return jsonify({
        "success": True,
        "deleted_question": question_id
      })
    except:
      abort(422)

  '''
  POST endpoint to add a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
    if (not 'question' in body) or (not 'answer' in body) or (not 'category' in body) or (not 'difficulty' in body):
        abort(422)
    question = body.get('question')
    answer = body.get('answer')
    category = body.get('category')
    difficulty = body.get('difficulty')
    try:
      question_obj = Question(question, answer, category, difficulty)
      question_obj.insert()

      return jsonify({
        "success": True,
        "created_question": question_obj.format()
      })
    except:
      abort(422)

  '''
  POST endpoint to get questions based on a search  term. 
  It returns any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_qustions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    if not search_term:
      abort(404)
    try:
      searched = Question.query.filter(func.lower(Question.question).contains(search_term.lower())).all()
      return jsonify({
        "success": True,
        "questions": format_questions(searched),
        "total_questions": len(searched),
      })
    except:
      abort(422)
 
  '''
  GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    try:
      questions_with_needed_category = Question.query.filter(Question.category == str(category_id)).all()
      return jsonify({
        "success": True,
        "questions": format_questions(questions_with_needed_category),
        "current_category": category_id
      })
    except:
      abort(404)

  '''
  POST endpoint to get questions to play the quiz. 
  This endpoint takes category and previous question parameters 
  and returns a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_game():
    body = request.get_json()
    if not 'previous_questions' in body:
      abort(422)
    try:
      category = body.get('quiz_category', None)
      prev_questions = set(body.get('previous_questions'))
      possible_questions = []
      if category is None or category['id'] == 0:
        possible_questions = Question.query.filter(Question.id not in prev_questions).all()
      else:
        possible_questions = Question.query.filter_by(category=category['id']).filter(Question.id not in prev_questions).all()
      new_question = random.choice(possible_questions).format() if len (possible_questions) > 0 else None

      return jsonify({
        "success": True,
        "question": new_question
      })
    except:
      abort(422)
  

  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not Found"
    }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
     return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400


  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500
  
  return app

    