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

def calculate_total_trading_costs(netCostDifferences,konzessionsCostDifferences):
    pass
    total_trading_costs_dict = {}

    netCostDifferences_discount = netCostDifferences
    konzessionCostDifferences_discount = konzessionsCostDifferences
    localTradingDiscount = calculate_price_reduction_of_local_trading()

    # constant values
    # EEG_Umlage mit 6,81 ct/kWh
    EEG_Umlage = float(6.81)
    # durchschnittlicher Strompreis in Deutschland
    average_electricity_price = float(30.0)

    for i in localTradingDiscount.keys():
        # entspricht der Einsparungsfunktion im schriftlichen Teil
        tradingDiscount = float(netCostDifferences_discount[i]) + float(konzessionCostDifferences_discount[i]) + float(
            localTradingDiscount[i])
        # berechnet die Stromkosten, welche fuer die Optimierung später benötigt werden
        total_trading_costs_dict[i] = average_electricity_price - EEG_Umlage - tradingDiscount

    with open(('tradingCost_prosumers_to_all_households.json'), 'w') as file:
        json.dump(str(total_trading_costs_dict),file)

    return total_trading_costs_dict


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


    print(len(calculate_total_trading_costs(netCostDifferences,konzessionsCostDifferences)))


if __name__ == '__main__':
    main()