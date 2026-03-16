# oc-stackoverflow-api

L'API HTTP sous FastAPI pour mon projet OpenClassrooms «Étiquetage des questions Stackoverflow»

## Installation

1. Faites `git clone ...` et `cd` dans le répertoire du projet cloné.

2. Installez `poetry` [avec pipx][1] ou autrement.

3. Installez les dépendances du projet en exécutant `poetry install --no-root`.

## Usage

1. Démarrez le serveur FastAPI

   - Soit en local, en exécutant `python ./local_server.py --port 5555` (ou tout autre numéro de port).

     ⚠️ Notez qu'il est nécessaire de préfixer cette commande de `poetry run` si vous utilisez poetry.

   - Soit dans le cloud (sur Azure), en y déployant le fichier `main.py`.

2. Ouvrez le notebook `ISAKOV_Kiril_3_notebook_API_Prediction_depl_sur_Azur_062025.ipynb` qui vous servira d'IHM sommaire pour lancer vos requêtes.

[1]: https://python-poetry.org/docs/#installation
