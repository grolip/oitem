# OITEM

## Description

Oitem permet d'intéragir avec des fichiers/dossiers à la manière des commandes Powershell Get-Item et Get-ChildItem.

Pour y parvenir, il fait appel entre autre aux modules pathlib, glob et fnmatch de la librairie standard python.


## Classe GetItem

oitem.get_item.GetItem

### Paramètres

| Nom          | Type        | Description                                  |
|:-------------|:------------|:---------------------------------------------|
| path         | list[str]   | Chemins cibles. Support wildcard.            |
| include      | list[str]   | Nom à inclure dans le résultat final.        |
| exclude      | list[str]   | Nom à exclure du résultat final.             |
| ignore_dir   | bool        | Exclure tous les dossier du résultat final.  |
| ignore_file  | bool        | Exclure tous les fichier du résultat final.  |
| recurse      | bool        | Recherche récursive. |
| depth        | int         | Limiter la profondeur de la recherche récursive. |
| follow_symlink | bool       | Suivre les liens symboliques |

### Méthodes

La méthode principale est ```obj.collect()```. Elle renvoie un générateur de chemins répondant aux critères passés lors de la création de l'objet. Ces chemins sont générés à l'aide de pathlib.Path et leur type est changeant selon le système d'exploitation hôte.

### Exemples

Retourner tous les fichiers .mp3 et m4a contenus dans deux dossiers distincs. Nous activons la recherche récursive sans limiter sa profondeur.

```python
from oitem import GetItem

item_col = GetItem(["~/Musiques/*", "~/Téléchargement/*"], 
    include = ["*.mp3", "*.m4a"],
    recurse = True)

items = [ item for item in item_col.collect() ]
```

Retourner tous les fichiers sauf les scripts python commençant par "test_".
Le premier chemin passé signifie "tous les enfants du dossier courant".

```python
from oitem import GetItem

item_col = GetItem(["*", "~/Documents/Projets/*"], exclude = ["test_*.py"], ignore_dir = True)
items = [ item for item in item_col.collect() ]
```

## Classe GetChildItem

oitem.get_child_item.GetChildItem

Cette classe agit de manière quasi identique à GetItem à la différence près que ce n'est plus les chemins passés qui sont pris pour cible mais leurs enfants. Autrement dit, si un chemin vers un fichier lui est passée, il est ignoré lors de la collecte.

### Exemples

Retourner tous les dossiers du dossier courant.

```python
from oitem import GetChildItem

item_col = GetChildItem(["."], ignore_file = True)

items = [ item for item in item_col.collect() ]
```

Retourner tous les fichiers text et markdown. On limite la recherche récursive.

```python
from oitem import GetChildItem

item_col = GetChildItem(["~/Documents", "~/Téléchargement"], 
    include = ["*.txt", "*.md"],
    recurse = True,
    depth = 3)

items = [ item for item in item_col.collect() ]
```

## Notes

Lors du balayage d'un dossier, si l'utilisateur courant n'a pas les droits de lecture, l'exception PermissionError est ignorée.

## Utilisation en tant qu'outil

Il est possible d'utiliser les capacités de la classe GetItem directement depuis la ligne de commande.

### Options

| nom           | correspondance     |
|--------------:|:-------------------|
| -p            | path |
| -i            | include |
| -e            | exclude |
| --ignore-dir  | ignore_dir |
| --ignore-file | ignore_file |
| -r            | recurse |
| -d            | depth |
| -s            | follow_symlink |

### Exemple

Retourner le contenu de Documents et Téléchargement de manière récursive avec une profondeur maximale de 3.

```bash
python3 -m oitem -p ~/Documents/* ~/Téléchargement/* -r -d 3
```
