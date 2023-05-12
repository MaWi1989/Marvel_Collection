from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_collection.forms import UserLoginForm, UserSignupForm
from marvel_collection.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()

    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print( first_name, last_name, email, username)

        user = User(first_name, last_name, email, username, password)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully created a user account {username}', 'user-created')

        return redirect(url_for('auth.signin'))

    
    return render_template('signup.html', form=form)



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    # try:
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)

        logged_user = User.query.filter(User.username == username).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successfully logged in: Via Email/Password', 'auth-success')
            return redirect(url_for('site.profile'))
        else:
            flash('Your Email/Password is incorrect', 'auth-failed')
            return redirect(url_for('auth.signin'))
    # except:
    #     raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))