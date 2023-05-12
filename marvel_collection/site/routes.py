from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_collection.forms import MarvelCharacterForm, UserSignupForm
from marvel_collection.models import Marvel_Character, db 

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    signup = UserSignupForm()
    print('dundundundundun')
    return render_template('home.html', form=signup)


@site.route('/profile', methods= ['GET', 'POST'])
@login_required
def profile():
    my_character = MarvelCharacterForm()

  
    if request.method == "POST" and my_character.validate_on_submit():
        name = my_character.name.data
        description = my_character.description.data
        series = my_character.series.data
        powers = my_character.powers.data
        comics_appeared_in = my_character.comics_appeared_in.data
        first_appeared_in = my_character.first_appeared_in.data
        year_introduced = my_character.year_introduced.data   
        user_id = current_user.id

        character = Marvel_Character(name, description, series, powers, comics_appeared_in, first_appeared_in, year_introduced, user_id=user_id)

        db.session.add(character)
        db.session.commit()

        return redirect(url_for('site.profile'))
 

    current_user_id = current_user.id

    all_characters = Marvel_Character.query.filter_by(user_id=current_user_id)


    return render_template('profile.html', form=my_character, all_characters = all_characters )


@site.route('/token', methods = ['POST'])
def show_token():
    return render_template('token.html')


@site.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')



@site.route('/chat', methods = ['GET','POST', 'DELETE'])
def chat():
    return render_template('chat.html')
        