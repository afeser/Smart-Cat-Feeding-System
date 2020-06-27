from app import app, db
from app.models import User, Device, Cat, Fed_Time, Denial_Time

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Device': Device, 'Cat': Cat, 'Fed_Time': Fed_Time, 'Denial_Time': Denial_Time}
