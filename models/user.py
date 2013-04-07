import hmac
import random
import string
import hashlib
from pymongo.errors import OperationFailure, DuplicateKeyError
import bson
import sys
from exceptions import DoesNotExist, UserPasswordNotMatch


def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt


def make_pw_hash(pw, salt=None):
    if salt is None:
        salt = make_salt()
    return hashlib.sha256(pw + salt).hexdigest() + "," + salt


def validate_login(db, username, password):
    users = db.users
    user = None

    user = users.find_one({'_id': username})
    if user is None:
        user = users.find_one({'email': username})
    if user is None:
        raise DoesNotExist

    salt = user['password'].split(',')[1]

    if (user['password'] != make_pw_hash(password, salt)):
        raise UserPasswordNotMatch

    return user["_id"]


def start_session(db, email):
    sessions = db.sessions
    session = {'username': email}

    try:
        sessions.insert(session)
    except:
        print "Unexpected error on start_session:", sys.exc_info()[0]
        return -1

    return str(session['_id'])


def end_session(db, session_id):
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
        sessions.remove({'_id': id})
    except:
        return


def get_session(db, session_id):
    sessions = db.sessions

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
    except:
        print "bad sessionid passed in"
        return None

    session = sessions.find_one({'_id': id})

    print "returning a session or none"
    return session


# creates a new user in the database
def newuser(db, username, email, password, message):
    # the hashed password is what we insert
    password_hash = make_pw_hash(password)

    user = {"_id": username,
            "email": email,
            "password": password_hash}
    users = db.users
    if users.find_one({"email": email}):
        message["error"] = u"Email has already been token!"
        return False
    try:
        users.insert(user)
    except (OperationFailure, DuplicateKeyError):
        message["error"] = u"Username has already been token!"
        return False
    return True


SECRET = 'AEVC284#^Mcarbnby*6v$jyncg*15cY)@xyH'


def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(s):
    return "{0}|{1}".format(s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val
