from app import app, db
from app.models import User, Course, Content

@app.shell_context_processor
def add_shell_context():
    return {'db': db, 'User': User, 'Course': Course, 'Content': Content}