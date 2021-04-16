import json
import csv
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
from getDataFromAssetListe import get_prosumer_ids

#hierbei werden aus den Daten der Enet die Konzessionsabgaben, welche auch auf der Karte
#https://www.bundesnetzagentur.de/SharedDocs/Bilder/DE/Sachgebiete/Energie/Verbraucher/Energielexikon/Netzentgeltkarte_Haush.jpg?__blob=poster&v=4
#abgebildet sind bezogen


""" this function returns the Netzentgelte for all households from AssetListe.json

    returns: dictionary         key: meterId        value: netzentgelt
    length: 92"""
def get_meterID_to_Netzentgelt(file,matched_meterIDs_to_zipcode):

    #erstelle Dict fuer Netzentgelte zu meterID
    meterID_to_Netzentgelte_Dict = {}


    for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

        meterID_to_Netzentgelte_Dict[meterId] = float(EnetData['spez. Netzentgelt'].replace(',', '.'))


    return meterID_to_Netzentgelte_Dict



""" function that returns the netzentgelte of all prosumer households from AssetListe.json
    
    returns dictionary          key: prosumerId         value: netzentgelt
    length: 14
"""
def get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode):

    #erstelle Dict fuer Netzentgelte der prosumers
    prosumerMeterId_to_Netzentgelte_Dict = {}

    #benutze producerListe
    for producer in get_prosumer_ids():

        for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

            if producer == meterId:
                prosumerMeterId_to_Netzentgelte_Dict[producer] = float(EnetData['spez. Netzentgelt'].replace(',', '.'))

    return prosumerMeterId_to_Netzentgelte_Dict


    """ function that calculates the difference of the netCosts from all prosumer households to all
        other households
        
        returns: dictionary         key= (prosumerId, householdId)      value = netCostDifference
        
        length: 1288
        """
def calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,meterID_to_Netzentgelte_Dict):
    pass
    netCost_difference_dict = {}

    for prosumerId, netCost in prosumerMeterId_to_Netzentgelte_Dict.items():
        for meterId, netCost2 in meterID_to_Netzentgelte_Dict.items():
            matchedHouseholdIds = tuple([prosumerId, meterId])
            netCostDifference = float(netCost) - float(netCost2)
            netCost_difference_dict[matchedHouseholdIds] = netCostDifference

    return netCost_difference_dict


def main():

    # input fuer die funktion get meter id to zipcode
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    # imput fuer die funktion get EnetData
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    #input für get_meterID_to_Konzessionsabgabe
    meterID_to_Netzentgelte_Dict = get_meterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    #input fuer get_prosumerMeterID_to_Netzentgelt
    prosumerMeterId_to_Netzentgelte_Dict = get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    netCost_difference_dict = calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,meterID_to_Netzentgelte_Dict)

    print(netCost_difference_dict)


if __name__ == '__main__':
    main()
