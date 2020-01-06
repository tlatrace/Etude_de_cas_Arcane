Comment utiliser cette API et son repository ?

I.	Installation des outils.

Cette API REST a été développée en Python 3.7.3 sous l'environnement de développement Pycharm. Elle est disponible dans le dossier API_REAL_ESTATE sous le nom de API_REAL_ESTATE. Afin de créer des pages web plus facilement, j’ai travaillé avec le framework Flask, que j’ai dû importer dans mon projet. J’ai également importer flask-httpauth, une extension de Flask permettant de simplifier l’authentification HTTP des utilisateurs de l’API. Pour pouvoir faire des requêtes à l’API directement dans le terminal Python, l’outil cURL a été installé via la commande pip. Dans le code, des exemples de requêtes HTTP à saisir dans le terminal sont disponibles en commentaire sous chaque fonction. Notons que le serveur utilisé pour cette API est le serveur local de la machine hébergeant le code. Enfin, toute cette API a été conçue pour que les fichiers renvoyés sur les différentes adresses HTTP soient au format JSON.

II.	Explication du code.

Le code permet de gérer la base de données des biens immobiliers ainsi que celle des utilisateurs. Ces bases de données sont sous la forme de liste de dictionnaires, chaque dictionnaire représentant un bien immobilier (et respectivement un utilisateur) avec toutes ses caractéristiques. Nous reviendrons sur les limites de cette modélisation de base de données dans la partie suivante. Les routes de chaque page HTTP sont disponibles dans les décorateurs @app.route(‘nom_de_la_route’). Les correspondances entre chaque fonctionnalité avec son URL et la méthode HTTP utilisée sont disponibles dans le tableau suivant (une version plus agréable à lire est disponible dans le document "Correspondance_Action_URI_Methode.docx"):


Méthode HTTP	URL						Fonctionnalité

GET		/real_estate/api/v1				Accéder à la page d’accueil de l’API

POST		/real_estate/api/v1/housing			Renseigner un bien immobilier avec ses caractéristiques

GET		/real_estate/api/v1/housing/<real_estate_id>	Accéder aux caractéristiques d’un bien particulier

PUT		/real_estate/api/v1/housing/<real_estate_id>	Modifier les caractéristiques d’un bien particulier

GET		/real_estate/api/v1/housing/<town>		Renvoyer une liste de logements d’une ville particulière 

POST		/real_estate/api/v1/user			L’utilisateur est nouveau et renseigne ses informations personnelles

GET		/real_estate/api/v1/user/<int:user_id>		L’utilisateur accède à ses informations personnelles

PUT		/real_estate/api/v1/user/<int:user_id>		L’utilisateur modifie ses informations personnelles


Dans le code Python, chaque fonction est précédée par un commentaire expliquant à quoi elle sert et dans quel cas l’utiliser.

III.	Limites de l’API.

Le principal défaut de mon API concerne la base de données. Actuellement, les données de nos utilisateurs et de nos biens immobiliers sont stockées dans des listes de dictionnaires, les clés du dictionnaire correspondant aux informations personnelles des utilisateurs ou aux caractéristiques du bien immobilier. Ce n’est pas du tout conseillé du point de vue de la sécurité informatique des données. En effet, bien que cela soit optionnel, les API de type REST doivent respecter la règle du « code on demand » stipulant que le serveur peut fournir au client le code de l’API pour qu’il puisse l’utiliser dans son propre contexte. Toutes les données seraient alors accessibles. Pour éviter cela, il aurait fallu lier le code Python à une base de données extérieure dans laquelle seraient stockées les données des utilisateurs et des bien immobiliers. Par manque de temps, je n’ai pas pu implémenter cette base de données. Cependant, j’ai fait des tests sur Python pour utiliser le module Flask-SQLAlchemy qui permet de gérer des bases de données et qui fonctionne avec PostgreSQL. Les tests sont disponibles dans le dossier test_database_API.
De plus, la fonctionnalité bonus « un propriétaire ne peut modifier que les caractéristiques de son bien sans avoir accès à l’édition des autres biens » n’a pas encore été implémentée, faute de temps. Pour implémenter celle-ci, il aurait fallu que le nom du propriétaire connecté sur la plateforme soit présent dans la requête HTTP. En effet, la règle « stateless » que doivent respecter les API REST impose que le serveur ne peut pas stocker d’informations d’une requête et les utiliser pour une autre requête. Cependant, je n’ai pas encore trouvé le moyen de fournir dans la requête HTTP le nom de l’utilisateur réellement connecté, et ce en évitant les usurpations d’identité (l’utilisateur connecté pourrait saisir dans la requête HTTP le nom d’un autre utilisateur).
Enfin, lorsque l’API sera opérationnelle et un peu plus optimisée, il serait préférable de l’héberger sur un serveur Web. Actuellement, celle-ci est uniquement disponible en local sur ma machine.


IV.	Approche/organisation de l’étude de cas. 

Le déroulé de mon étude de cas s’est divisé en deux grandes parties. Tout d’abord, j’ai profité de cette opportunité pour me former à des outils informatiques que je n’avais parfois jamais utilisés. J’ai passé les premiers jours à revoir des notions sur Git et le protocole HTTP, ainsi qu’à me familiariser avec Flask et HTML au travers de plusieurs tutoriels. Les liens de tous les tutoriels utilisés pour cette étude de cas sont renseignés dans les différents documents Word « Tuto » déposés sur le repository. Concernant l’utilisation de Flask, j’ai tout d’abord suivi le MOOC permettant de créer un formulaire sur un site web pour ensuite passer à ce qui m’intéressait, à savoir coder une API REST avec Flask. Le fichier annexe « Notes_en_vrac.docx » regroupe des notes prises à la volée pour garder une trace écrite d’informations utiles pour l’étude de cas. Pour ce qui est de la deuxième grande partie de mon approche de l’étude de cas, je l’ai passé à coder l’API pour remplir les différents critères des consignes. Tout au long de l’étude de cas, j’ai mis à jour régulièrement les fichiers de mon repository sur Github, pour avoir un suivi de ma progression.
J’ai finalement investi beaucoup de temps pour me former sur ces outils qui, j’en suis sûr, me seront utiles un jour ou l’autre dans mon parcours en programmation.
