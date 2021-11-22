# -*-coding:Latin-1 -* 
"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 20/09/2021
Descripton : Module d'interrogation d'utilisation de la RAM.
"""

#Import des dépendances.

from pysnmp.hlapi import *
import sys
from datetime import datetime

#Module d'interrogation d'utilisation de la RAM 
class ram():

# =============================================================================
# Constructeur
# =============================================================================

    def __init__(self):
        pass

# =============================================================================
# Fonctions principales
# =============================================================================

    #Interroge l'équipement, retourne l'utilisation de la ram, la date et l'heure.
    def check_ram_usage(self,ip,community):
        
        # OID de l'utilisation de la ram 
        oid = '1.3.6.1.4.1.2021.4.6.0' 
       
        #Formatage de la requete snmp
        #Requete snmp pour récupérer l'utilisation de la ram
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
        result = f"ram\n{result}\n{date[0]}"
        print(result)
        
    #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())
        
      
# =============================================================================
# Fonctions utilitaires
# =============================================================================

#récupération des arguments
args = sys.argv

#creation de l'objet ram et appel de la fonction avec les bons arguments
ram_usage = ram()
ram_usage.check_ram_usage(args[1],args[2]) 




