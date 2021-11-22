# -*- coding: utf-8 -*-
"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 24/09/2021
Descripton : Module de gestion des threads. Contient les fonctions permettant de gérer threads.
"""

#Import des dépendances.
import datetime, os, threading,time
from saves_manager import saves_manager

#Gestionnaire des modules d'interogation des équipements.
class thread_manager(threading.Thread):

# =============================================================================
# Constructeur
# =============================================================================   
    def __init__(self,host):
        
        #Initialisation du Thread
        #Initialisation du chemin des modules
        #Mise à jour de la variable locale
        #Initialisation du saves_manager
        threading.Thread.__init__(self)
        self.script_path = '../Modules/'
        self.host = host
        self.saves_manager = saves_manager
        
        #Affichage des logs: Création d'un thread manager
        print(self.current_time() + " Object thread_manager created.")

# =============================================================================
# Fonctions principales
# =============================================================================
    
    # Lance le thread 
    def run(self):
        
        #Boucle infini
        while True :

            #Récupération d'une liste de datas  (retour de la fonction module_launcher du check_manager)
            #Lancement de la fonction add_save du save_manager qui écrit les datas recupérées dans le fichier de sauvegarde
            data = self.module_launcher(self.host['Ip'], self.host['Community'], self.host['Monitor'])
            self.saves_manager.add_save(self.host['Hostname'],self.host['Monitor'], data)
            
            #Attente de 5 secondes entre chaque requêtage 
            time.sleep(5)
    
    #Permet de lancer les modules d'interogation des équipements.
    def module_launcher(self, ip, community, monitor):
        
        #Initialisation de la variable data
        data = []
        
        #Boucle for pour chaque index dans monitor 
        for mon in monitor:
            
            #Traitement du chemin
            path = f'{self.script_path}{mon}.py'
            
            #lancement du module
            data.append(self.python_launcher(path,ip,community))
        
        #Retourne une liste 
        return data                     
            
    #Permet d'executer un module python
    def python_launcher(self,path,ip,community):
        
        #Initialisation du chemin des scripts python
        #Lancement du script python
        cmd = f"python {path} {ip} {community}"
        output = str.split(os.popen(cmd).read(),'\n')
        
        #Traitement des données
        del output[3]
        
        #Retour
        return output

# =============================================================================
# Fonctions utilitaires
# =============================================================================
        
    #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.datetime.today())