import pprint
import sys
from secrets import *

pp = pprint.PrettyPrinter(indent=4)


# Top 30 US airports.
def list_of_destinations():
    return ["ATL", "LAX", "ORD", "DFW", "JFK", "SFO", "LAS", "SEA",
            "CLT", "EWR", "MCO", "PHX", "MIA", "IAH", "BOS", "MSP", "DTW",
            "PHL", "LGA", "BWI", "SLC", "DCA", "IAD", "SAN", "MDW", "TPA",
            "HNL", "PDX", "FLL"]


# API Request from origin to destination
def make_request(orig, destination, outbound_date, inbound_partial_date):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/"
    currency = "USD"
    locale = "en-US"
    # print("origin is " + orig + "destination is " + destination)

    response = unirest.get(
        url +
        currency + "/" +
        locale + "/" +
        orig + "/" +
        destination + "/" +
        outbound_date +
        "?inboundpartialdate=" + inbound_partial_date,
        headers={
            "X-RapidAPI-Key": api_key
        })
    return response.body


# Minimum price of origin to destination
def cheapest_option(origin, destination, outbound_date, inbound_partial_date):
    if origin == destination:
        return 0

    dic = make_request(origin, destination, outbound_date, inbound_partial_date)
    # There are no flights from origin to this destination
    if not dic['Quotes']:
        print("flight to " + destination + " does not exist.")
        # this should be optimized
        return sys.maxsize

    min_price = dic['Quotes'][0]['MinPrice']
    print("Cheapest option from " + origin + " to " +
          destination + " is: " + str(min_price))
    return min_price


# Cheapest destination from list of origins.
def find_cheapest_destination(origins, outbound_date, inbound_partial_date):
    global cheapest_destination
    total_cost = 0
    total_destination_cost = sys.maxsize  # Trying to improve this
    destinations_to_cost = {}  # map of destination and total cost

    # Iterate over popular airport destinations
    for destination in list_of_destinations():
        # Check cost from given origin
        for key in origins:
            total_cost += (origins.get(key) * cheapest_option(key, destination, outbound_date, inbound_partial_date))
        destinations_to_cost[str(destination)] = total_cost

        # Update cheapest option
        if total_cost < total_destination_cost:
            print("updating total cost to " + str(total_cost))
            cheapest_destination = destination
            total_destination_cost = total_cost
        total_cost = 0

    print("cheapest destination is " + str(cheapest_destination)
          + " with total cost of " + str(total_destination_cost))

    sorted_dest = sorted(destinations_to_cost.items(), key=lambda kv: kv[1])
    for dest in range(5):
        print(sorted_dest.__getitem__(dest))


def main():
    origins = {"BOS": 1, "LAX": 1}
    find_cheapest_destination(origins, "2019-06-27", "2019-07-03")


def doSomething(params):
    return params
