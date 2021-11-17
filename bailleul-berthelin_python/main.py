import requests
import json
from requests.models import RequestEncodingMixin

from DICT_DEP import departement_dict
from NB_COMMUNES_PAR_DEPARTEMENT import nb_communes_par_dep as nbCparD
#import urllib.request


def remplir_dict_avec_villes(dep_dict, data_utile, nb_villes):
    """
        Exemple :
        dd == {'1' : ['ville1', 'ville2']}
        dd['1']
        Renvoie ['ville1', 'ville2']

        dd['1'].append("ville3")
        dd['1']
        Renvoie ['ville1', 'ville2', 'ville3']
    """
    # de 0 à n-1  # Remplacer par nb_villes si différent de nb_villes
    for i in range(nb_villes):
        codecommune = data_utile[i]["fields"]["code_commune"]
        nomcommune = data_utile[i]["fields"]["nom_commune"]
        codedepartement = codecommune[0:2]

        # Ajoute la ville dans la liste associée au département
        try:
            # Métropole
            if codedepartement != '97':
                dep_dict[codedepartement].append(nomcommune)
                continue

            # Outre-Mer
            codeoutremer = codecommune[0:3]
            dep_dict[codeoutremer].append(nomcommune)

        # Si le code département n'a pas de sens
        except KeyError:
            print("\n\n\nBug ici\n\n\n")
            breakpoint()

    return dep_dict


def pourcent_ville_defavorisee_par_dep(dep_dict):
    """

    """
    pourcent_dict = dict()

    for numero_dep in dep_dict.keys():
        nb_defa = len(dep_dict[numero_dep])
        nb_comm = nbCparD[numero_dep]
        pourcent_dict[numero_dep] = round(float(nb_defa)*100 / float(nb_comm), 2)
    # itère sur tous les départements
    # for i in dep_dict:
    #     numero_dep = str(i).zfill(2)
    #     nb_defa = len(dep_dict[numero_dep])
    #     nb_comm = nbCparD[numero_dep]
    #     pourcent = round(float(nb_defa*100 / float(nb_comm)), 2)
    #     pourcent_dict[numero_dep] = pourcent

    return pourcent_dict


def main():

   
    LIEN = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=liste-des-communes-classees-en-zones-defavorisees-au-1er-janvier-2017&q=&rows=9336&refine.zone_defavorisee_simple_fr=ZDS"
    json_brut = json.loads(requests.get(LIEN).text)

    # Définition des constantes et déclaration des listes
    NB_VILLES = json_brut["nhits"]
    DATA_UTILE = json_brut["records"]

    # Remplacer nb_ville=200 par NB_VILLES à la fin
    # (9336 villes = trop de data pour les tests)
    departement_dictM = remplir_dict_avec_villes(
        departement_dict, DATA_UTILE, NB_VILLES)

    #for i in departement_dict.keys():
    #    if(len(departement_dict.get(i)) == 0):
      #      print(i)

    pourcent_defavorise = pourcent_ville_defavorisee_par_dep(departement_dictM)
    for le_dep in pourcent_defavorise:
        print(le_dep + " : " + str(pourcent_defavorise.get(le_dep,"not exist, too bad jajaja")))
    #print(pourcent_defavorise)
# end main


"""
    Utilisation des dictionnaires
    Exemple :
        '03053' : 'CHANTELLE'
        communes_dict.get('81159', 'key not in dict'))
        Renvoie 'MASSAC-SERAN'"""

"""
    A FAIRE PLUS TARD (coordonnées GPS)
    # Récupérer les données géographiques des communes via code insee
    for codeinsee in communes_dict.items():
        print(codeinsee[0])
        #url_json_dep = "https://geo.api.gouv.fr/communes?code={codeinsee[0]}&fields=nom,code,codesPostaux,codeDepartement,codeRegion,population&format=geojson&geometry=contour"
        #url_json_dep_truc = json.loads(requests.get(url_json_dep).text)"""


# Run
if __name__ == "__main__":
    main()
# end
