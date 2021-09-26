import json
import csv


def read_asset_list(file):
    """ function read in the json-file 'AssetListe.json and returns
        a list called asset_ids which contains all meter ids"""
    with open(file, 'r') as json_data:
        payload = json.load(json_data)
        asset_ids = []
        for household in payload['data']:
            if household['meterId'] != 'NO_METER_AVAILABLE':
                asset_ids.append(household['meterId'])

    return asset_ids


def generate_prosumer_keys(file):
    """ This function reads in a file called prosumer_Ids.csv
        It contains a list of all meterIds that are prosumer households
        in the BloGPV-Community
        """

    # getting Data out of csv file
    with open(file, 'r') as csv_file:
        csvReader = csv.reader(csv_file)

       #storing meterIds in a List
        prosumerList = []
        for i in csvReader:
            prosumerList.append(i[0])

    return prosumerList


def get_prosumer_ids():
    """ this function checks which prosumer Ids are also in AssetListe.json
        it returns a list called prosumerIds"""

    prosumerKeys = generate_prosumer_keys(file= 'prosumer_IDs.csv')
    prosumerIDs = list(set(prosumerKeys) & set(read_asset_list('AssetListe.json')))

    return prosumerIDs



def get_consumer_ids():
    """ This function returns a list of all households that are just consumers
        from AssetListe.json"""

    prosumerIDs = set(get_prosumer_ids())
    assetIDs = set(read_asset_list('AssetListe.json'))
    consumerIDs = list(assetIDs.difference(prosumerIDs))

    return consumerIDs


def get_prosumer_coordinates(file):
    """ This function reads the coordinates from all prosumerHouseholds
        from AssetListe.json

        It returns them in the python dictionary prosumer_coordinates
        key: prosumer-Id
        value: [langitude, longitude]"""

    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        prosumer_coordinates = {}

        for household in payload['data']:
            for k in get_prosumer_ids():
                if household['meterId'] == k:
                    prosumer_coordinates[k] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return prosumer_coordinates


def get_consumer_coordinates(file):
    """ This function reads the coordinates from all consumerHouseholds
        from AssetListe.json

        This function isnt needed!

        key: consumer-Id
        value: [langitude, longitude]"""

    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        consumer_coordinates = {}

        for household in payload['data']:
            for i in get_consumer_ids():
                if household['meterId'] == i:
                    consumer_coordinates[i] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return consumer_coordinates



def get_allHouseholds_coordinates(file):
    """ This function reads the coordinates from all Households
        from AssetListe.json

        It returns them in a dictionary

        key: consumer-Id
        value: [langitude, longitude]"""

    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        allHouseholds_coordinates = {}

        for household in payload['data']:
            if household['meterId'] != 'NO_METER_AVAILABLE':
                allHouseholds_coordinates[household['meterId']] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return allHouseholds_coordinates

