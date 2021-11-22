# -*-coding:Latin-1 -* 

"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 15/11/2021
Descripton : Module de gestion du fichier des sauvegardes. Contient l'ensemble des fonctions permettant de gérer les fichiers sauvegardes.
"""

#Import des dépendances.
import os
import json
from datetime import datetime

#Module de gestion du fichier des sauvegardes.
class saves_manager():

# =============================================================================
# Constructeur
# =============================================================================
    def __init__(self, save_directory = '../Saves'):
        
        #Initialisation du save_manager
        self.save_directory = save_directory
        
        #Affichage des logs: Création d'un saves_manager
        print(self.current_time() + " Object saves_manager created.")
        
# =============================================================================
# Fonctions principales
# =============================================================================
    
    #Permet d'ajouter des données dans le fichier de sauvegarde
    def add_save(self, hostname,monitor, data):
        
        #Lecture du fichier de sauvegarde
        #Initialisation de la variable locale
        file_content = self.read_save_file(hostname)
        index= -1
        
        #Modification du fichier de sauvegarde
        #Boucle for, pour chaque index dans monitor
        for mon in monitor:
            
            #Boucle for, pour chaque index dans data
            for i in data:
                
                #Incréménation de la variable index
                #Condition si l'index est égal au monitor 
                index = index + 1
                if i[0] == mon:
                    
                    #Ajout des données dans les fichiers de sauvegarde
                    file_content['saves'][monitor.index(mon)]['componentsaves']['data'].append(int(data[index][1]))
                    file_content['saves'][monitor.index(mon)]['componentsaves']['time'].append(data[index][2])
                    break             
    
        #Ecriture du fichier de sauvegarde
        self.saves = file_content
        self.write_saves(self.parse_file_path(hostname))
        

    #Permet de créer les fichiers de sauvegardes.
    def create_save_file(self, hostname, monitors):
        
        #Initialisation de la variable local 
        file_path = self.parse_file_path(hostname)
        
        #Condition: si le fichier n'existe pas 
        if not self.is_save_exist(hostname):

            data = {
                    'Hostname': hostname,
                    'saves': []
            }
            
            for monitor in monitors:
                
                monitor = {
                        'name': monitor,
                        "componentsaves":{
                                "data":[],
                                "time":[]
                        }
                }
                
                data['saves'].append(monitor)
            
            #Création du fichier de sauvegarde et écriture du modèle de donné dans un nouveau fichier
            self.saves = data
            self.write_saves(file_path)
            
    #Permet d'écrire dans les fichiers de sauvegarde.
    def write_saves(self, file_path):
        
        #Formate les données du dicionaire en json 
        json_data = json.dumps(self.saves,ensure_ascii=False, indent=4)	
        
        #Ouverture du fichier
        #Ecriture des données json dans le fichier 
        #Fermeture du fichier
        config_file = open(file_path,'w')
        config_file.write(json_data)
        config_file.close()

        #Affichage des logs: Les données ont été sauvegardées
        print(self.current_time() + " Datas had been saved.")
        
    #Permet de supprimer les fichiers de sauvegardes.        
    def remove_save_file(self,hostname):
        
        #Si le fichier exist
        if self.is_save_exist(hostname):
            
            #Suppression du fichier
            os.remove(self.parse_file_path(hostname))
            
            #Affichage des logs: Le fichier a été supprimé
            print(self.current_time() + "Save file removed.")
            
        else:
            #Affichage des logs: Le fichier n'a pas pu être supprimé, fichier non trouvé
            print(self.current_time() + "Can't remove save file : File not found")
            
    #Permet de lire les fichiers de sauvegardes.
    def read_save_file(self, hostname):
        
        #Initialisation de la variable locale
        reponse = ""
        
        #Ouverture du fichier
        #Lecture du fichier
        #Fermeture du fichier
        file = open(f"{self.save_directory}/{hostname}.json", 'r')
        reponse = json.load(file)
        file.close()
        
        return reponse

    #Permet de traiter les données du fichier de sauvegarde.
    def parse_save_data(self, save):
        
        #Initialisation des variables
        response = {}
        save = save['saves']
        
        #Boucle for, index dans save
        for i in save :
            
            #Récupère les données sauvegardées
            response[i['name']] = i['componentsaves']
        
        return response
    
# =============================================================================
# Fonctions utilitaires
# =============================================================================
        
     #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())
    
    #Retourne le chemin du fichier de sauvegarde.
    def parse_file_path(self,hostname):
        return self.save_directory+ "/" + hostname + '.json'
    
    #Retourne si le fichier de sauvegarde de l'hôte existe 
    def is_save_exist(self,hostname):
        
        #Initialisation de la variable
        #Récupère la liste des fichiers dans le repertoire de sauvegarde
        response = False
        list_of_saves = os.listdir(self.save_directory)
        
        #Condition: Si  le fichier existe retoune true
        if hostname + ".json" in list_of_saves:
            response = True
            
        return response 