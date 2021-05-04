from NetzentgeltGetter import calculate_prosmumer_to_all_households_netCosts_difference, get_meterID_to_Netzentgelt, get_prosumerMeterID_to_Netzentgelt
from KonzessionsGetter import prosumers_to_all_households_konzessionscost, get_prosumerMeterID_to_Konzessionsabgabe, get_meterID_to_Konzessionsabgabe
from lokalerZusammenhang import calculate_price_reduction_of_local_trading
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
import json

""" this script calculates the final tradingCost from all prosumers to all households
    
    it gets data from lokaler Zusammenhang
    lokalerZusammenhang.py      - price reduction because of distance < 4.5 km
    KonzessionsGetter.py        - difference of konzessionsKosten
    Netzentgelter.py            - differnece of Netzentgelte
"""

def calculate_total_trading_costs_nested(netCostDifferences,konzessionsCostDifferences):

    total_trading_costs_dict_nested = {}

    netCostDifferences_discount = netCostDifferences
    konzessionCostDifferences_discount = konzessionsCostDifferences
    localTradingDiscount = calculate_price_reduction_of_local_trading()

    # constant values
    # EEG_Umlage mit 6,81 ct/kWh
    EEG_Umlage = float(6.81)
    # durchschnittlicher Strompreis in Deutschland
    average_electricity_price = float(30.0)

    for prosumerId,households in calculate_price_reduction_of_local_trading().items():
        total_trading_costs_dict_nested[prosumerId] = {}

        for meterId, localDiscountValue in households.items():

            localDiscount = localDiscountValue

            netCostDiscount = netCostDifferences_discount[prosumerId][meterId]

            konzessionsCostDiscount = konzessionCostDifferences_discount[prosumerId][meterId]


            tradingDiscount = float(localDiscount)+float(netCostDiscount)+float(konzessionsCostDiscount)

            total_trading_costs_dict_nested[prosumerId][meterId] = average_electricity_price - EEG_Umlage - tradingDiscount

    with open(('tradingCost_prosumers_to_all_households_nested.json'), 'w') as file:
        json.dump(str(total_trading_costs_dict_nested),file)

    return total_trading_costs_dict_nested



def main():

    #input for functions from EnetGetterNew
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    #input to calculate netCostDifferences
    prosumerMeterId_to_Netzentgelte_Dict = get_prosumerMeterID_to_Netzentgelt(matched_MeterIDS_to_EnetData,
                                                                              matched_meterIDs_to_zipcode)
    meterID_to_Netzentgelte_Dict = get_meterID_to_Netzentgelt(matched_MeterIDS_to_EnetData, matched_meterIDs_to_zipcode)

    netCostDifferences = calculate_prosmumer_to_all_households_netCosts_difference(prosumerMeterId_to_Netzentgelte_Dict,meterID_to_Netzentgelte_Dict)

    #input to calculate Konzessionscosts
    prosumerMeterId_to_Konzessionsabgabe_Dict = get_prosumerMeterID_to_Konzessionsabgabe('AssetListe.json',
                                                                                         matched_meterIDs_to_zipcode)
    meterID_to_Konzessionsabgabe_Dict = get_meterID_to_Konzessionsabgabe('AssetListe.json', matched_meterIDs_to_zipcode)

    konzessionsCostDifferences = prosumers_to_all_households_konzessionscost(prosumerMeterId_to_Konzessionsabgabe_Dict,
                                               meterID_to_Konzessionsabgabe_Dict)



if __name__ == '__main__':
    main()