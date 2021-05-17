from app import app, db
from app.models import *

@app.shell_context_processor
def add_shell_context():
    return {'db': db, 
            'User': User, 
            'Course': Course, 
            'Content': Content, 
            'Quiz': Quiz,
            'Question': Question,
            'Question_Response': Question_Response,
            'Content_Viewed': Content_Viewed,
            'Result': Result}