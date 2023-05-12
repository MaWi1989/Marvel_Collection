from flask import Blueprint, request, jsonify
from marvel_collection.helpers import token_required
from marvel_collection.models import db, Marvel_Character, character_schema, all_characters_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}


@api.route('/all_characters', methods = ['POST'])
@token_required
def create_marvel_character(current_user_token):
    name = request.json['Name']
    description = request.json['Description']
    series = request.json['Series']
    powers = request.json['Super Powers']
    comics_appeared_in = request.json['Comics Appeared In']
    first_appeared_in = request.json['First Appeared In']
    year_introduced = request.json['Year Introduced']
    user_id = current_user_token.id

    print(f'BIG TESTER: {current_user_token.id}')

    character = Marvel_Character(name, description, series, powers, comics_appeared_in, first_appeared_in, year_introduced, user_id = user_id )

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)




@api.route('/all_characters', methods = ['GET'])
@token_required
def get_all_characters(current_user_token):
    user = current_user_token.token
    all_characters = Marvel_Character.query.filter_by(user_token = user).all()
    response = all_characters_schema.dump(all_characters)
    return jsonify(response)



@api.route('/all_characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    if id:
        character = Marvel_Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



@api.route('/all_characters/<id>', methods = ['POST'])
@token_required
def update_character(current_user_token,id):
    character = Marvel_Character.query.get(id)
    character.name = request.json['Name']
    character.description = request.json['Description']
    character.series = request.json['Series']
    character.powers = request.json['Super Powers']
    character.comics_appeared_in = request.json['comics Appeared In']
    character.first_appeared_in = request.json['First Appeared In']
    character.year_introduced = request.json['Year Introduced']
    character.user_id = current_user_token.id

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)



@api.route('/all_characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Marvel_Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)
