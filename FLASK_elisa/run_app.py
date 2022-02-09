#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Créé le 15/02/2021
@author: Eric Buonocore
"""

# Librairie(s) utilisée(s)
from flask import *
import sqlite3

# Fonctions utilisées pour appeler des commandes SQL
def lire_base():
    """ Récupére des personnes dans la table
        Renvoie (list of tuples) : liste des artistes
    """
    connexion = sqlite3.connect("bdd/artistes_connus.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT *
    FROM artistes_famous;"""
    resultat = curseur.execute(requete_sql)
    artistes = resultat.fetchall()
    connexion.close()
    return artistes

def index_max():
    """ Récupére l'id du prochain enregistrement
        Renvoie un entier
    """
    connexion = sqlite3.connect("bdd/artistes_connus.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT MAX(id)
    FROM artistes_famous;"""
    resultat = curseur.execute(requete_sql)
    index = resultat.fetchall()
    connexion.close()
    return int(index[0][0])+1 # Transtype le résultat de la recherche et ajoute 1


def max_abos():
    """ Récupére l'id du prochain enregistrement
        Renvoie un entier
    """
    connexion = sqlite3.connect("bdd/artistes_connus.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT MAX(nombre_abos)
    FROM artistes_famous;"""
    resultat = curseur.execute(requete_sql)
    index = resultat.fetchall()
    connexion.close()
    return int(index[0][0])+1

def recherche_sql(donnees):
    """ Recherche au moins une des informations comprise dans le dictionnaire donnees
        Si un élément est nul, alors le paramètre de la recherche est vide
        Sinon, il est de la forme: '%'+element+'%'
    """
    parametre0, parametre1 = "", ""
    if donnees['Nom'] !="":
        parametre0 = '%'+donnees['nom']+'%'
    if donnees['singles'] != "":
        parametre1 = '%'+donnees['singles']+'%'
    if donnees['singles2'] != "":
        parametre1 = '%'+donnees['singles2']+'%'
        
    parametres = (parametre0, parametre1)
    connexion = sqlite3.connect("bdd/artistes_connus.db")
    curseur = connexion.cursor()
    requete_sql = """
    SELECT *
    FROM students 
    WHERE nom LIKE ? OR singles LIKE ? OR singles2 LIKE ? ;"""
    resultat = curseur.execute(requete_sql, parametres)
    labos = resultat.fetchall()
    connexion.close()
    return labos

def ajoute_enregistrement(donnees):
    """ Créé l'enregistrement avec le nouvel id et les données saisies
        Renvoire un booléen : True si l'ajout a bien fonctionné
    """
    # Test si tous les champs sont renseignés
    parametre0 = donnees['id']
    parametre1 = donnees['Nom']
    parametre2 = donnees['nombre_abos']
    parametre3 = donnees['singles']
    parametre4 = donnees['singles2']
    if parametre0 != 0 or parametre1 == "" or parametre2 != 0 or parametre3 == "" or parametre4 == "" :
        return False
    parametres = (parametre0, parametre1, parametre2, parametre3, parametre4)
    connexion = sqlite3.connect("bdd/artistes_connus.db")
    curseur = connexion.cursor()
    requete_sql = """
    INSERT INTO Labos (id, Nom, nombre_abos, singles, singles2) VALUES (?,?,?,?,?);"""
    resultat = curseur.execute(requete_sql, parametres)
    connexion.commit()
    connexion.close()
    return True
     
     
# Création d'un objet application web Flask
app = Flask(__name__, static_url_path='/static')
# Création d'une fonction accueillir() associee a l'URL "/"
# pour générer une page web dynamique
@app.route("/")
def accueillir():
    """Présentation du site"""
    return render_template("index.html")

# Page utilisant une base de données
@app.route("/lire")
def lire_complete():
    # Récupération des personnes de la base de données SQLite
    artistes = lire_base()
    # Transmission pour affichage
    return render_template("lecture.html",artistes=artistes)

@app.route("/chercher")
def cherche_individu():
    return render_template("recherche.html")

@app.route("/modifier", methods = ['POST'])
def modification_ligne():
    result = request.form # Récupération des informations en provenance du POST: C'est un dictionnaire
    liste_artistes = recherche_sql(result)
    return render_template("modification.html", id = result['id'], Nom = result['Nom'], nombre_abos = result['nombre_abos'], singles = result['singles'], singles2 = result['singles2'], liste_artistes = liste_artistes)

@app.route("/saisir")
def saisie_ligne():
    """ Ouvre le formulaire pour demander les champs nécessaires à la création d'un enregistrement
    """
    return render_template("saisie.html")

@app.route("/saisir", methods = ['POST'])
def valide_saisie():
    result = request.form # Récupération des informations en provenance du POST: C'est un dictionnaire
    index = index_max()
    ajoute_enregistrement(index, result)  # Créé l'enregistrement avec le nouvel id et les données saisies
    artistes = lire_base() # Interroge la base pour récupérer la liste des labos avant de l'afficher
    return render_template("lecture.html", liste_artistes=liste_artistes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1660, debug=True)
