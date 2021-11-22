# -*-coding:Latin-1 -* 

"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 17/09/2021
Descripton : Module de gestion du fichier de configuration. Contient les fonctions permettant de gérer le fichier de configuration.
"""

#Import des dépendances.
import json
from datetime import datetime

#Module de gestion du fichier de configuration.
class config_manager():

# =============================================================================
# Constructeur
# =============================================================================
    def __init__(self,config_file_path = '../Data/startup_config.json'):
		
        #Initialisation de la localisation du fichier de configuration.
        #Mise à jour de la variable locale.
        self.config_file_path = config_file_path
        self.update()
        
        #Affichage des logs : Création du gestinaire de fichier de configuration.
        print(self.current_time() + " Object config_manager created.")

# =============================================================================
# Fonctions principales
# =============================================================================
	#Permet d'ajouter un hôte.
    def add_host(self, hostname, ip, community, monitor):
		
        #Préparation de la nouvelle entrée.
        new_host = {
			'Hostname': hostname,
			'Ip': ip,
			'Community': community,
			'Monitor': monitor
		}

        #Test : si l'hôte n'existe pas alors,
        if not self.is_exist(hostname):

            #Ajout de la nouvelle entrée dans la variable local.
            #Sauvegarde de la configuration.
            self.config['Hosts'].append(new_host)
            self.write_config()
            
            #Affichage des logs : L'hôte a été ajouté.
            print(self.current_time() + " Host " + hostname + " has been added.")
        else:

            #Affichage des logs : L'hôte existe déjà.
            print(self.current_time() + " Host " + hostname + " already exist.")
            
	#Permet de supprimer un hôte.
    def delete_host(self,hostname):
        
        #Test : si l'hôte existe alors,
        if self.is_exist(hostname):
            
            #Suppression de l'hôte de la variable locale.
            #Sauvgarde de la configuration.
            del self.config['Hosts'][self.get_index(hostname)]
            self.write_config()
            
            #Affichage des logs : L'hôte a été supprimé.
            print(self.current_time() + " Host " + hostname + " has been deleded.")
        else:

            #Affichage des logs : L'hôte n'a pas été trouvé.
            print(self.current_time() + " Host " + hostname + " not found.")
            
	#Permet de modifier un hôte.
    def modify_host(self, hostname, new_ip = -1, new_community = -1, new_monitor = -1):
        
        #Test : si l'hôte existe alors,
        if self.is_exist(hostname):
            
            #Localisation de l'hôte dans la variable locale.
            index = self.get_index(hostname)

            #Réécriture des éléments à modifier.
            if new_ip != -1 :
                self.config['Hosts'][index]['Ip'] = new_ip

            if new_community != -1 :
                self.config['Hosts'][index]['Community'] = new_community

            if new_monitor != -1 :
                self.config['Hosts'][index]['Monitor'] = new_monitor

            #Sauvgarde de la configuration.
            self.write_config()
            
            #Affichage des logs : L'hôte a été modifié.
            print(self.current_time() + " Host " + hostname + " has been modified.")
			
        else:

            #Affichage des logs : L'hôte n'a pas été trouvé.
            print(self.current_time() + " Host " + hostname + " not found.")
            
	#Permet d'écrire dans le fichier de configuration.
    def write_config(self):

        #Conversion du dictionnaire en données JSON.
        json_data = json.dumps(self.config,ensure_ascii=False, indent=4)	

        #Ouverture du fichier de configuration.
        #Ecriture dans le fichier de configuration.
        #Fermeture du fichier de configuration.
        config_file = open(self.config_file_path,'w')
        config_file.write(json_data)
        config_file.close()

        #Affichage des logs : La configuration a été sauvgardée.
        print(self.current_time() + " Configuration has been saved.")
        
	#Mise à jour de la variable locale.
    def update(self):
		
		#chargement du fichier de configuration		
        with open(self.config_file_path) as json_data:

            #Conversion des données JSON en dictionnaire.
            self.config = json.load(json_data)

        #Affichage des logs : La configuration a été chargée.
        print(self.current_time() + " Configuration loaded on config_manager.")

# =============================================================================
# Fonctions utilitaires
# =============================================================================
	#Retourne le fichier de configuration.	
    def read(self):
        return self.config

	#Retourne la liste des hôtes présent dans le fichier de configuration.
    def get_hosts(self):
        hosts = []

        #Récupération et sauvegarde des hôtes présent dans le fichier.
        for host in self.config['Hosts']:
            hosts.append(host['Hostname'])

        return hosts
    
    #Retournes les informations liés a chaque hôte.
    def get_hosts_info(self):
        return self.config['Hosts']

	#Retourne vrai si le hôte passé en paramètre est présent dans le fichier de configuration sinon retourne faux.
    def is_exist(self, hostname):
        
        #Récupération de la liste de tous les hôte présent dans le fichier de configuration.
        #Initialisation de la variable réponse à faux.
        hosts = self.get_hosts()
        is_exist = False

        #test : Si l'hôte est dans la liste alors,
        if hostname in hosts:

            #On retourne vrai.
            is_exist = True

        return is_exist

	#Retourne l'index de l'hôte passé en paramètre.
    def get_index(self,hostname):
        return self.get_hosts().index(hostname)

    #Retourne la date et l'heure courante.
    def current_time(self):
        return str(datetime.now())
    
    #Retourne la liste des éléments supervisés pour un host.
    def get_monitored_components(self,hostname):
        reponse = -1
        
        #Si l'hôte existe alors,
        if self.is_exist(hostname):

            #On récupère l'index.
            #On retourne les éléments monitorés.
            index = self.get_index(hostname)
            reponse = self.config['Hosts'][index]['Monitor']
            
        return reponse
    
    #Retourne la liste des éléments supervisés pour un host.
    def get_community(self,hostname):
        reponse = -1
        
        #Si l'hôte existe alors
        if self.is_exist(hostname):
            
            #On récupère l'index.
            #On retourne la communité.
            index = self.get_index(hostname)
            reponse = self.config['Hosts'][index]['Community']
            
        return reponse