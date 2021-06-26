from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required, AnonymousUserMixin
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username' : 'Pranto'}
    posts = [
        {
            'author' : { 'username' : 'John'}, 
            'body' : 'Beautiful day in Portland'
        }, 

        {
            'author': {'username' : 'Susan' }, 
            'body' : 'The avengers Movie was so cool!'
        }
        
    ]
    return render_template('index.html', title = 'Home', user=user, posts=posts), 200


# Login handaller
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or password")
            return redirect(url_for('login')), 301
        login_user(user, remember=form.remember_me.data) 
        """
        /index, for example, the @login_required decorator will intercept the
        request and respond with a redirect to /login, but it will add a query
        string argument to this URL, making the complete redirect URL
        /login?next=/index. The next query string argument is set to the
        original URL, so the application can use that to redirect back after
        login.
        """
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page), 301

        return redirect(url_for('index'))
        # flash("Login requested for user {}, remember_me = {}".format(form.username.data, form.remember_me.data))
        # return redirect(url_for('index')), 301

    return render_template('login.html', title = 'Sign In', form = form), 200


#logout handler
@app.route('/logout')
def logout(): 
    logout_user()
    return redirect(url_for('index')), 301


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index')), 301
    
    form = RegistrationForm()

    if form.validate_on_submit():
        print("Pass")
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login')), 301
    
    return render_template('register.html', title='Register', form=form), 200



#User Profile view function
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    email_hash = user.avatar()
    posts = [
        {'author' : user, 'body' : 'TEST post #1'}, 
        {'author' : user, 'body' : 'TEST POST #2'}
    ]

    return render_template('user.html', user=user, posts = posts, email_hash = email_hash), 200


