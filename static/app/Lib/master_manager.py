# -*- coding: utf-8 -*-

"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 24/09/2021
Descripton : Contrôlleur. Contient les fonctions permettant de gérer les gestionnaires.
"""
#Import des dépendances.
from datetime import datetime
from time import sleep

#Import des gestionnaires
from config_manager import config_manager
from saves_manager import saves_manager
from html_manager import html_manager
from thread_manager import thread_manager

class master_manager():

# =============================================================================
# Constructeur
# =============================================================================   
    def __init__(self, config_file_path, path_save_directory, path_template, path_html):    
        
        #Création du gestionnaire de configuration.
        #Création du gestionnaire de sauvgarde.
        #Créatin du gestionnnaire de fichier HTML.
        self.config_manager = config_manager(config_file_path)
        self.saves_manager = saves_manager(path_save_directory)
        self.html_manager = html_manager(path_template, path_html)
        
        #Liste de threads.
        self.threads = []
        
        #Affichage des logs : Création du master_manager (contrôleur).
        print(self.current_time() + " Object master_manager created.")

# =============================================================================
# Fonctions principales
# =============================================================================
    
    #Permet d'ajouter un hôte.
    def add_host(self,hostname, ip, community, monitor):
        
        #On ajoute l'hôte de la fichier de configuration.
        #On créée un fichier de sauvgarde.
        #On génère une page html.
        self.config_manager.add_host(hostname, ip, community, monitor)
        self.saves_manager.create_save_file(hostname, monitor)
        self.html_manager.create_html_file(hostname, self.get_host_info(hostname)['Monitor'], monitor)
        
        #On créée le thread lié à l'hôte.
        #démmarage du thread.
        self.threads.append(thread_manager(self.get_host_info(hostname)))
        self.start_new_thread()
    
    #Permet du supprimer un hôte.  
    def delete_host(self,hostname):

        #Supprime l'hôte du fichier de configuration.
        #Supprime le fichier de sauvgarde associé à l'hôte.
        #Supprime le fichier HTML associé à l'hôte.
        self.config_manager.delete_host(hostname)
        self.saves_manager.remove_save_file(hostname)
        self.html_manager.delete_html_file(hostname)

        #Stop le thread associé à l'hôte.
        #Supprime le thread associé à l'hôte.
        """self.threads[self.get_thread_index(hostname)].stop_thread"""
        """del self.threads(self.get_thread_index(hostname))"""

    #Permet de modifier un hôte
    def modify_host(self, hostname, new_ip = -1, new_community = -1, new_monitor = -1):
        self.config_manager.modify_host(hostname, new_ip, new_community, new_monitor)
    
    #Retourne la configuration de tous les hôtes.
    def get_hosts_info(self):
        return self.config_manager.get_hosts_info()

    #Retourne tous les hôtes déclarés dans le fichier de configuration.
    def get_hosts(self):        
        return self.config_manager.get_hosts()
    
    #Retourne la configuration d'un hôte passé en paramétre.
    def get_host_info(self, hostname):
        
        #Récupérartion de la configuration de tous les hôtes.
        hosts_info = self.get_hosts_info()
        host_info = ''
        
        #Récupération des informations de l'hôte passé en paramétre.
        for i in hosts_info:
            if i['Hostname'] == hostname:
                host_info = i
        
        return host_info

    #Retourne toutes les données sauvegardées pour un hôte.
    def get_saves_of_host(self, hostname):
        
        #Récupération du contenu du fichier de sauvgarde pour un hôte.
        #Formatage des données.
        save_file_content = self.saves_manager.read_save_file(hostname)
        response = self.saves_manager.parse_save_data(save_file_content)
        
        return response

# =============================================================================
# Gestion des Threads
# =============================================================================

    #Démarrage des requêtes SNMP.
    def start_app(self):
        
        #Récupération des hôtes.
        hosts = self.get_hosts()
        
        #Création des treads pour chaque hôte déclarés.
        for host in hosts:
            self.threads.append(thread_manager(self.get_host_info(host)))
                
        #Démarrage de tous les treads.
        for thread in self.threads:
            thread.start()
    
    #Arrêt des requêtes SNMP.
    def stop_app(self):

        #Arrêt des treads
        for thread in self.threads:
            
            #Arrêt des threads.
            #Destruction des threads.
            thread.stop_thread()
            thread.join()
        
        #Suppression des données de la liste
        self.threads.clear()
    
    #Démarre le dernier thread créée.
    def start_new_thread(self):
        
        #localisation du dernier thread créée.
        #Démarre le dernier thread créée.
        index = len(self.threads) - 1
        self.threads[index].start()
        
        #Affichage des logs : Lancement du thread n°x.
        print(f"{self.current_time()} Thread {index} launched.")
    
    #Récuperation de l'index d'un thread en fonction de l'hôte passé en paramètre.
    def get_thread_index(self, hostname):
        pass

# =============================================================================
# Fonctions utilitaires
# =============================================================================
    
    #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())