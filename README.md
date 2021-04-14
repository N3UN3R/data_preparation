# data_preparation
this repo contains all scripts that were needed to prepare the input data for the algorithms

this repo will contain the scripts for:

getDataFromAssetListe.py
- this script contain various functions to get data from AssetListe.json
- def get_allHouseholds_coordinates(file): returns a dictionary with all meterIds matched to their coordinates
- def get_prosumer_coordinates(file): returns a dictionary with all meterIds of prosumers matched to their coordinates

lokalerZusammenhang.py
- this script calculates the distance of all households 
- based on the distance it checks which trading costs could be reduced in consequence of a distance < 4.5 km 


calculating distances in between households

extracting needed data from ene't data

calculating the cost dictionary
