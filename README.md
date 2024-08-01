# Application de parsing d'une page HTML( par Herve Stephane )
`hervesiyou@gmail.com`

 
## COMMENT LANCER L'APPLICATION ?`

- Installer un virtualenv `pip install virtualenv` puis `
- Creer dans le dossier fourni l'environnement virtuel nommé `venv`avec `virtualenv venv`
- Activer l'environnement virtuel `source venv/bin/activate`, regarder l'equivalence si vous etes sous windows
- Installer les modules `pip install -r requirements.txt`
- Lancer la commande  `python manage.py runserver`
- Aller dans un navigateur taper `127.0.0.1:8000` consulter l'application

### CONTRAINTES ET LIMITATIONS `




### TO DO

- verifier que l url est valide
- donner le titre et la version html du fichier
- le nombre de HX groupé en X
- le nombre de liens internes et externes
- donner les etat d'accessibilité des liens et leurs contenus
- le nombre de formulaire de login et l'algorithme pour le trouver

### TEST QU'UNE PAGE PEUT CONTENIR UN LOGIN FORM
-  Tester la presence de <form></form>
-  tester la presence de <input> type text ou email ou password ou submit
-  tester la presence d'un <button></button>
 

