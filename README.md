# Autocomplete server

Moteur de complétion de mots sur la base de dictionnaires fournis en entrée. L'application prend la forme d'un serveur REST dans une image Docker.

## Configuration

Les variables d'environnement lues au démarrage du serveur sont les suivantes :

| Nom               | Description                                                                                         | Valeur par défaut |
| ----------------- | --------------------------------------------------------------------------------------------------- | ----------------- |
| RESULT_MAX_LENGTH | Nombre maximal de résultats retournés par le système de complétion.                                 | 20                |
| DICTIONARIES_DIR  | Répertoire contenant les dictionnaires à charger au démarrage du serveur.                           | /app/dictionaries |
| HOST              | Adresse d'écoute du serveur HTTP.                                                                   | 0.0.0.0           |
| PORT              | Port d'écoute du serveur HTTP.                                                                      | 8080              |
| LOG_LEVEL         | Niveau de verbosité des logs. Voir <https://docs.python.org/3/library/logging.html#logging-levels>. | INFO              |

## Déploiement

L'application propose une image Docker très basique. Aucune dépendance Python n'étant utilisée, l'image sert uniquement à contenir les fichiers sources et à démarrer le serveur.

L'image est disponible ici :
<https://github.com/matmut7/autocomplete-server/pkgs/container/autocomplete-server>

Exécuter le serveur :

```sh
docker run --rm -it -p 8080:8080 ghcr.io/matmut7/autocomplete-server:main
```

Puis utiliser l'API, par exemple avec `curl` :

```txt
curl 127.0.0.1:8080/autocomplete\?query=hai
["haiku", "hail", "hails", "hair", "haircut", "hairs"]
```

## Serveur

Le serveur REST est également très simple. Les seules dépendances conséquentes sont de la bibliothèque standard : `http`, `urllib`, `json` et `logging`.

L'API comprend deux routes :

#### GET /autocomplete?query=\<prefix\>

L'unique paramètre est la paramètre de requête `prefix`. Retourne tous les mots des dictionnaires débutant par ce préfixe, dans la limite de `RESULT_MAX_LENGTH` et dans l'ordre alphabétique.

Si la paramètre est nul, renvoie une erreur 400.

#### GET /healthz

Permet de vérifier que le serveur est en cours d'exécution.

## Moteur de recherche de mots

Le noyau logique de l'application est la recherche de mots débutant par un préfixe dans les dictionnaires.

### Structure de données du dictionnaire

Dans le cas où plusieurs dictionnaires sont fournis, le serveur lit chaque fichier et agrège un unique dictionnaire qu'il garde en mémoire.

La structure de donnée retenue pour une implémentation simple est une liste triée par ordre alphabétique. Cet ordre a l'avantage de correspondre à l'ordre attendu pour le résultat renvoyé par le serveur.

Il existe également une structure spécifiquement adaptée à notre cas d'usage : la trie, ou arbre préfixe. Cette structure permettrait une recherche par préfixe extrêmement efficace en temps même si elle consomme plus d'espace mémoire.

### Algorithme de recherche

L'algorithme de recherche permis par la liste triée est un simple parcours de la liste dans l'ordre, avec interruption de la recherche une fois qu'aucun mot ultérieur ne peut correspondre.

Il serait également possible d'utiliser une recherche dichotomique pour diminuer la complexité mais la taille réduite des dictionnaires rend cette amélioration largement dispensable.

Ici, aucune dépendance complexe n'est autorisée, même dans la librairie standard. On s'autorise seulement l'usage d'opérateurs basiques comme des comparateurs.

### Précision sur les entrées possibles

Il serait préférable de définir précisément l'espace de caractères acceptés par l'application, tant pour la requête que pour les dictionnaires. Cela permettrait d'assainir systématiquement toutes les entrées, réduisant ainsi les risques d'erreur à l'exécution et la surface d'attaque.
