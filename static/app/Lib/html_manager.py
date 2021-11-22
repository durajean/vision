# -*- coding: utf-8 -*-

"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 24/09/2021
Descripton : Gestionnaire des fichiers HTML. Contient les fonctions permettant de gérer les fichiers HTML.
"""

#Import des dépendances.
from datetime import datetime
import os

class html_manager():

# =============================================================================
# Constructeur
# =============================================================================   
    def __init__(self, template_path, html_file_path):    
        
        #Initialisation de la localisation du fichier de configuration.
        #Mise à jour de la variable locale.
        self.template_path = template_path
        self.html_file_path = html_file_path
        
        #Affichage des logs : Création du gestinaire de fichier HTML.
        print(f"{self.current_time()} Object html_manager created.")

# =============================================================================
# Fonctions principales
# =============================================================================

    #Génère un fichier HTML.
    def create_html_file(self, hostname, possible_monitor, monitor):
        
        #Création du template HTML de base.
        template = '{% extends "dashboard-template.html" %}\n{% block title %}dashboard-view{% endblock %}\n{% block header %}{{ hostname }}{% endblock %}\n{% block content %}\n{% endblock %}'
        template = template.split("\n")
        
        #Ajout des templates HTML en fonction des éléments à monitorer.
        for m in monitor:

            #Test : si l'éléments a supperviser est déclaré dans la solution alors,
            if m in possible_monitor:

                #On récupère le template HTML.
                #On le convertie en chaine de caractère.
                #On l'ajoute dans le template de base.
                content = open(f"{self.template_path}/{m}-template.html", "r")
                content = "".join(content)
                template.insert(len(template)-1, content)
        
        #On convertie l'ensemble du template en chaine.
        template = "".join(template)
        
        #Ouverture du fichier de HTML.
        #Ecriture dans le fichier de HTML.
        #Fermeture du fichier de HTML.
        fichier = open(f"{self.html_file_path}/{hostname}.html", 'w')
        fichier.write(template)
        fichier.close()
        
        #Affichage des logs : Le fichier .html a été créé.
        print(f"{self.current_time()} file {hostname}.html created.")
    
    #Supprime le fichier HTML.
    def delete_html_file(self, hostname):
        
        #Supprime le fichier HTML.
        os.remove(f"{self.html_file_path}/{hostname}.html")
        
        #Affichage des logs : Le fichier de HTML a été sauvgardé.
        print(f"{self.current_time()} file {hostname}.html deleted.")
                
# =============================================================================
# Fonctions utilitaires
# =============================================================================
    #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())