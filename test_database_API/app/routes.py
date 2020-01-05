from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Ceci est l'API test pour la création d'une database"
