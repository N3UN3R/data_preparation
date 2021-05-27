import json
import csv

# this programm gets the Netzentgelte out of Data provided by ene't GmbH

""" This function returns a dictionary with zip codes
    matched to the meterIds from houesholds

    Inputfile is 'assetListe.json'
    the length of the output dictionary is 92
   """


def get_meter_id_to_zipcode_dict(file):
    with open(file, 'r') as json_data:
        payload = json.load(json_data)
        meter_ids_to_zipcodes = {}
        for household in payload['data']:
            meter_ids_to_zipcodes[household['meterId']] = int(household['location']['zip'])

    return meter_ids_to_zipcodes


# function that gets netcosts out of ene't Data (csv file)
""" Function that returns all entrys of a csv-file from ene't GmbH
    This file contains informations like netcosts, konzessionskosten,
    and more matched to zipcodes.

    This function receives the meterIds matched to zipcodes from
    get_meter_id_to_zipcode_dict()

    it returns a dictionary where meterIds are matched to the entrys
    from the csv-file
    """


def get_ENetData(file, matched_meterIDs_to_zipcode):
    # getting Data out of ene't Data from csv file
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        rows = [dict(d) for d in csv_reader]
        households_with_Enet_Data = {}

        # comparing zipcodes from meter_id_list and ENet Data
        data = []
        for row in rows:

            for meterId, zip in matched_meterIDs_to_zipcode.items():
                zipcode = zip
                test.append(zipcode)

                if float(zipcode) == float(row['PLZ']):
                    data.append(zipcode)
                    households_with_Enet_Data[meterId] = row

    return households_with_Enet_Data


def main():
    # input fuer die funktion get meter id to zipcode
    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    # imput fuer die funktion get EnetData
    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    print(matched_MeterIDS_to_EnetData)


if __name__ == '__main__':
    main()