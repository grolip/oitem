# OITEM

## Description

Oitem a pour objectif de fournir une collection d'objets s'inspirants des Cmdlets de Powershell utilisées dans la manipulation des fichiers/dossiers. 

Il n'est pas question ici de langage de script ou bien de pipeline mais uniquement de "commandes" indépendantes représentées par des objets.

En savoir plus: https://github.com/grolip/oitem/wiki

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
