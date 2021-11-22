# -*-coding:Latin-1 -* 
"""
Auteurs : Maude RIBOT, Jean DURAND
Date : 20/09/2021
Descripton : Module d'interrogation du nombre d'octect sur une interface.
"""

#Import des dépendances.

from datetime import datetime
from pysnmp.hlapi import *
import sys

#Module d'interrogation du nombre d'octect sur une interface
class interface():

# =============================================================================
# Constructeur
# =============================================================================

    def __init__(self):
        pass

# =============================================================================
# Fonctions principales
# =============================================================================

    #Interroge l'équipement, retourne le débit de l'interface, la date, l'heure et le nombre d'octect sur l'interface.
    
    def check_interface_usage(self,ip,community):
        
        # OID du nombre octect qui entre sur l'interface
        oid = '1.3.6.1.2.1.2.2.1.10' 
        
        #Formatage de la requete snmp
        #Requete snmp pour récupérer le nombre octect sur l'interface
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
        
        #Gestion de la date
        date = str.split(self.current_time(), '.')
        
        #Formatage du retour
        result = f"interface\n{result}\n{date[0]}"
        print(result) 
        
       #Retourne la date et l'heure.
    def current_time(self):
        return str(datetime.now())
        
       
# =============================================================================
# Fonctions utilitaires
# =============================================================================


#récupération des arguments
args =sys.argv

#creation de l'objet interface et l'appel de la fonction avec les bons arguments
interface_int = interface()
interface_int.check_interface_usage(args[1],args[2]) 