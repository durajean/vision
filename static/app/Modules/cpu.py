# -*-coding:Latin-1 -* 
"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 20/09/2021
Descripton : Module d'interrogation d'utilisation CPU.
"""

#Import des dépendances.

from pysnmp.hlapi import *
import sys
from datetime import datetime

#Module d'interrogation d'utilisation CPU.
class cpu():

# =============================================================================
# Constructeur
# =============================================================================

    def __init__(self):
        pass

# =============================================================================
# Fonctions principales
# =============================================================================

    #Interroge l'équipement, retourne le % de cpu, la date et l'heure.
    
    def check_cpu_usage(self,ip,community):
        
        # OID du % de CPU utilisé
        oid = '1.3.6.1.4.1.2021.11.10.0' 
       
        #Formatage de la requete snmp
        #Envoie de la requete snmp pour récupérer le % de CPU utilisé
        #Gestion du retour et des erreurs
        g = nextCmd(SnmpEngine()
                        , CommunityData(community, mpModel=1)
                        , UdpTransportTarget((ip, 161)) # demo.snmplabs.com
                        , ContextData()
                        , ObjectType(ObjectIdentity(oid))) # octect IN

        errorIndication, errorStatus, errorIndex, varBinds = next(g)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint()
                , errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )
        )
        else:
            for varBind in varBinds:
                resultoid = ('='.join([x.prettyPrint() for x in varBind]))
       
        #Séparation du résultat en une liste par le séparateur '='
        #Récupération de la donnée 
        result = str.split(resultoid, '=')
        result = result[1]
        
        #gestion de la date
        date = str.split(self.current_time(), '.')
        
        #Formatage du retour
        result = f"cpu\n{result}\n{date[0]}"
        print(result)
        
    #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())
        
      
# =============================================================================
# Fonctions utilitaires
# =============================================================================

#récupération des arguments
args = sys.argv

#création de l'objet cpu et appel de la fonction avec les bons arguments
cpu_usage = cpu()
cpu_usage.check_cpu_usage(args[1],args[2]) 