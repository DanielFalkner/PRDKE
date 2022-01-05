from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, RailwagonForm, RailwagonUpdateForm, PersonwagonForm, \
    PersonwagonUpdateForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Railwagon, Personwagon
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    railwagons = Railwagon.query.all()
    personwagons = Personwagon.query.all()
    return render_template('index.html', title='Home', railwagons=railwagons, personwagons=personwagons)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/newUser', methods=['GET', 'POST'])
def newUser():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('newUser.html', title='New User', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/railwagon', methods=['GET', 'POST'])
def railwagon():
    form = RailwagonForm()
    if form.validate_on_submit():
        railwagon = Railwagon(id=form.id.data, max_traction=form.max_traction.data, width=form.width.data)
        db.session.add(railwagon)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('railwagon.html', title='Railwagon', form=form)


@app.route('/personwagon', methods=['GET', 'POST'])
def personwagon():
    form = PersonwagonForm()
    if form.validate_on_submit():
        personwagon = Personwagon(id=form.id.data, seats=form.seats.data, max_weight=form.max_weight.data,
                                  width=form.width.data)
        db.session.add(personwagon)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('personwagon.html', title='Personwagon', form=form)


@app.route('/deleteRw/<int:id>')
def delete_rw(id):
    rw_to_delete = Railwagon.query.get_or_404(id)
    db.session.delete(rw_to_delete)
    db.session.commit()
    return redirect(url_for('index'))
    return render_template('index.html', rw_to_delete=rw_to_delete)


@app.route('/deletePw/<int:id>')
def delete_pw(id):
    pw_to_delete = Personwagon.query.get_or_404(id)
    db.session.delete(pw_to_delete)
    db.session.commit()
    return redirect(url_for('index'))
    return render_template('index.html', pw_to_delete=pw_to_delete)


@app.route('/updateRw/<int:id>', methods=['GET', 'POST'])
def update_rw(id):
    rw = Railwagon.query.get_or_404(id)
    form = RailwagonUpdateForm()
    if request.method == 'GET':
        form.id.data = rw.id
        form.max_traction.data = rw.max_traction
        form.width.data = rw.width
    if form.validate_on_submit():
        rw.id = form.id.data
        rw.max_traction = form.max_traction.data
        rw.width = form.width.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('updateRw.html', form=form, rw=rw)


@app.route('/updatePw/<int:id>', methods=['GET', 'POST'])
def update_pw(id):
    pw = Personwagon.query.get_or_404(id)
    form = PersonwagonUpdateForm()
    if request.method == 'GET':
        form.id.data = pw.id
        form.seats.data = pw.seats
        form.max_weight.data = pw.max_weight
        form.width.data = pw.width
    if form.validate_on_submit():
        pw.id = form.id.data
        pw.seats = form.seats.data
        pw.max_weight = form.max_weight.data
        pw.width = form.width.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('updatePw.html', form=form, pw=pw)
