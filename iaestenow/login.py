
from flask.ext.login import LoginManager, UserMixin
from iaestenow.database import Session, User

loginmanager = LoginManager()

@loginmanager.user_loader
def load_user(userid):

    userid = int(userid)
    session = Session()

    query = session.query(User).filter_by(id=userid)

    if query.count() == 1:
        return query.one()
    else:
        return None

def register_user(email, password, name):

    session = Session()

    new = User(email=email, password=password, name=name)
    session.add(new)
    session.commit()
