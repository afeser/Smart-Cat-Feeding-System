from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from app.models import User, Device, Cat
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index/')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login/', methods=['GET', 'POST'])
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

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    devices = user.devices
    device_ids = []
    for device in devices:
        device_ids.append(device.id)
    title = user.username + ' - Devices'
    return render_template('user.html', title=title, devices=devices, device_ids=device_ids)

@app.route('/user/<username>/<device_id>')
@login_required
def device(username,device_id):
    user = User.query.filter_by(username=username).first_or_404()
    device = user.devices.filter_by(id=device_id).first()
    cats = device.cats
    cat_ids = []
    cat_last_feds = []
    for cat in cats:
        cat_ids.append(cat.id)
        cat_last_feds.append(cat.get_time_after_last_feeding())
    title = user.username + ' - ' + device.location
    return render_template('device.html', title=title, device=device, cats=cats, cat_ids=cat_ids, cat_last_feds=cat_last_feds)

@app.route('/user/<username>/<device_id>/<cat_id>')
@login_required
def cat(username,device_id,cat_id):
    user = User.query.filter_by(username=username).first_or_404()
    device = user.devices.filter_by(id=device_id).first()
    cat = device.cats.filter_by(id=cat_id).first()
    return render_template('cat.html', title=cat.name, device=device, cat=cat)
