from hubby import database as db

def setup(env):
    app = env['app']
    request = env['request']
    env['s'] = request.db
    env['db'] = db
    
    
