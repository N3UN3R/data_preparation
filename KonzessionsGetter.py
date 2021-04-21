import json
import csv
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
from getDataFromAssetListe import get_prosumer_ids

""" This function returns for all households to their Konzessionsabgaben matched
    to their meterIds

    It returns a dictionary.

    Length of the dictionary is 92
    """


def get_meterID_to_Konzessionsabgabe(file, matched_meterIDs_to_zipcode):
    # dictionary for konzessionsabgaben matched to households meterids
    meterID_to_Konzessionsabgabe_Dict = {}

    for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():
        meterID_to_Konzessionsabgabe_Dict[meterId] = float(EnetData['Konzessionsabgabe'].replace(',', '.'))

    return meterID_to_Konzessionsabgabe_Dict


""" This function returns the Konzessionsabgaben of every prosumer household from AssetListe.json

    This is used to calculate the costs from all prosumers to all households later on

    return: dictionary prosumerIds matched to Konzessionsabgaben
    lenght: 14
    """


def get_prosumerMeterID_to_Konzessionsabgabe(file, matched_meterIDs_to_zipcode):
    # dictionary for all prosumerIds to their Konzessionsabgaben
    prosumerMeterId_to_Konzessionsabgabe_Dict = {}

    for producer in get_prosumer_ids():

        for meterId, EnetData in get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode).items():

            if producer == meterId:
                prosumerMeterId_to_Konzessionsabgabe_Dict[meterId] = float(
                    EnetData['Konzessionsabgabe'].replace(',', '.'))

    return prosumerMeterId_to_Konzessionsabgabe_Dict


""" Function that calculates the difference in between the KonzessionsKosten from all prosumers from AssetListe.json
    to all other households

    returns a dictionary with the households meterIds as key and the konzessionskosten difference as value entry

    returns: dictionary     key: (prosumerId, householdId)      value: netCostDifference

    length: 1288 = the dictionary also contains pairs of households with themselves. They have to be removed later
    """


def prosumers_to_all_households_konzessionscost(prosumerMeterId_to_Konzessionsabgabe_Dict,
                                                meterID_to_Konzessionsabgabe_Dict):

    konzessionCost_prosumers_to_all_households = {}

    for prosumerId, konzessionCost in prosumerMeterId_to_Konzessionsabgabe_Dict.items():
        konzessionCost_prosumers_to_all_households[prosumerId] = {}
        for meterId, konzessionCost2 in meterID_to_Konzessionsabgabe_Dict.items():
            konzessionCostDifference = float(konzessionCost) - (konzessionCost2)
            konzessionCost_prosumers_to_all_households[prosumerId][meterId] = konzessionCostDifference

    return konzessionCost_prosumers_to_all_households


def main():
    # input fuer die funktion get meter id to zipcode
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    file = 'AssetListe.json'

    # imput fuer die funktion get EnetData
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    # input für get_meterID_to_Konzessionsabgabe
    meterID_to_Konzessionsabgabe_Dict = get_meterID_to_Konzessionsabgabe(file, matched_meterIDs_to_zipcode)

    # input für  get_prosumerMeterID_to_Konzessionsabgabe
    prosumerMeterId_to_Konzessionsabgabe_Dict = get_prosumerMeterID_to_Konzessionsabgabe(file,
                                                                                         matched_meterIDs_to_zipcode)

    test = prosumers_to_all_households_konzessionscost(prosumerMeterId_to_Konzessionsabgabe_Dict,
                                                       meterID_to_Konzessionsabgabe_Dict)


if __name__ == '__main__':
    main()