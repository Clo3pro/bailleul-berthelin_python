from collections import namedtuple
import csv
import json


def build_stations_dict(filename):
    with open('C:/Users/valen/Desktop/E2/Python/Python/data/' + filename, 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=';')
        l = list(r)
    l[0].remove("Nom")
    Meteo = namedtuple('Station', l[0])
    d = dict()
    l.remove(l[0])
    oui = " "
    for i in l:
        oui = i.pop(1)
        d[oui] = Meteo(i[0], i[1], i[2], i[3])
    return d


if __name__ == '__main__':
    # votre code de test ici...
    d = build_stations_dict('stations-meteo.csv')
    print(d['NICE'])
    print(d['BELLE ILE-LE TALUT'])
    print(d['CAYENNE-MATOURY'])
    print(d['NICE'].ID)
    print(d['NICE'].Latitude)
    print(d['NICE'].Longitude)
    print(d['NICE'].Altitude)
    print('Writing JSON...')
    with open('stations-meteo.json', 'w') as jsonfile:
        json.dump(d, jsonfile)
    print('Done !')

# print(build_stations_dict("stations-meteo.csv"))
