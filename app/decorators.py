from functools import wraps
from flask import session
from flask import redirect, url_for

def guest_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id'):
            return redirect(url_for('main.dashboard')) 
        
        return f(*args, **kwargs)
    
    return decorated_function



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('main.login')) 
        
        return f(*args, **kwargs)
    
    return decorated_function