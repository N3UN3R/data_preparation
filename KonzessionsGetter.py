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


""" Function that calculates the difference in between the KonzessionsKosten from all prosumers from AssetListe.json
    to all other households
    
    returns a dictionary with the households meterIds as key and the konzessionskosten difference as value entry
    """
def prosumers_to_all_households_konzessionscost():




def main():

    # input fuer die funktion get meter id to zipcode
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    # imput fuer die funktion get EnetData
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    #input für get_meterID_to_Konzessionsabgabe
    matched_MeterIDS_to_Konzessionsabgabe = get_meterID_to_Konzessionsabgabe(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    #input für  get_prosumerMeterID_to_Konzessionsabgabe
    prosumerIds_matched_to_konzessionscost = get_prosumerMeterID_to_Konzessionsabgabe(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode)

    #print(prosumerIds_matched_to_konzessionscost.__len__())

    print(matched_MeterIDS_to_Konzessionsabgabe)


    #print(matched_MeterIDS_to_Konzessionsabgabe)
    #print(matched_MeterIDS_to_Konzessionsabgabe.__len__())



if __name__ == '__main__':
    main()



#file = 'AssetListe.json'
#prosumerMeterId_to_Konzessionsabgabe_Dict = get_prosumerMeterID_to_Konzessionsabgabe(file,matched_meterIDs_to_zipcode)


#def calculate_KonzessionsabgabenDifferenz_prosumer_to_all_households(file, meterID_to_Konzessionsabgabe_Dict,prosumerMeterId_to_Konzessionsabgabe_Dict):

 #   konzessionCost_difference_dict = {}

  #  for meterId, KonzessionCost in get_meterID_to_Konzessionsabgabe(file,matched_meterIDs_to_zipcode).items():
   #     for meterId2Konz, KonzessionCost2 in get_meterID_to_Konzessionsabgabe(matched_MeterIDS_to_EnetData,matched_meterIDs_to_zipcode).items():
      #      matchedHouseholdIdsKonzession = tuple([meterIdKonz,meterId2Konz])
    #        konzessionCostDifference = float(KonzessionCost)-(KonzessionCost2)
     #       konzessionCost_difference_dict[matchedHouseholdIdsKonzession] = konzessionCostDifference

    #return konzessionCost_difference_dict