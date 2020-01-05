#Lien d'accueil de l'application : http://localhost:5000/real_estate/api/v1

#la v2 de l'API a pour objectif de sécuriser notre API REST avec le module flask_httpauth ainsi que de pouvoir gérer la base de données des utilisateurs

from flask import Flask,jsonify,request,abort,make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
auth = HTTPBasicAuth()

#base de données temporaire des utilisateurs
users=[
    {
        'id':1,
        'username':'thibault',
        'password':generate_password_hash('python'),
        'first_name':'thibault',
        'last_name':'decosse',
        'birth_date':'06/07/1998'
    },
    {
        'id':2,
        'username':'valentin',
        'password':generate_password_hash('dojo'),
        'first_name':'valentin',
        'last_name':'riner',
        'birth_date':'07/11/1997'
    }
]


#fonction callback utilisée pour obtenir le mot de passe d'un utilisateur d'une base de données
@auth.verify_password
def verify_password(username,password):
    usernames=[users[i]['username'] for i in range(len(users))]
    if username in usernames:
        index_username=usernames.index(username)
        return check_password_hash(users[index_username].get('password'), password)
        #dans le get, il faut mettre une clé et non pas une valeur
    return False


#on renvoie la réponse accès interdit dans un format JSON au lieu de HTML
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


#page d'accueil de l'API
@app.route('/real_estate/api/v1')
def index():
    return "Bonjour, vous êtes bien sur l'API Real Estate"
#dans Anaconda Prompt, saisir curl -i http://localhost:5000/real_estate/api/v1 pour accéder à la page d'accueil de l'API


#page temporaire d'affichage de tous les users, à utiliser seulement pour debugger
@app.route('/real_estate/api/v1/users', methods=['GET'])
@auth.login_required
def get_all_users():
    return jsonify({'users':users})
#dans Anaconda Prompt, saisir curl -u thibault:python -i http://localhost:5000/real_estate/api/v1/users pour accéder à tous les biens


