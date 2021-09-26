from NetzentgeltGetter import calculate_prosmumer_to_all_households_netCosts_difference, get_meterID_to_Netzentgelt, get_prosumerMeterID_to_Netzentgelt
from KonzessionsGetter import prosumers_to_all_households_konzessionscost, get_prosumerMeterID_to_Konzessionsabgabe, get_meterID_to_Konzessionsabgabe
from lokalerZusammenhang import calculate_price_reduction_of_local_trading
from ENetGetterNew import get_ENetData, get_meter_id_to_zipcode_dict
import json


def calculate_total_trading_costs_nested(netCostDifferences,konzessionsCostDifferences):
    """ function that calculates the trading prices of all possible household pairs
        within the community"""

    total_trading_costs_dict_nested = {}
    localTradingDiscount = calculate_price_reduction_of_local_trading()

    # constant values
    #EEG-Umlage value of 6,81 ct/kWh
    EEG_Umlage = float(6.81)
    # average electricity price
    average_electricity_price = float(30.0)

    for prosumerId,households in localTradingDiscount.items():
        total_trading_costs_dict_nested[prosumerId] = {}
        for meterId, localDiscountValue in households.items():
            tradingDiscount = 0

            if float(localDiscountValue) > 0:
                tradingDiscount += localDiscountValue

            netCostDiscount = netCostDifferences[prosumerId][meterId]
            if float(netCostDiscount) > 0:
                tradingDiscount += netCostDiscount

            konzessionsCostDiscount = konzessionsCostDifferences[prosumerId][meterId]
            if float(konzessionsCostDiscount) > 0:
                tradingDiscount += konzessionsCostDiscount

            total_trading_costs_dict_nested[prosumerId][meterId] = average_electricity_price - EEG_Umlage - tradingDiscount

    with open(('tradingCost_prosumers_to_all_households_nested.json'), 'w') as file:
        json.dump(total_trading_costs_dict_nested, file)

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

    print(netCostDifferences)

   # print(konzessionsCostDifferences)
   # print(calculate_total_trading_costs_nested(netCostDifferences,konzessionsCostDifferences))

if __name__ == '__main__':
    main()