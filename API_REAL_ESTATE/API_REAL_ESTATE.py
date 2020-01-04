#Liens d'accueil de l'application : http://localhost:5000/real_estate/api/v1

from flask import Flask,jsonify,request,abort,make_response

app=Flask(__name__)


#page d'accueil de l'API
@app.route('/real_estate/api/v1')
def index():
    return "Vous êtes bien sur l'API Real Estate"
#dans Anaconda Prompt, saisir curl -i http://localhost:5000/real_estate/api/v1 pour accéder à la page d'accueil de l'API


#base de données temporaire
real_estates=[
    {
        'id': 1,
        'name of the client': 'Thibault',
        'description': 'Appartement tres lumineux',
        'type of real estate': 'Appartement',
        'town': 'Paris',
        'rooms': {
    'bedrooms':3, 'kitchen':1, 'bathrooms':2, 'living_room':1, 'terrace':1
},
        'rooms caracteristics': {},
        'owner': 'Jean'
    }
]

#page pour ajouter un bien immobilier à la base de données
@app.route('/real_estate/api/v1/housing', methods=['POST'])
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
#curl -i -H "Content-Type: application/json" -X POST -d "{\"type of real estate\":\"house\", \"town\":\"Madrid"}" http://localhost:5000/real_estate/api/v1/housing


#page temporaire d'affichage de tous les biens immobiliers, à utiliser seulement pour debugger
@app.route('/real_estate/api/v1/housing', methods=['GET'])
def get_real_estates():
    return jsonify({'real estates':real_estates})
#dans Anaconda Prompt, saisir curl -i http://localhost:5000/real_estate/api/v1/housing pour accéder à tous les biens


#page temporaire d'affichage d'un bien immobilier connaissant son id, à n'utiliser que pour débbuguer
@app.route('/real_estate/api/v1/housing/<int:real_estate_id>', methods=['GET'])
def get_one_real_estates(real_estate_id):
    real_estate=[real_estate for real_estate in real_estates if real_estate['id']==real_estate_id]
    if len(real_estate)==0:
        abort(404)
    return jsonify({'real estate':real_estate})
# saisir curl -i http://localhost:5000/real_estate/api/v1/housing/1 dans Anaconda Prompt pour obtenir les caractéristiques du bien immobilier d'id 1


#page pour modifier les caractéristiques d'un bien
@app.route('/real_estate/api/v1/housing/<int:real_estate_id>', methods=['PUT'])
def update_real_estate(real_estate_id):
    real_estate=[real_estate for real_estate in real_estates if real_estate['id']==real_estate_id]
    #si tout se passe bien cette liste contient un element si real_estate_id existe et est vide sinon
    if len(real_estate)==0:
        abort(404)
    real_estate[0]['name of the client']=request.json.get('name of the client', real_estate[0]['name of the client'])
    real_estate[0]['description']=request.json.get('description', real_estate[0]['description'])
    real_estate[0]['type of real estate']=request.json.get('type of real estate', real_estate[0]['type of real estate'])
    real_estate[0]['town']=request.json.get('town', real_estate[0]['town'])
    real_estate[0]['rooms']=request.json.get('rooms', real_estate[0]['rooms'])
    real_estate[0]['rooms caracteristics']=request.json.get('rooms caracteristics', real_estate[0]['rooms caracteristics'])
    real_estate[0]['owner']=request.json.get('ownner', real_estate[0]['owner'])
    return jsonify({'real_estate':real_estate[0]})
#dans Anaconda Prompt, pour modifier le bien d'id 2 sur la caractéristique ville saisir :
#curl -i -H "Content-Type: application/json" -X PUT -d "{\"town\":\"Valencia\"}" http://localhost:5000/real_estate/api/v1/housing/2


#page d'affichage de tous les biens immobiliers d'une ville donnée
@app.route('/real_estate/api/v1/housing/<town>', methods=['GET'])
def get_real_estates_of_a_town(town):
    real_estates_town=[real_estate for real_estate in real_estates if real_estate['town']==town]
    return jsonify({'real estates':real_estates_town})
#à saisir dans Anaconda Prompt pour afficher les biens de Paris :
#curl -i http://localhost:5000/real_estate/api/v1/housing/Paris


#pour affichier dans un fichier JSON que l'on a une erreur 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
