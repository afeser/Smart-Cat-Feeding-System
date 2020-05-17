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
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/')
@login_required
def user():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    devices = user.devices
    title = user.username + ' - Devices'
    return render_template('user.html', title=title, devices=devices)

@app.route('/device/<device_id>')
@login_required
def device(device_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    device = user.devices.filter_by(id=device_id).first_or_404()
    title = user.username + ' - ' + device.location
    return render_template('device.html', title=title, device=device)

@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    devices = user.devices
    title = user.username + ' - Devices'
    if request.method == 'POST':
        result = request.form
        input_id = list(result.keys())[0]
        edited = input_id.split('_')
        if len(edited) == 2 and edited[0] == 'device':
            device = Device.query.filter_by(id=int(edited[1])).first_or_404()
            try:
                float_result = float(result[input_id][0])
            except ValueError:
                device.set_location(result[input_id])
            except IndexError:
                pass
        elif len(edited) == 3:
            print(edited)
            device = Device.query.filter_by(id=int(edited[1])).first_or_404()
            cat = device.cats.filter_by(id=edited[2]).first_or_404()
            if edited[0] == 'cat':
                try:
                    float_result = float(result[input_id][0])
                except ValueError:
                    cat.set_name(result[input_id])
                except IndexError:
                    pass
            if edited[0] == 'food':
                print('okidoki')
                try:
                    cat.set_food_amount(int(result[input_id]))
                except:
                    pass

    return render_template('settings.html', title=title, devices=devices)
