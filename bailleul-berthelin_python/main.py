import csv
import requests
import json
from requests.models import RequestEncodingMixin

from DICT_DEP import departement_dict
from NB_COMMUNES_PAR_DEPARTEMENT import nb_communes_par_dep as nbCparD
LIEN = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=liste-des-communes-classees-en-zones-defavorisees-au-1er-janvier-2017&q=&rows=9336&refine.zone_defavorisee_simple_fr=ZDS"


def getcheminrelatif():
    try:
        with open('/Users/cloeberthelin/labo_school/bailleul-berthelin_python/bailleul-berthelin_python/pourcent_defavorise.csv', 'w'):
            cheminrelatif = "/Users/cloeberthelin/labo_school/bailleul-berthelin_python"
    except:
        cheminrelatif = "C:/Users/VALENTIN/Desktop/E3/python/bailleul-berthelin_python"
    return cheminrelatif


CHEMIN_RELATIF = getcheminrelatif()


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

    """# tests pour dep sans ville:
	for dep in list(dep_dict):
		if len(dep_dict[dep]) == 0:
			dep_dict.pop(dep)
			# breakpoint()"""

    return dep_dict


def pourcent_ville_defavorisee_par_dep(dep_dict):
    """

    """
    pourcent_dict = dict()

    for numero_dep in dep_dict.keys():
        nb_defa = len(dep_dict[numero_dep])
        nb_comm = nbCparD[numero_dep]
        pourcent_dict[numero_dep] = round(
            float(nb_defa)*100 / float(nb_comm), 2)

    return pourcent_dict


def create_csv_file(pourcent_defavorise):
    with open(CHEMIN_RELATIF+'/bailleul-berthelin_python/pourcent_defavorise.csv', 'w', newline='') as csv_file:
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
    with open(CHEMIN_RELATIF+'/bailleul-berthelin_python/pourcent_defavorise.csv', 'w') as csv_file:
        breakpoint()


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
