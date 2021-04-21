import json
import csv


""" this function read the json-file AssetListe.json

    it returns a list with alle meterIds in Asset-Liste.json"""
def read_asset_list(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)
        asset_ids = []
        for household in payload['data']:
            if household['meterId'] != 'NO_METER_AVAILABLE':
                asset_ids.append(household['meterId'])

    return asset_ids


""" This function reads in a file called prosumer_Ids.csv
    It contains a list of all meterIds that are prosumer households 
    in the BloGPV-Community
    """
def generate_prosumer_keys(file):
    # getting Data out of csv file
    with open(file, 'r') as csv_file:
        csvReader = csv.reader(csv_file)

       #storing meterIds in a List
        prosumerList = []
        for i in csvReader:
            prosumerList.append(i[0])
        return prosumerList

#keys_prosumer = generate_prosumer_keys('prosumer_IDs.csv')


""" this function checks which prosumer Ids are also in AssetListe.json.
    This has to be made as there are more prosumers on the API than in
    AssetListe.json
    
    It returns a list of all prosumderIds that are in AssetListe.json
    
    In total 14"""
def get_prosumer_ids():
    prosumerKeys = generate_prosumer_keys(file= 'prosumer_IDs.csv')
    prosumerIDs = list(set(prosumerKeys) & set(read_asset_list('AssetListe.json')))

    return prosumerIDs


""" This function returns a list of all households that are just consumers
    from AssetListe.json
    
    in total 78"""
def get_consumer_ids():

    prosumerIDs = set(get_prosumer_ids())
    assetIDs = set(read_asset_list('AssetListe.json'))
    consumerIDs = list(assetIDs.difference(prosumerIDs))

    return consumerIDs


#Funktion die prosumer-Koordinaten abfragt und diese den meterIDs zuordnet
""" This function reads the coordinates from all prosumerHouseholds
    from AssetListe.json
    
    It returns them in a dictionary
    
    key: prosumer-Id
    value: [langitude, longitude]"""
def get_prosumer_coordinates(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        prosumer_coordinates = {}

        for household in payload['data']:
            for k in get_prosumer_ids():
                if household['meterId'] == k:
                    prosumer_coordinates[k] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return prosumer_coordinates


""" This function reads the coordinates from all consumerHouseholds
    from AssetListe.json
    
    This function isnt needed!
        
    It returns them in a dictionary

    key: consumer-Id
    value: [langitude, longitude]"""
def get_consumer_coordinates(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        consumer_coordinates = {}

        for household in payload['data']:
            for i in get_consumer_ids():
                if household['meterId'] == i:
                    consumer_coordinates[i] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return consumer_coordinates


""" This function reads the coordinates from all Households
    from AssetListe.json

    It returns them in a dictionary

    key: consumer-Id
    value: [langitude, longitude]
    
    total lenght: 92"""
def get_allHouseholds_coordinates(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        allHouseholds_coordinates = {}

        for household in payload['data']:
            if household['meterId'] != 'NO_METER_AVAILABLE':
                allHouseholds_coordinates[household['meterId']] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return allHouseholds_coordinates

print(len(get_allHouseholds_coordinates('AssetListe.json')))