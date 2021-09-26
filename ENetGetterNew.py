import json
import csv


def get_meter_id_to_zipcode_dict(file):
    """ function that reads in 'AssetListe.json and
        returns a python dictionary with all meterIds matched
        to zipcodes"""

    with open(file, 'r') as json_data:
        payload = json.load(json_data)
        meter_ids_to_zipcodes = {}
        for household in payload['data']:
            meter_ids_to_zipcodes[household['meterId']] = int(household['location']['zip'])

    return meter_ids_to_zipcodes


def get_ENetData(file, matched_meterIDs_to_zipcode):
    """ Function that returns all entrys of a csv-file from ene't GmbH
    This file contains informations like netcosts, konzessionskosten,
    and more matched to zipcodes.

    This function receives the meterIds matched to zipcodes from
    get_meter_id_to_zipcode_dict()

    it returns a dictionary where meterIds are matched to the entrys
    from the csv-file
    """

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

                if float(zipcode) == float(row['PLZ']):
                    data.append(zipcode)
                    households_with_Enet_Data[meterId] = row

    return households_with_Enet_Data


def main():

    matched_meterIDs_to_zipcode = get_meter_id_to_zipcode_dict('AssetListe.json')

    matched_MeterIDS_to_EnetData = get_ENetData('NetzpreiseCSV.csv', matched_meterIDs_to_zipcode)

    #print(matched_MeterIDS_to_EnetData)


if __name__ == '__main__':
    main()