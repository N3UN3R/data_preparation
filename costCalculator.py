from NetzentgeltGetter import calculate_prosmumer_to_all_households_netCosts_difference, get_meterID_to_Netzentgelt, get_prosumerMeterID_to_Netzentgelt
from KonzessionsGetter import prosumers_to_all_households_konzessionscost, get_prosumerMeterID_to_Konzessionsabgabe, get_meterID_to_Konzessionsabgabe
from lokalerZusammenhang import calculate_price_reduction_of_local_trading
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict

""" this script calculates the final tradingCost from all prosumers to all households
    
    it gets data from lokaler Zusammenhang
    lokalerZusammenhang.py      - price reduction because of distance < 4.5 km
    KonzessionsGetter.py        - difference of konzessionsKosten
    Netzentgelter.py            - differnece of Netzentgelte
"""

def calculate_total_trading_costs():

    total_trading_costs_dict = {}

    netCost_discount_prosumers = calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,meterID_to_Netzentgelte_Dict)

    konzessionCost_discount_prosumers = prosumers_to_all_households_konzessionscost()
   # print(netCost_difference_dict)

    return 0


def main():
    # input fuer die funktion get meter id to zipcode
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    # imput fuer die funktion get EnetData
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    # input für get_meterID_to_Konzessionsabgabe
    meterID_to_Netzentgelte_Dict = get_meterID_to_Netzentgelt(matched_MeterIDS_to_EnetData, matched_meterIDs_to_zipcode)

    # input fuer get_prosumerMeterID_to_Netzentgelt
    prosumerMeterId_to_Netzentgelte_Dict = get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,
                                                                              matched_meterIDs_to_zipcode)
    netCost_difference_dict = calculate_prosmumer_to_all_households_netCosts_difference(
        prosumerMeterId_to_Netzentgelte_Dict, meterID_to_Netzentgelte_Dict)


    # input für get_meterID_to_Konzessionsabgabe
    meterID_to_Konzessionsabgabe_Dict = get_meterID_to_Konzessionsabgabe('AssetListe.json', matched_meterIDs_to_zipcode)

    # input für  get_prosumerMeterID_to_Konzessionsabgabe
    prosumerMeterId_to_Konzessionsabgabe_Dict = get_prosumerMeterID_to_Konzessionsabgabe('AssetListe.json',
                                                                                         matched_meterIDs_to_zipcode)

    print(netCost_difference_dict)

    print()

if __name__ == '__main__':
    main()