from NetzentgeltGetter import calculate_prosmumer_to_all_households_netCosts_difference
from KonzessionsGetter import prosumers_to_all_households_konzessionscost
from lokalerZusammenhang import calculate_price_reduction_of_local_trading

""" this script calculates the final tradingCost from all prosumers to all households
    
    it gets data from lokaler Zusammenhang
    lokalerZusammenhang.py      - price reduction because of distance < 4.5 km
    KonzessionsGetter.py        - difference of konzessionsKosten
    Netzentgelter.py            - differnece of Netzentgelte
"""

