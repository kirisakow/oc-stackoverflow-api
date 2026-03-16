# Quels outils open source pour généraliser l’approche MLOps (Machine Learning Operations) dans le cadre du projet « Étiquetage automatique des questions StackOverflow » ?

Note technique

## Introduction

Ce document est une note technique qui présente une brève étude des approches et outils open source pour généraliser l’approche MLOps (Machine Learning Operations). Elle se concentre sur deux axes principaux :

- **Pipeline de codage des étapes d’élaboration du modèle** : Automatisation et standardisation des processus.
- **Suivi de la performance en production** : Détection des drifts et maintenance des modèles.

Dans le contexte de ce projet de l'étiquetage automatique des questions Stack Overflow, la qualité des tags influence directement l’expérience utilisateur, rend ces pratiques essentielles pour garantir des prédictions fiables et évolutives.

---

## 1. Principaux Composants d’un Pipeline MLOps

Un pipeline MLOps se décompose en plusieurs étapes clés, chacune pouvant être automatisée et monitorée :

### a) Collecte et Préparation des Données

- **Objectif** : Récupérer et nettoyer les données brutes (e.g., questions Stack Overflow).
- **Exemple** : Requêtes SQL/API, nettoyage du texte, extraction de features (BoW, Word2Vec).

### b) Entraînement des Modèles

- **Objectif** : Expérimenter et entraîner des modèles (supervisés/non supervisés).
- **Exemple** : Tracking des hyperparamètres avec MLFlow, comparaison des métriques.

### c) Validation et Tests

- **Objectif** : Évaluer les modèles sur des jeux de test et valider leur robustesse.
- **Exemple** : Tests unitaires, validation croisée, métriques de couverture des tags.

### d) Déploiement

- **Objectif** : Mettre en production le modèle sélectionné via une API.
- **Exemple** : FastAPI déployé sur Azure, avec CI/CD via GitHub Actions.

### e) Monitoring et Maintenance

- **Objectif** : Surveiller les performances et détecter les drifts.
- **Exemple** : Suivi des métriques en temps réel, alertes en cas de dégradation.

---

## 2. Technologies et Outils pour Automatiser les Étapes

### a) Gestion des Données

- **Kedro** :
  - **Fonctionnalités** : Pipelines reproductibles, catalogues de données, modularité ([documentation Kedro][1]).
  - **Cas d’usage** : Séparation claire entre code, données et paramètres.
  - **Exemple** :
    ```python
    from kedro.pipeline import Pipeline, node
    pipeline = Pipeline([
        node(preprocess_data, "raw_questions", "cleaned_questions")
    ])
    ```

- **MLFlow Data Tracking** :
  - **Fonctionnalités** : Versioning des jeux de données, traçabilité ([guide MLFlow][2]).
  - **Cas d’usage** : Collaboration d’équipe et reproductibilité.

### b) Entraînement et Expérimentation

- **MLFlow** :
  - **Fonctionnalités** : Tracking des expérimentations, gestion des artefacts (modèles, métriques) ([documentation MLFlow][2]).
  - **Cas d’usage** : Dans notre projet, nous avons utilisé MLFlow pour effectuer des runs répétés et comparer les performances des modèles LDA (approche non supervisée, notebook 3) et BERT (approche supervisée, notebook 4). L’interface MLFlow UI a permis de visualiser et sélectionner le modèle optimal.
  - **Exemple** :
    ```python
    with mlflow.start_run():
        mlflow.log_param("model", "BERT")
        mlflow.log_metric("accuracy", 0.95)
    ```

- **Weights & Biases (W&B)** :
  - **Fonctionnalités** : Visualisation des courbes d’apprentissage, collaboration.
  - **Cas d’usage** : Projets nécessitant un suivi visuel avancé.

### c) Déploiement

