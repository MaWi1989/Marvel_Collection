from flask import Blueprint, request, jsonify
from flask_login import current_user
from marvel_collection.helpers import token_required
from marvel_collection.models import db, Marvel_Character, character_schema, all_characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata/<current_user_token>')
@token_required
def getdata(current_user_token):
    current_user_token = current_user.token
    return {'some': 'value'}


@api.route('/all_characters', methods = ['POST'])
@token_required
def create_marvel_character(current_user):
    name = request.json['name']
    description = request.json['description']
    series = request.json['series']
    powers = request.json['powers']
    comics_appeared_in = request.json['comics_appeared_in']
    first_appeared_in = request.json['first_appeared_in']
    year_introduced = request.json['year_introduced']
    user_id = current_user.id

    print(f'BIG TESTER: {current_user.id}')

    character = Marvel_Character(name, description, series, powers, comics_appeared_in, first_appeared_in, year_introduced, user_id = user_id )

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)




@api.route('/all_characters', methods = ['GET'])
@token_required
def get_all_characters(current_user):
    user = current_user
    all_characters = Marvel_Character.query.filter_by(user_id = user.id).all()
    response = all_characters_schema.dump(all_characters)
    return jsonify(response)



@api.route('/all_characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user, id):
    if id:
        character = Marvel_Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



@api.route('/all_characters/<id>', methods = ['POST'])
@token_required
def update_character(current_user,id):
    character = Marvel_Character.query.get(id)
    character.name = request.json['name']
    character.description = request.json['description']
    character.series = request.json['series']
    character.powers = request.json['powers']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.first_appeared_in = request.json['first_appeared_in']
    character.year_introduced = request.json['year_introduced']
    character.user_id = current_user.id

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)



@api.route('/all_characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user, id):
    character = Marvel_Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)
