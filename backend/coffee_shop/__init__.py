from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from schema import Schema, And, Use, Optional, SchemaError
import json

from .models import db, setup_db, Drink
from .auth import requires_auth


def create_app(test_config=None):
    #----------------------------------------------------------------------------#
    # Setup App.
    #----------------------------------------------------------------------------#

    # Create flask app and setup CORS
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Setup sqlalchemy database
    setup_db(app)

    # CORS allowed headers and methods
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    #----------------------------------------------------------------------------#
    # Drinks.
    #----------------------------------------------------------------------------#

    @app.route('/drinks', methods=['GET'])
    def get_drinks():
        drinks = Drink.query.order_by(Drink.id).all()

        if len(drinks) == 0:
            abort(404, 'no drinks found')

        return jsonify({
            'success': True,
            'drinks': [drink.format_short() for drink in drinks]
        })

    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def get_drinks_details(payload):
        drinks = Drink.query.order_by(Drink.id).all()

        if len(drinks) == 0:
            abort(404, 'no drinks found')

        return jsonify({
            'success': True,
            'drinks': [drink.format_long() for drink in drinks]
        })

    #  Create, edit, and delete drinks
    #  ----------------------------------------------------------------

    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(payload):
        body = request.get_json()

        if not body:
            abort(400, 'no json body was found')

        schema = Schema({
            Optional('id'): Use(int),
            'title': str,
            'recipe': [{
                'name': str,
                'color': str,
                'parts': Use(int)
            }]
        })

        # validate drink input
        drink_data = {}
        try:
            drink_data = schema.validate(body)
        except:
            abort(400, 'input drink was bad or not formatted correctly')

        # create drink
        drink = Drink(drink_data['title'], json.dumps(drink_data['recipe']))

        # add drink to database
        error = False
        try:
            db.session.add(drink)
            db.session.commit()
            drink_data = drink.format_long()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't create drink")
        else:
            return jsonify({
                'success': True,
                'drinks': [drink_data]
            })

    @app.route('/drinks/<int:drink_id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def edit_drink(payload, drink_id):
        drink = Drink.query.get(drink_id)

        if not drink:
            abort(422, f'no drink found with id {drink_id}')

        body = request.get_json()
        if not body:
            abort(400, 'no json body was found')

        schema = Schema({
            Optional('id'): Use(int),
            Optional('title'): str,
            Optional('recipe'): [{
                'name': str,
                'color': str,
                'parts': Use(int)
            }]
        })

        # validate drink input
        drink_data = {}
        try:
            drink_data = schema.validate(body)
        except:
            abort(400, 'input drink was bad or not formatted correctly')

        # edit drink
        if 'title' in drink_data:
            drink.title = drink_data['title']
        if 'recipe' in drink_data:
            drink.recipe = json.dumps(drink_data['recipe'])

        # edit drink in database
        error = False
        try:
            db.session.commit()
            drink_data = drink.format_long()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't edit drink")
        else:
            return jsonify({
                'success': True,
                'drinks': [drink_data]
            })

    @app.route('/drinks/<int:drink_id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, drink_id):
        drink = Drink.query.get(drink_id)

        if not drink:
            abort(422, f'no drink found with id {drink_id}')

        # delete drink from database
        error = False
        try:
            drink_data = drink.format_long()
            db.session.delete(drink)
            db.session.commit()
        except:
            db.session.rollback()
            error = True
        finally:
            db.session.close()

        if error:
            abort(500, "couldn't delete drink")
        else:
            return jsonify({
                'success': True,
                'drinks': [drink_data]
            })

    #----------------------------------------------------------------------------#
    # Error Handling.
    #----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request',
            'description': error.description
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized',
            'description': error.description
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'forbidden',
            'description': error.description
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found',
            'description': error.description
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method is not allowed',
            'description': error.description
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity',
            'description': error.description
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error',
            'description': error.description
        }), 500

    return app


if __name__ == "__main__":
    create_app()