- **Serveur Git** : [GitHub][7].
- **Plateforme cloud** : Azure.
- **Serveur API HTTP** : [FastAPI][3], un framework pour des API HTTP légères et performantes.
  - **Cas d’usage** : Une API HTTP de prédiction de tags en réponse à une question (voir l'implémentation dans `main.py` et `local_server.py`) accompagnée de tests unitaires (voir `test_main.py` et `test_local_server.py`) pour respecter les bonnes pratique de la profession et éviter des erreurs d'inattention.
  - **Exemple** :
    ```python
    from fastapi import FastAPI
    app = FastAPI()
    @app.post("/predict")
    def predict(text: str):
        return {"predicted_tags": model.predict(text)}
    ```

- **Docker + Kubernetes** :
  - **Fonctionnalités** : Conteneurisation et orchestration.
  - **Cas d’usage** : Déploiement scalable sur le cloud (Azure, AWS).

### d) Monitoring et Suivi

- **Evidently AI** :
  - **Fonctionnalités** : Détection de data drift/concept drift, dashboards ([documentation Evidently][4]).
  - **Cas d’usage** : Surveillance des modèles en production.
  - **Exemple** :
    ```python
    from evidently.report import Report
    report = Report(metrics=[DataDriftTable()])
    report.run(reference_data=ref, current_data=prod)
    ```

- **Prometheus + Grafana** :
  - **Fonctionnalités** : Collecte et visualisation des métriques (latence, précision) ([documentation Prometheus][5] | [Grafana][6]).
  - **Cas d’usage** : Monitoring infrastructure et performance API.

- **Popmon** :
  - **Fonctionnalités** : Détection automatique des anomalies dans les distributions.
  - **Cas d’usage** : Projets avec des données évolutives (e.g., tendances technologiques).

---

## 3. Importance du Suivi de la Performance en Production

### Bénéfices

- **Détection Précoce des Problèmes** : Identification rapide des drifts (data ou concept) avant qu’ils n’impactent les utilisateurs.
- **Maintenance Proactive** : Mises à jour ciblées des modèles (e.g., ré-entraînement avec de nouvelles données).
- **Transparence** : Justification des décisions auprès des parties prenantes (e.g., Chris chez Stack Overflow).

### Risques en l’Absence de Suivi

- **Dégradation Silencieuse** : Un modèle peut devenir obsolète sans que personne ne s’en aperçoive (e.g., nouveaux tags populaires non prédits).
- **Perte de Confiance** : Les utilisateurs perdent confiance dans les suggestions de tags.
- **Coûts Cachés** : Correction rétroactive plus coûteuse que la maintenance continue.

### Exemple Concret pour Stack Overflow

- **Scénario** : Un nouveau framework JavaScript (e.g., Svelte) devient populaire.
- **Sans Monitoring** : Le modèle continue à suggérer des tags obsolètes (e.g., AngularJS).
- **Avec Monitoring** : Détection du concept drift → ré-entraînement avec des données récentes.

---

## 4. Perspectives pour Généraliser l’Approche MLOps dans le Projet

### Étapes Clés à Implémenter

1. **Standardisation des Pipelines** :
   - Utiliser **Kedro** pour structurer les étapes de prétraitement à l’entraînement.
   - Intégrer **MLFlow** pour le tracking des expérimentations.

2. **Automatisation du Déploiement** :
   - Mettre en place une **CI/CD** avec GitHub Actions pour tester et déployer l’API.
   - Conteneuriser l’API avec **Docker** pour un déploiement reproducible.

3. **Monitoring en Production** :
   - Configurer **Evidently AI** pour surveiller les drifts mensuellement.
   - Utiliser **Prometheus/Grafana** pour visualiser les métriques de l’API (e.g., temps de réponse, taux d’erreur).

4. **Documentation et Collaboration** :
   - Documenter chaque étape du pipeline dans un **README.md**.
   - Partager les résultats via **MLFlow UI** pour une revue d’équipe.

### Architecture Proposée

#### Architecture Actuelle (Implémentée dans le Projet)

```
Données Brutes (Stack Overflow - API/SQL)
    ↓
Nettoyage (Notebook 1 : suppression HTML, tokenization)
    ↓
(Feature engineering)
    ↓
Modèles (best model actuel : TfIdfClassifier x LogisticRegression)
    ↓
FastAPI (main.py) → Déploiement sur Azure
    ↓
Evidently AI + Prometheus (Monitoring à implémenter)
```

#### Piste d’Amélioration : Intégration de Kedro pour l’Industrialisation

**Contexte** : Kedro n’a pas été utilisé dans ce projet, mais son adoption future permettrait de :

1. **Structurer le prétraitement** (Notebook 1) en un pipeline reproductible :
   - Définir des `nodes` pour chaque étape (nettoyage, tokenization).
   - Versionner les jeux de données intermédiaires.

2. **Standardiser l’extraction de features** (Notebook 2) :
   - Intégrer BoW et Word2Vec dans des composants modulaires.
   - Faciliter les mises à jour (e.g., ajout de nouveaux embeddings).

3. **S’intégrer à MLFlow** :
   - Lier les pipelines Kedro aux runs MLFlow pour un tracking complet.

**Exemple d’Architecture avec Kedro** :

```
Données Brutes (Stack Overflow)
    ↓
[Kedro] Pipeline de Prétraitement (nodes : nettoyage → tokenization)
    ↓
[Kedro] Extraction de Features (BoW, Word2Vec)
    ↓
[MLFlow] Entraînement & Tracking (Notebooks 3/4)
    ↓
FastAPI (main.py) → Déploiement Azure
```

**Valeur Ajoutée** :
- **Reproductibilité** : Réexécution garantie des étapes de nettoyage.
- **Collaboration** : Séparation claire entre code (Kedro) et analyse (notebooks).
- **Évolutivité** : Ajout facile de nouvelles étapes (e.g., lemmatization).

---

## Conclusion

L’adoption d’une approche MLOps avec des outils comme **MLFlow**, **Evidently AI** et **Prometheus** permet de :

- **Automatiser** les étapes clés du cycle de vie du modèle.
- **Garantir** la reproductibilité et la scalabilité.
- **Minimiser** les risques liés à la dégradation des performances en production.

Pour ce projet de l'étiquetage automatique des questions Stack Overflow, cette approche complète notre implémentation actuelle :
- **MLFlow** a déjà été utilisé pour comparer les modèles LDA et BERT (notebooks 3 et 4).
- **FastAPI** est déployé (fichiers `main.py` et `local_server.py`), mais l’ajout de **Prometheus** permettrait de monitorer son usage réel (temps de réponse, taux d’erreur).

**Perspectives avec Kedro** :
Bien que non utilisé dans ce projet, Kedro représente une piste d’industrialisation pour structurer le prétraitement (notebook 1) et l’extraction de features (notebook 2) en pipelines reproductibles. Son intégration future permettrait de :
- **Standardiser** les étapes de nettoyage et feature engineering.
- **Faciliter la collaboration** en séparant le code de production (Kedro) des analyses exploratoires (notebooks).
- **S’intégrer à MLFlow** pour un tracking complet des données et modèles.

Les outils présentés ici, qu’ils soient déjà implémentés (MLFlow, FastAPI) ou proposés en amélioration (Kedro, Prometheus), offrent une feuille de route pour industrialiser et pérenniser le système de suggestion de tags.

---

[1]: https://kedro.org/docs
[2]: https://mlflow.org/docs/latest/tracking.html
[3]: https://fastapi.tiangolo.com/
[4]: https://www.evidentlyai.com/documentation
[5]: https://prometheus.io/docs/introduction/overview/
[6]: https://grafana.com/docs/
[7]: https://docs.github.com/actions
