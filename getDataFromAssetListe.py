import json
import csv


""" this function read the json-file AssetListe.json

    it returns a list with alle meterIds in Asset-Liste.json"""
def read_asset_list(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)
        asset_ids = []
        for household in payload['data']:
            asset_ids.append(household['meterId'])

    return asset_ids

""" This function reads in a file called prosumer_Ids.csv
    It contains a list of all meterIds that are prosumer households 
    in the BloGPV-Community
    """
def generate_producer_keys(file):
    # getting Data out of csv file
    with open(file, 'r') as csv_file:
        csvReader = csv.reader(csv_file)

       #storing meterIds in a List
        producerList = []
        for i in csvReader:
            producerList.append(i[0])
        return producerList

#keys_prosumer = generate_producer_keys('prosumer_IDs.csv')


""" this function checks which producer Ids are also in AssetListe.json.
    This has to be made as there are more producers on the API than in
    AssetListe.json
    
    It returns a list of all prosumderIds that are in AssetListe.json
    
    In total 14"""
def get_producer_ids():
    producerKeys = generate_producer_keys(file= 'prosumer_IDs.csv')
    producerIDs = list(set(producerKeys) & set(read_asset_list('AssetListe.json')))

    return producerIDs


""" This function returns a list of all households that are just consumers
    from AssetListe.json
    
    in total 78"""
def get_consumer_ids():

    producerIDs = set(get_producer_ids())
    assetIDs = set(read_asset_list('AssetListe.json'))
    consumerIDs = list(assetIDs.difference(producerIDs))

    return consumerIDs




#Funktion die Producer-Koordinaten abfragt und diese den meterIDs zuordnet
""" This function reads the coordinates from all prosumerHouseholds
    from AssetListe.json
    
    It returns them in a dictionary
    
    key: prosumer-Id
    value: [langitude, longitude]"""
def get_producer_coordinates(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)

        producer_coordinates = {}

        for household in payload['data']:
            for k in get_producer_ids():
                if household['meterId'] == k:
                    producer_coordinates[k] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return producer_coordinates


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
            allHouseholds_coordinates[household['meterId']] = list((float(household['location']['lat']),float(household['location']['lng'])))

    return allHouseholds_coordinates

