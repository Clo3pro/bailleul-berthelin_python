import csv
import requests
import json
from requests.models import RequestEncodingMixin

from DICT_DEP import departement_dict
from NB_COMMUNES_PAR_DEPARTEMENT import nb_communes_par_dep as nbCparD

from datetime import datetime

LIEN = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=liste-des-communes-classees-en-zones-defavorisees-au-1er-janvier-2017&q=&rows=9336&refine.zone_defavorisee_simple_fr=ZDS"



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



def create_dict_annees(json_brut, nb_villes):
    """
    {ville1 : année, ville2 : année ...}
    """
    annees_dict = dict()
    for ville_index in range(nb_villes):
        nom_ville = json_brut['records'][ville_index]['fields']['nom_commune']
        try:
            if(nom_ville not in annees_dict.keys()):
                annees_dict[nom_ville] = (json_brut['records'][ville_index]['fields']['date_de_decision_france_4']).split('-')[0]
            continue
        except KeyError: # suite
            try:
                if(nom_ville not in annees_dict.keys()):
                    annees_dict[nom_ville] = (json_brut['records'][ville_index]['fields']['date_de_decision_france_3']).split('-')[0]
                continue
            except KeyError: # suite
                try:
                    if(nom_ville not in annees_dict.keys()):
                        annees_dict[nom_ville] = (json_brut['records'][ville_index]['fields']['date_de_decision_france_2']).split('-')[0]
                    continue
                except KeyError: # suite
                    try:
                        if(nom_ville not in annees_dict.keys()):
                            annees_dict[nom_ville] = (json_brut['records'][ville_index]['fields']['date_de_decision_france_1']).split('-')[0]
                        continue
                    except KeyError:
                        # Pas de date équivaut à une commune non défavorisée
                        continue
    return annees_dict



def annees_entreefunction(dep_dict, dict_annees):
    dict_des_entrees_dans_defa = dict()
    for nomville in dict_annees.keys():
        for dep in dep_dict.keys():
            if(nomville in dep_dict[dep]):
                dict_des_entrees_dans_defa[nomville] = dict_annees[nomville]
                continue
    return dict_des_entrees_dans_defa



def nb_villes_par_annees(dict_annees):
    nb_ville_par_annee = {
        '1970-1975': 0,
        '1975-1980': 0,
        '1980-1985': 0,
        '1985-1990': 0,
        '1990-1995': 0,
        '1995-2000': 0,
        '2000-2005': 0,
        '2005-2010': 0,
        '2010-2015': 0,
        '2015-2020': 0,
    }

    for nomville in dict_annees.keys():
        annee = int(dict_annees[nomville])
        if 1970 < annee <= 1975:
            nb_ville_par_annee['1970-1975'] += 1
        elif 1975 < annee <= 1980:
            nb_ville_par_annee['1975-1980'] += 1
        elif 1980 < annee <= 1985:
            nb_ville_par_annee['1980-1985'] += 1
        elif 1985 < annee <= 1990:
            nb_ville_par_annee['1985-1990'] += 1
        elif 1990 < annee <= 1995:
            nb_ville_par_annee['1990-1995'] += 1
        elif 1995 < annee <= 2000:
            nb_ville_par_annee['1995-2000'] += 1
        elif 2000 < annee <= 2005:
            nb_ville_par_annee['2000-2005'] += 1
        elif 2005 < annee <= 2010:
            nb_ville_par_annee['2005-2010'] += 1
        elif 2010 < annee <= 2015:
            nb_ville_par_annee['2010-2015'] += 1
        elif 2015 < annee <= 2020:
            nb_ville_par_annee['2015-2020'] += 1
        else:
            breakpoint()

    return nb_ville_par_annee



def create_csv_annees(annees_entree_dict):
    with open('./nombre_ville_ajoutees_par_periode.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['Periode entree', 'Nombre de villes ajoutees cette periode']
        )
        for k, v in annees_entree_dict.items():
            writer.writerow([k, v])



def pourcent_ville_defavorisee_par_dep(dep_dict):
    pourcent_dict = dict()
    for numero_dep in dep_dict.keys():
        nb_defa = len(dep_dict[numero_dep])
        nb_comm = nbCparD[numero_dep]
        pourcent_dict[numero_dep] = round(
            float(nb_defa) * 100 / float(nb_comm), 2)
    return pourcent_dict