#page temporaire d'affichage d'un user connaissant son id, à n'utiliser que pour débbuguer
@app.route('/real_estate/api/v1/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_one_user(user_id):
    user=[user for user in users if user['id']==user_id]
    if len(user)==0:
        abort(404)
    return jsonify({'user':user})
#saisir curl -i http://localhost:5000/real_estate/api/v1/user/1 dans Anaconda Prompt pour obtenir les caractéristiques du bien immobilier d'id 1


#base de données temporaire des biens immobiliers
real_estates=[
    {
        'id': 1,
        'name of the client': 'Thibault',
        'description': 'Very bright apartment',
        'type of real estate': 'Apartment',
        'town': 'Paris',
        'rooms': {
            'bedrooms':3,
            'kitchen':1,
            'bathrooms':2,
            'living_room':1,
            'terrace':1
        },
        'rooms caracteristics': {
            'bedrooms':'equiped with bed, desk and wardrobe',
            'kitchen':'fully equiped with fridge, freezer, oven, microwave, tableware, dishwasher...',
            'bathrooms':'one shower, sink and toilet in each bathroom',
            'living room':'one of the best place of the apartment : very bright and calm',
            'terrace':'in the shade'
        },
        'owner': 'Jean'
    }
]


#page temporaire d'affichage de tous les biens immobiliers, à utiliser seulement pour debugger
@app.route('/real_estate/api/v1/housing', methods=['GET'])
@auth.login_required
def get_all_real_estates():
    return jsonify({'real estates':real_estates})
#pour poster un bien immobilier de type "House" de ville "Madrid", saisir dans Anaconda Prompt :
#dans Anaconda Prompt, saisir curl -u thibault:python -i http://localhost:5000/real_estate/api/v1/housing pour accéder à tous les biens


#page temporaire d'affichage d'un bien immobilier connaissant son id, à n'utiliser que pour débbuguer
@app.route('/real_estate/api/v1/housing/<int:real_estate_id>', methods=['GET'])
def get_one_real_estate(real_estate_id):
    real_estate=[real_estate for real_estate in real_estates if real_estate['id']==real_estate_id]
    if len(real_estate)==0:
        abort(404)
    return jsonify({'real estate':real_estate})
# saisir curl -i http://localhost:5000/real_estate/api/v1/housing/1 dans Anaconda Prompt pour obtenir les caractéristiques du bien immobilier d'id 1


#page pour ajouter un user à la base de données : pas d'authentification requise car on cherche à créer le compte d'un utilisateur
@app.route('/real_estate/api/v1/user', methods=['POST'])
def create_user():
    if not 'username' and 'password' and 'first_name' and 'last_name' and 'birth_date' in request.json:
        abort(400)
    user={
        'id': users[-1]['id']+1,
        'username': request.json['username'],
        'password': generate_password_hash(request.json['password']),
        'first_name': request.json['first_name'],
        'last_name': request.json['last_name'],
        'birth_date': request.json['birth_date']
    }
    users.append(user)
    return jsonify({'user':user})
#curl -u thibault -i -H "Content-Type: application/json" -X POST -d "{\"username\":\"remi\", \"password\":\"sombrero\", \"first_name\":\"remi\", \"last_name\":\"alexandre\", \"birth_date\":\"28/06/98\"}" http://localhost:5000/real_estate/api/v1/user


#page pour ajouter un bien immobilier à la base de données
@app.route('/real_estate/api/v1/housing', methods=['POST'])
@auth.login_required
def create_real_estate():
    if not 'type of real estate' and 'town' in request.json:
        abort(400)
    real_estate={
        'id': real_estates[-1]['id']+1,
        'name of the client': request.json.get('name of the client', ""),
        'description': request.json.get('description', ""),
        'type of real estate': request.json['type of real estate'],
        'town': request.json['town'],
        'rooms': request.json.get('rooms',{}),
        'rooms caracteristics': request.json.get('rooms caracteristics',{}),
        'owner': request.json.get('owner',"")
    }
    real_estates.append(real_estate)
    return jsonify({'housing':real_estate})
#pour poster un bien immobilier de type "House" de ville "Madrid", saisir dans Anaconda Prompt :
#curl -u thibault -i -H "Content-Type: application/json" -X POST -d "{\"type of real estate\":\"house\", \"town\":\"Madrid\"}" http://localhost:5000/real_estate/api/v1/housing


#page pour modifier les caractéristiques d'un user
@app.route('/real_estate/api/v1/user/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user=[user for user in users if user['id']==user_id]
    #si tout se passe bien cette liste contient un element si real_estate_id existe et est vide sinon
    if len(user)==0:
        abort(404)
    user[0]['username']=request.json.get('username', user[0]['username'])
    user[0]['password']=request.json.get('password', user[0]['password'])
    user[0]['first_name']=request.json.get('first_name', user[0]['first_name'])
    user[0]['last_name']=request.json.get('last_name', user[0]['last_name'])
    user[0]['birth_date']=request.json.get('birth_date', user[0]['birth_date'])
    return jsonify({'user':user[0]})
#dans Anaconda Prompt, pour modifier le user d'id 2 sur la caractéristique last_name saisir :
#curl -u thibault -i -H "Content-Type: application/json" -X PUT -d "{\"last_name\":\"Morisson\"}" http://localhost:5000/real_estate/api/v1/user/2


#page pour modifier les caractéristiques d'un real_estate
@app.route('/real_estate/api/v1/housing/<int:real_estate_id>', methods=['PUT'])
@auth.login_required
def update_real_estate(real_estate_id):
    real_estate=[real_estate for real_estate in real_estates if real_estate['id']==real_estate_id] #si tout se passe bien cette liste contient un element si real_estate_id existe et est vide sinon
    if len(real_estate)==0:
        abort(404)
    real_estate[0]['name of the client']=request.json.get('name of the client', real_estate[0]['name of the client'])
    real_estate[0]['description']=request.json.get('description', real_estate[0]['description'])
    real_estate[0]['type of real estate']=request.json.get('type of real estate', real_estate[0]['type of real estate'])
    real_estate[0]['town']=request.json.get('town', real_estate[0]['town'])
    real_estate[0]['rooms']=request.json.get('rooms', real_estate[0]['rooms'])
    real_estate[0]['rooms caracteristics']=request.json.get('rooms caracteristics', real_estate[0]['rooms caracteristics'])
    real_estate[0]['owner']=request.json.get('owner', real_estate[0]['owner'])
    return jsonify({'real_estate':real_estate[0]})
#dans Anaconda Prompt, pour modifier le bien d'id 2 sur la caractéristique ville saisir :
#curl -u thibault -i -H "Content-Type: application/json" -X PUT -d "{\"town\":\"Valencia\"}" http://localhost:5000/real_estate/api/v1/housing/2


#page d'affichage de tous les biens immobiliers d'une ville donnée
@app.route('/real_estate/api/v1/housing/<town>', methods=['GET'])
@auth.login_required
def get_real_estates_of_a_town(town):
    real_estates_town=[real_estate for real_estate in real_estates if real_estate['town']==town]
    return jsonify({'real estates':real_estates_town})
#à saisir dans Anaconda Prompt pour afficher les biens de Paris :
#curl -i http://localhost:5000/real_estate/api/v1/housing/Paris


#pour affichier dans un fichier JSON plutôt que HTML que l'on a une erreur 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#activation du debugger intégré de Flask qui nous renvoie une page d'erreur et qui nous évite d'avoir une erreur 500 (interne au serveur) en cas d'erreur de code
if __name__ == '__main__':
    app.run(debug=True)
