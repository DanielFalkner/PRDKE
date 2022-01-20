from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm, RailwagonForm, RailwagonUpdateForm, PersonwagonForm, \
    PersonwagonUpdateForm, TrainForm, MaintenanceForm, MaintenanceUpdateForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Railwagon, Personwagon, Train, trains_schema, train_schema, Maintenance, \
    maintenances_schema
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    railwagons = Railwagon.query.all()
    personwagons = Personwagon.query.all()
    trains = Train.query.all()
    maintenances = Maintenance.query.all()
    return render_template('index.html', title='Home', railwagons=railwagons, personwagons=personwagons, trains=trains,
                           maintenances=maintenances)


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
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
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
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
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
    all_maintenances = Maintenance.query.all()
    maintenances = []
    for maintenance in all_maintenances:
        if maintenance.user_id == user.id:
            maintenances.append(maintenance)
    return render_template('user.html', user=user, maintenances=maintenances)


@app.route('/train', methods=['GET', 'POST'])
def train():
    form = TrainForm()
    if form.validate_on_submit():
        train = Train(id=form.id.data, width=form.railwagon.data.width, railwagon=form.railwagon.data)
        for personwagon in form.personwagons.data:
            personwagon.train_id_pw = train.id
            if personwagon.width != train.width:
                flash('Width of Railwagon and Personwagon was not equal')
                return redirect(url_for('train'))
        db.session.add(train)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('train.html', title='Train', form=form)


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


@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    form = MaintenanceForm()
    if form.validate_on_submit():
        maintenance = Maintenance(id=form.id.data, user_id=form.user_id.data.id, train_id=form.train_id.data.id,
                                  time=form.time.data)
        db.session.add(maintenance)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('maintenance.html', title='Maintenance', form=form)


@app.route('/deleteMaintenance/<int:id>')
def delete_Maintenance(id):
    maintenance_to_delete = Maintenance.query.get_or_404(id)
    db.session.delete(maintenance_to_delete)
    db.session.commit()
    return redirect(url_for('index'))
    return render_template('index.html', maintenance_to_delete=maintenance_to_delete)


@app.route('/deleteTrain/<int:id>')
def delete_Train(id):
    train_to_delete = Train.query.get_or_404(id)
    db.session.delete(train_to_delete)
    db.session.commit()
    return redirect(url_for('index'))
    return render_template('index.html', train_to_delete=train_to_delete)


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


@app.route('/updateMaintenance/<int:id>', methods=['GET', 'POST'])
def update_maintenance(id):
    maintenance = Maintenance.query.get_or_404(id)
    form = MaintenanceUpdateForm()
    if request.method == 'GET':
        form.id.data = maintenance.id
        form.user_id.data = maintenance.user_id
        form.train_id.data = maintenance.train_id
        form.time.data = maintenance.time
    if form.validate_on_submit():
        maintenance.id = form.id.data
        maintenance.user_id = form.user_id.data.id
        maintenance.train_id = form.train_id.data.id
        maintenance.time = form.time.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('updateMaintenance.html', form=form, maintenance=maintenance)


@app.route('/get-trains', methods=['GET'])
def api_trains():
    all_trains = Train.query.all()
    result = trains_schema.dump(all_trains)
    return jsonify(result)


@app.route("/get-train/<int:id>", methods=["GET"])
def api_train(id):
    train = Train.query.get(id)
    return train_schema.jsonify(train)


@app.route('/get-maintenances', methods=['GET'])
def api_maintenances():
    all_maintenances = Maintenance.query.all()
    result = maintenances_schema.dump(all_maintenances)
    return jsonify(result)


@app.route("/get-maintenance/<int:id>", methods=["GET"])
def api_maintenance(id):
    maintenance = Maintenance.query.get(id)
    return train_schema.jsonify(maintenance)
