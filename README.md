# data_preparation
this repo contains all scripts that are need to calculate the power costs for all possible 
It is still work in progress!
Scripts will be added in the next days

Following files are needed to run these scripts:

- AssetListe.json
- NetzpreiseCSV.csv
- prosumer_IDs.csv



# The following scripts get needed information from AssetListe.json

getDataFromAssetListe.py
- this script contain various functions to get data from AssetListe.json
- def get_allHouseholds_coordinates(file): returns a dictionary with all meterIds matched to their coordinates
- def get_prosumer_coordinates(file): returns a dictionary with all meterIds of prosumers matched to their coordinates

lokalerZusammenhang.py
- this script calculates the distance of all households 
- based on the distance it checks which trading costs could be reduced in consequence of a distance < 4.5 km 


# The following scripts work with data provided by ene't GmbH

enetGetterNew.py
- contains one function that returns all households zipcodes matched to their meterIds
- contains one function that returns all netinformations for a household matched to its meterId