def create_csv_file(pourcent_defavorise):
    with open('./pourcent_defavorise.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['Departement', 'Pourcentage communes defavorisees', 'Nombre total communes', 'Nombre communes defavorisees'])
        for k, v in pourcent_defavorise.items():
            writer.writerow([k, v, nbCparD[k], int(nbCparD[k]*pourcent_defavorise[k]/100)])



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
    with open('./pourcent_defavorise.csv', newline='') as csv_file:
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
            
    return myRangeDict



def recup_insee_via_ville( DATA_UTILE, NB_VILLES):
    dict_ville_insee = dict()
    for i in range(NB_VILLES):
        codecommune = DATA_UTILE[i]["fields"]["code_commune"]
        nomcommune = DATA_UTILE[i]["fields"]["nom_commune"]
        dict_ville_insee[nomcommune] = codecommune
    return dict_ville_insee



def write_geojson(my_geojson, dep, nb_ville, i_ville):
    try :
        codeinsee = int(dep[1]) # important

        url_json_dep = f"https://geo.api.gouv.fr/communes?code={codeinsee}&fields=nom,code,codesPostaux,codeDepartement,codeRegion,population&format=geojson&geometry=contour"
        json_commune = json.loads(requests.get(url_json_dep).text)
        
        geometry_ville  = json_commune["features"][0]["geometry"]["coordinates"][0]
        
        # "type": "Feature",
        my_geojson.write('\t\t{\n')
        my_geojson.write('\t\t\t"type" : "Feature",\n')

        #"properties": {
        my_geojson.write('\t\t\t"properties" : {\n')
        my_geojson.write('\t\t\t\t"nom": "' + json_commune["features"][0]["properties"]["nom"] + '",\n')
        my_geojson.write('\t\t\t\t"code": "' + json_commune["features"][0]["properties"]["code"] + '",\n')
        my_geojson.write('\t\t\t\t"codesPostaux": "' + json_commune["features"][0]["properties"]["codesPostaux"][0] + '",\n')
        my_geojson.write('\t\t\t\t"codeDepartement": "' + json_commune["features"][0]["properties"]["codeDepartement"] + '",\n')
        my_geojson.write('\t\t\t\t"codeRegion": "' + json_commune["features"][0]["properties"]["codeRegion"] + '",\n')
        my_geojson.write('\t\t\t\t"population": "' + str(json_commune["features"][0]["properties"]["population"]) + '"\n')
        my_geojson.write('\t\t\t},\n')

        #"geometry"
        my_geojson.write('\t\t\t"geometry": {\n')
        my_geojson.write('\t\t\t\t"type": "' + json_commune["features"][0]["geometry"]["type"] + '",\n')
        my_geojson.write('\t\t\t\t"coordinates":\n')
        my_geojson.write('\t\t\t\t[\n')
        my_geojson.write('\t\t\t\t\t[\n')


        taille = len(geometry_ville)
        i = 1
        for localisation in geometry_ville:
            my_geojson.write('\t\t\t\t\t\t[\n')

            my_geojson.write('\t\t\t\t\t\t\t' + str(localisation[0]) + ',\n')
            my_geojson.write('\t\t\t\t\t\t\t' + str(localisation[1]) + '\n')
            
            if i != taille :
                my_geojson.write('\t\t\t\t\t\t],\n')
            else :
                my_geojson.write('\t\t\t\t\t\t]\n')

            i += 1



        my_geojson.write('\t\t\t\t\t]\n')
        my_geojson.write('\t\t\t\t]\n')
        my_geojson.write('\t\t\t}\n')

        if i_ville != nb_ville :
            my_geojson.write('\t\t},\n')
        else:
            my_geojson.write('\t\t}\n')
            return

        i_ville += 1
        

    except IndexError:
        i_ville += 1
        return



def ecrire_geojson_via_code_insee(dict_ville_insee_dep_plus_touche):
        dict_ville_position = dict()

        print("\tDébut d'écriture du GeoJSON...")
        debut = datetime.now()


        with open('./location_ville.geojson', 'w') as my_geojson:
            my_geojson.write('{\n')
            my_geojson.write('\t"type": "FeatureCollection",\n')
            my_geojson.write('\t"features":\n')
            my_geojson.write('\t[\n')



            nb_ville = len(dict_ville_insee_dep_plus_touche.items())
            i_ville = 1

            for dep in dict_ville_insee_dep_plus_touche.items():
                write_geojson(my_geojson, dep, nb_ville, i_ville)


            my_geojson.write('\t]\n')
            my_geojson.write('}')


        fin = datetime.now()
        total = fin - debut
        total_seconds = total.total_seconds()
        print(f"\tTerminé.\n\tDurée de traitement : {total_seconds} secondes.\n")

        return dict_ville_position



def recup_dep_le_plus_touche(pourcent_defavorise):
    max = 0
    dep_max = ''
    for dep in pourcent_defavorise.items():
        if max < dep[1]:
            max = dep[1]
            dep_max = dep[0]
    return dep_max



def recup_insee_dep_touche(dict_ville_insee, dep_plus_touche):
    dict_ville_insee_plus_touche = dict()
    for ville in dict_ville_insee.items():
        dep_actuel = (ville[1])[0:2]
        if dep_actuel == dep_plus_touche:
            nomville = ville[0]
            codeinsee = ville[1]
            dict_ville_insee_plus_touche[nomville] = codeinsee
    return dict_ville_insee_plus_touche



def main():
    json_brut = json.loads(requests.get(LIEN).text)

    # Définition des constantes et déclaration des listes
    NB_VILLES = json_brut["nhits"]
    DATA_UTILE = json_brut["records"]

    departement_dictM = remplir_dict_avec_villes(departement_dict, DATA_UTILE, NB_VILLES)
    

    dict_annees = create_dict_annees(json_brut, NB_VILLES)
    annees_entreefunction(departement_dictM, dict_annees)


    pourcent_defavorise = pourcent_ville_defavorisee_par_dep(departement_dictM)
    create_csv_file(pourcent_defavorise)

    
    nb_villes_annees = nb_villes_par_annees(dict_annees)
    create_csv_annees(nb_villes_annees)



    dict_ville_insee = recup_insee_via_ville(DATA_UTILE, NB_VILLES)

    dep_plus_touche = recup_dep_le_plus_touche(pourcent_defavorise)
    dict_ville_insee_dep_plus_touche = recup_insee_dep_touche(dict_ville_insee, dep_plus_touche)
    ecrire_geojson_via_code_insee(dict_ville_insee_dep_plus_touche)


if __name__ == "__main__":
    main()
