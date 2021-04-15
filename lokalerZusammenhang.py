from getDataFromAssetListe import get_allHouseholds_coordinates, get_prosumer_coordinates
from geopy.distance import geodesic



#berechne die Entfernung der Prosumer Haushalte zu allen Haushalten

""" this function calculates the distance from all prosumer-households to all households.
    As the distance from a prosumer household to itself would be zero this is set to 10000.
    
    The distances in between the households are needed to calculate the possible price reduction
    due to räumlicher Zusammenhang"""
def calculate_distance_from_prosumers_to_allHouseholds():

    distance_from_prosumers_to_allHouseholds = {}
    for key1, coordinate1 in get_prosumer_coordinates('AssetListe.json').items():
        for key2, coordinate2 in get_allHouseholds_coordinates('AssetListe.json').items():
                distance = float(geodesic(coordinate1, coordinate2).km)

                matchedprosumerIds = tuple([key1, key2])
                distance_from_prosumers_to_allHouseholds[matchedprosumerIds] = distance

                if key1 == key2:
                    distance_from_prosumers_to_allHouseholds[matchedprosumerIds] = 100000

    return distance_from_prosumers_to_allHouseholds


""" This function sets the possible price reduction from local trading.
    As price could be reduced for a distance lower than 4.5km it checks
    whether the distance in between to households is lower than this limit"""
def calculate_price_reduction_of_local_trading():

    localNeighbourDiscount = {}
    for key, distance in calculate_distance_from_prosumers_to_allHouseholds().items():
        if float(distance) <= float(4.5):
            #2.07 is based on the Stromsteuer of an average price of 30 ct/kWh
            localNeighbourDiscount[key] = float(2.07)

        else:
            localNeighbourDiscount[key] = float(0)

    return localNeighbourDiscount
