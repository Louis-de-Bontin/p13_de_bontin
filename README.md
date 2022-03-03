## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


# My work

## Deploy
You should always be working on a different branch than "main". The branch "main" is reserved for the production phase. Indeed, pushing some code on the "main" branch will update the heroku app, which is not what we want during a development phase.<br>
When you push a commit on any other branch, the CircleCI will still run, but only the tests and linting will be preformed. Here is the workflow you must adopt :
- Pull the branch you need to work on, or pull the branch "main", then do `git checkout -B NEW_BRANCH_NAME` to work on a different branch
- Make the modifications locally
- Run the tests and the linting localy to avoid pushing again and loosing time if anything fails
- Push on the same branch on github (the tests and linting will proceed automaticly)
- Once the team agree that the code is ready for deployment, merge the curent branch with "main" (the best practice would be to have a "ready_to_deploy" branch to perform the merging of all the work the team did to fix the conflicts and check all features implementations. Once it's done, you can perform the merge with the "main" branch. I was the only worker on that project, so no conflict should arise, this is why I decided to skip this step.)
- CircleCI will automaticly proceed to test, lint, build docker image and push the code on Heroku, which will deploy the update<br><br>
So, as you can see, everything is automatic, the workflow has the same rules as usuall, and everything in regard of the deployment is taken care of by CircleCI. But, a particular rigor with the "main" branch is expected, because every pushes on it that passes the tests and linting would update the running application on Heroku.

## What does CircleCI ?
### Not branch "main"
- Builds a virtual environment
- Installs the dependencies in this environment
- Runs the tests and the linting.
- Signal on CircleCI and GitHub UXs if everything is ok, or not.
### Branch "main"
- Proceeds to all actions described above
- If something went wrong, stops and signals on CircleCI and GitHub UXs that something went wrong
- Login to Docker Hub (username and password are stored in the evironment variables in CircleCI)
- Builds the image, uses the repository name and the SHA1 hash available in the Variable CircleCI automaticly made while preparing the environment variables
- Pushes the image to docker hub, using the same variables
- If something went wrong, stops and signals on CircleCI and GitHub UXs that something went wrong
- Deploys on heroku (requires the Heroku API key, and the application name in environment viriables on CircleCI)
- Signals on CircleCI and GitHub UXs that everything is ok

## Build an Heroku app
- On the Heroku UX, create a new app
- In the "deploy" section of the app, select GitHub, and link the app with the repository
- Don't check the "Wait for CI to pass", and don't select "Enable Automatic Deploy"
- In the "Manual Deploy" section, enter "main" in the "Name of Branch" section
- And click on "Deploy Branch"
- Update the environment variables on Heroku with the new application name
- Now, every push on the main branch that passes the tests and the linting will update the application in production phase

## Docker
Run the app from Docker Hub :
- Install docker `snap install docker`
- Build and run the image `docker run --rm -p 8000:8000 likhardcore/oc-lettings`