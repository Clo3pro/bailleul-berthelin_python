import csv
import requests
import json
from requests.models import RequestEncodingMixin

from DICT_DEP import departement_dict
from NB_COMMUNES_PAR_DEPARTEMENT import nb_communes_par_dep as nbCparD

LIEN = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=liste-des-communes-classees-en-zones-defavorisees-au-1er-janvier-2017&q=&rows=9336&refine.zone_defavorisee_simple_fr=ZDS"


def getcheminrelatif():
    return '/Users/cloeberthelin/labo_school/bailleul-berthelin_python/bailleul-berthelin_python/pourcent_defavorise.csv'
    # return "C:/Users/VALENTIN/Desktop/E3/python/bailleul-berthelin_python/bailleul-berthelin_python/pourcent_defavorise.csv"


CHEMIN_ABSOLU = getcheminrelatif()


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

    """
    # tests pour dep sans ville:
    for dep in list(dep_dict):
    if len(dep_dict[dep]) == 0:
    dep_dict.pop(dep)
    # breakpoint()
    """

    return dep_dict


def pourcent_ville_defavorisee_par_dep(dep_dict):
    """

    """
    pourcent_dict = dict()

    for numero_dep in dep_dict.keys():
        nb_defa = len(dep_dict[numero_dep])
        nb_comm = nbCparD[numero_dep]
        pourcent_dict[numero_dep] = round(
            float(nb_defa) * 100 / float(nb_comm), 2)

    return pourcent_dict


def create_csv_file(pourcent_defavorise):
    with open(CHEMIN_ABSOLU, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['Departement', 'Pourcentage communes defavorisees'])
        for k, v in pourcent_defavorise.items():
            writer.writerow([k, v])
    print(f'Ecriture terminée')


def pourcentage_de_communes_défa_par_dép_selon_range_0_25_50_75_100():
    """
    y= pourcentage de communes défa par dép en fct de x= range 0/25/50/75/100
    """
    myRangeDict = {
        '0': 0,
        '0-25': 0,
        '25-50': 0,
        '50-75': 0,
        '75-100': 0
    }
    with open(CHEMIN_ABSOLU, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            dep = row['Departement']
            val = float(row['Pourcentage communes defavorisees'])

            if val == 0:
                myRangeDict['0'] += 1
            elif 0 < val <= 25:
                myRangeDict['0-25'] += 1
            elif 25 < val <= 50:
                myRangeDict['25-50'] += 1
            elif 50 < val <= 75:
                myRangeDict['50-75'] += 1
            elif 75 < val <= 100:
                myRangeDict['75-100'] += 1
            else:
                print(f"dep:{dep} ; val:{val}")
    print(myRangeDict)
    print(
        f"Somme = {myRangeDict['0'] + myRangeDict['0-25'] + myRangeDict['25-50'] + myRangeDict['50-75'] + myRangeDict['75-100']}")

    # print(row['Pourcentage communes defavorisees'])


def main():
    json_brut = json.loads(requests.get(LIEN).text)

    # Définition des constantes et déclaration des listes
    NB_VILLES = json_brut["nhits"]
    DATA_UTILE = json_brut["records"]

    departement_dictM = remplir_dict_avec_villes(
        departement_dict, DATA_UTILE, NB_VILLES)

    pourcent_defavorise = pourcent_ville_defavorisee_par_dep(departement_dictM)

    create_csv_file(pourcent_defavorise)
    pourcentage_de_communes_défa_par_dép_selon_range_0_25_50_75_100()


# end main


"""
A FAIRE PLUS TARD (coordonnées GPS)
# Récupérer les données géographiques des communes via code insee
for codeinsee in communes_dict.items():
    print(codeinsee[0])
    # url_json_dep = "https://geo.api.gouv.fr/communes?code={codeinsee[0]}&fields=nom,code,codesPostaux,codeDepartement,codeRegion,population&format=geojson&geometry=contour"
    # url_json_dep_truc = json.loads(requests.get(url_json_dep).text)
"""

# Run
if __name__ == "__main__":
    main()
# end
