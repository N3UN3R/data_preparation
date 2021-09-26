import json
import csv
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
from getDataFromAssetListe import get_prosumer_ids


def get_meterID_to_Netzentgelt(file,matched_meterIDs_to_zipcode):
    """ this function returns the Netzentgelte for all households from AssetListe.json
        returns: dictionary meterID_to_Netzentgelte_Dict
                 key: meterId        value: netzentgelt"""

    #erstelle Dict fuer Netzentgelte zu meterID
    meterID_to_Netzentgelte_Dict = {}

    for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

        meterID_to_Netzentgelte_Dict[meterId] = float(EnetData['spez. Netzentgelt'].replace(',', '.'))

    return meterID_to_Netzentgelte_Dict


def get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode):
    """ function that returns the netzentgelte of all prosumer households from AssetListe.json
        returns dictionary prosumerMeterId_to_Netzentgelte_Dict
         key: prosumerId         value: netzentgelt"""

    #erstelle Dict fuer Netzentgelte der prosumers
    prosumerMeterId_to_Netzentgelte_Dict = {}

    #benutze producerListe
    for producer in get_prosumer_ids():

        for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

            if producer == meterId:
                prosumerMeterId_to_Netzentgelte_Dict[producer] = float(EnetData['spez. Netzentgelt'].replace(',', '.'))

    return prosumerMeterId_to_Netzentgelte_Dict


def calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,
                                                              meterID_to_Netzentgelte_Dict):
    """ function that calculates the difference of the netCosts from all prosumer households to all
        other households
        returns: dictionary   netCost_difference_dict
                 key= (prosumerId, householdId)      value = netCostDifference"""

    netCost_difference_dict = {}

    for prosumerId, netCost in prosumerMeterId_to_Netzentgelte_Dict.items():
        netCost_difference_dict[prosumerId] = {}
        for meterId, netCost2 in meterID_to_Netzentgelte_Dict.items():
            netCostDifference = float(netCost) - float(netCost2)
            netCost_difference_dict[prosumerId][meterId] = netCostDifference

    return netCost_difference_dict


def main():

    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    meterID_to_Netzentgelte_Dict = get_meterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    prosumerMeterId_to_Netzentgelte_Dict = get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    netCost_difference_dict = calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,meterID_to_Netzentgelte_Dict)



if __name__ == '__main__':
    main()
