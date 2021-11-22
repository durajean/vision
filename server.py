# -*- coding: utf-8 -*-

"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 20/09/2021
Descripton : Serveur Flask pour l'application Vision.
"""

#import des dépendances
from flask import Flask, render_template, request, redirect
import sys

#import du contrôlleur
sys.path.append("static/app/Lib/")
from master_manager import master_manager

#Création de l'objet Flask
app = Flask(__name__)

# =============================================================================
# Routes statiques
# =============================================================================

@app.route('/')
@app.route('/home')
def home():
    return render_template('/html/home.html')

@app.route('/start')
def start():

    #Lancement des thread.
    master_manager.start_app()

    return redirect("/home")

@app.route('/stop')
def stop():

    #Arrêt des threads.
    master_manager.stop_app()

    return redirect('/home')

@app.route('/dashboard')
def dashboard():
    
    #Retourne tous les hôtes déclarés dans le fichier de configuration.
    devices = master_manager.get_hosts()
    
    return render_template('/html/dashboard.html', devices = devices)

@app.route('/dashboard-view', methods = ['POST'])
def dashboard_view():
    
    hostname = request.form['hostname']
    
    data = master_manager.get_saves_of_host(hostname)
    
    return render_template(f'/html/{hostname}.html', hostname = hostname, data = data)

@app.route('/contact')
def contact():
    return render_template('/html/contact.html')

@app.route('/monitoring_devices')
def monitoring_devices():
    
    #Récupère les informations des hôtes.
    devices = master_manager.get_hosts_info()
    
    return render_template('/html/monitoring_devices.html', devices = devices)

@app.route('/about')
def about():
    return render_template('/html/about.html')

@app.route('/users')
def users():
    return render_template('/html/users.html')

@app.route('/new_host')
def new_host():
    return render_template('/html/new_host.html')

@app.route('/success_new_host', methods = ['POST'])
def success_new_host():
    
    rqt = request.form
    monitor = []
    
    #A modifer => récupérer les "possible_monitors".
    if "cpu" in rqt:
        monitor.append(rqt['cpu'])
    
    if "ram" in rqt:
        monitor.append(rqt['ram'])
    
    if "disk" in rqt:
        monitor.append(rqt['disk'])
        
    if "interfaces" in rqt:
        monitor.append(rqt['interfaces'])

    #Ajout de l'hôte dans l'application.
    master_manager.add_host(rqt['hostname'], rqt['ip'],rqt['community'], monitor)
   
    return render_template('/html/success_new_host.html', hostname = rqt['hostname'])

@app.route('/success_delete_host', methods = ['POST'])
def success_delete_host():
    
    #Récupération du hostname.
    #Suppression de l'hôte.
    hostname = request.form['hostname']
    master_manager.delete_host(hostname)
    
    return render_template('/html/success_delete_host.html', hostname = hostname)

# =============================================================================
# main
# =============================================================================
if __name__ == "__main__":
    
    #Création du contrôleur
    master_manager = master_manager("static/app/Data/startup_config.json","static/app/Saves/","templates", "templates/html")
    
    #Lancement du serveur.
    app.run()
