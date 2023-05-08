from app import app,db
from app.models import User,Post

#define the variables that will be pre-imported when running the flask shell 
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}


