import json
import csv
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
from getDataFromAssetListe import get_prosumer_ids


""" This function returns for all households to their Konzessionsabgaben matched
    to their meterIds
    
    It returns a dictionary.
    
    Length of the dictionary is 92
    """
def get_meterID_to_Konzessionsabgabe(file,matched_meterIDs_to_zipcode):

    #dictionary for konzessionsabgaben matched to households meterids
    meterID_to_Konzessionsabgabe_Dict = {}

    for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

        meterID_to_Konzessionsabgabe_Dict [meterId] = float(EnetData['Konzessionsabgabe'].replace(',', '.'))

    return meterID_to_Konzessionsabgabe_Dict



""" This function returns the Konzessionsabgaben of every prosumer household from AssetListe.json
    
    This is used to calculate the costs from all prosumers to all households later on
    
    return: dictionary prosumerIds matched to Konzessionsabgaben
    lenght: 14
    """
def get_prosumerMeterID_to_Konzessionsabgabe(file,matched_meterIDs_to_zipcode):

    #dictionary for all prosumerIds to their Konzessionsabgaben
    prosumerMeterId_to_Konzessionsabgabe_Dict = {}


    for producer in get_prosumer_ids():

        for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

            if producer == meterId:

                prosumerMeterId_to_Konzessionsabgabe_Dict [meterId] = float(EnetData['Konzessionsabgabe'].replace(',', '.'))

    return prosumerMeterId_to_Konzessionsabgabe_Dict

