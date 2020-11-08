#!/usr/bin/env python3
import argparse
import sys

from . import GetItem

def main():
    parser = argparse.ArgumentParser(prog = 'oitem',
        description = "Lister les fichiers et les dossiers présents")
    parser.add_argument('-p', '--path', nargs = '+', required = True,
        help = "Fichier/dossier cible (support wildcard)")
    parser.add_argument('-i', '--include', nargs = '+', default = [],
        help = "Nom à inclure dans le résultat (support wildcard)")
    parser.add_argument('-e', '--exclude', nargs = '+', default = [],
        help = "Nom à exclure du résultat (support wildcard)")
    parser.add_argument('--ignore-dir', action = 'store_true',
        help = "Ignorer les dossiers dans le résultat")
    parser.add_argument('--ignore-file', action = 'store_true',
        help = "Ignorer les fichiers dans le résultat")
    parser.add_argument('-r', '--recurse', action = 'store_true',
        help = "Activer la lecture récursive")
    parser.add_argument('-d', '--depth', type = int, default = -1,
        help = "Définir la profondeur limite de la lecture récursive (aucune par défaut)")
    parser.add_argument('-s', '--follow-symlink', action = 'store_true',
        help = "Suivre les liens symboliques")

    args = parser.parse_args(sys.argv[1:])

    item_col = GetItem(args.path, 
        include = args.include,
        exclude = args.exclude,
        ignore_dir = args.ignore_dir,
        ignore_file = args.ignore_file,
        recurse = args.recurse,
        depth = args.depth,
        follow_symlink = args.follow_symlink)

    for item in item_col.collect():
        print(item)

if __name__ == "__main__":
    main()