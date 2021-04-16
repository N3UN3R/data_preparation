# data_preparation (wip not all needed scripts added yet)

this repo contains all scripts that are needed to calculate the power costs for all possible household-pairs.
the resulting cost dictionary could be interpreted as an adjancecy matrix and is basis for all algorithms of
this thesis.

Following files are needed to run these scripts:

- AssetListe.json
- NetzpreiseCSV.csv
- prosumer_IDs.csv


# Calculating the trading costs for all possible household pairs

costCalculator.py


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

KonzessionsGetter.py
- contains function that matches Konzessionsabgaben from all households from assetList.json to their meterIds
- contains function that matches Konzessionsabgaben from all prosumer Households from assetListe.json to their meterIds
- contains function that calculates the Konzessionsabgaben-Difference from all prosumer households to all households

NetzentgeltGetter.py
- contains function that matches Netzentgelte of all households to their meterIds
- contains function that matches Netzentgelte of all prosumer households to their meterIds
- contains function that matches all Netzentgelt differences from all prosumers to all households

