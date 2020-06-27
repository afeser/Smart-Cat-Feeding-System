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

@app.route('/calendar/')
def calendar():
    cat = Cat.query.all()[2]
    return render_template('calendar.html', title='Calendar', cat = cat)

@app.route('/user/')
@login_required
def user():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    devices = user.devices
    title = user.username
    return render_template('user.html', title=title, devices=devices)

@app.route('/device/<device_id>')
@login_required
def device(device_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    device = user.devices.filter_by(id=device_id).first_or_404()
    title = device.location + ' - ' + user.username
    return render_template('device.html', title=title, device=device)

@app.route('/device/<device_id>/cat/<cat_id>')
@login_required
def cat(device_id, cat_id):
    user = User.query.filter_by(username=current_user.username).first_or_404()
    device = user.devices.filter_by(id=device_id).first_or_404()
    cat = device.cats.filter_by(id=cat_id).first_or_404()
    title = cat.name + ' - ' + device.location + ' - ' + user.username
    fed_times = []
    denial_times = []
    for i in range(31):
        for j in range(3):
            if i < 9:
                day = '0' + str(i+1)
            else:
                day = str(i+1)
            if j == 0:
                hour1 = '08'
                hour2 = '09'
            else:
                hour1 = str(7*j+8)
                hour2 = str(7*j+9)
            fed_times.append('2020-05-'+day+'T'+hour1+':00:00')
            denial_times.append('2020-05-'+day+'T'+hour2+':50:00')
    return render_template('cat.html', title=title, cat=cat, fed_times=fed_times, denial_times=denial_times)

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
        if len(edited) == 2:
            if edited[0] == 'device':
                device = Device.query.filter_by(id=int(edited[1])).first_or_404()
                try:
                    float_result = float(result[input_id][0])
                except ValueError:
                    device.set_location(result[input_id])
                except IndexError:
                    pass
            if edited[0] == 'turnon':
                device = Device.query.filter_by(id=int(edited[1])).first_or_404()
                try:
                    device.set_turn_on(result[input_id])
                except:
                    pass
            if edited[0] == 'turnoff':
                device = Device.query.filter_by(id=int(edited[1])).first_or_404()
                try:
                    device.set_turn_off(result[input_id])
                except:
                    pass
        elif len(edited) == 3:
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
                try:
                    cat.set_food_amount(int(result[input_id]))
                except:
                    pass

    return render_template('settings.html', title=title, devices=devices)

'''
@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    cats = Cat.query.all()
    return render_template('admin.html', title=title, cats=cats)
'''

@app.route('/toggle_on_off') 
def toggled_status():
  device = Device.query.all()[0]
  device.toggle_on_off()
  return 'Toggled'