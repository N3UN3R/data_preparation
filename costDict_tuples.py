import json


def create_tuple_costDict():
    """ function that reads in 'tradingCost_prosumers_to_all_households_nested.json'
        and returns a dictionary with matched households and the specific costs of
        each pair

        the returned dictionary is saved to a json-file called
        'tradingCost_prosumers_to_all_households_tuples.json'"""

    with open('tradingCost_prosumers_to_all_households_nested.json', 'r') as data:
        costs = json.load(data)

    tuple_dict = {}
    for prosumerId, matchedHouseholds in costs.items():
        for householdId, cost in matchedHouseholds.items():
            tuple_dict[(prosumerId, householdId)] = cost

    with open(('tradingCost_prosumers_to_all_households_tuples.json'), 'w') as file:
        json.dump(str(tuple_dict), file)

    return tuple_dict

print(create_tuple_costDict())