import unirest
import pprint
import sys

pp = pprint.PrettyPrinter(indent = 4)

# Top 30 US airports. 
def list_of_destinations():
    return ["ATL", "LAX", "ORD", "DFW", "JFK", "SFO", "LAS", "SEA",
    "CLT", "EWR", "MCO", "PHX", "MIA", "IAH", "BOS", "MSP", "DTW",
    "PHL", "LGA", "BWI", "SLC", "DCA", "IAD", "SAN", "MDW", "TPA", 
    "HNL", "PDX", "FLL"]

# API Request from origin to destination
def make_request(orig, destination, outboundDate, inboundpartialdate):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/"
    currency = "USD"
    locale = "en-US"
    #print("origin is " + orig + "destination is " + destination)

    response = unirest.get(
    	url + 
    	currency + "/" + 
     	locale +  "/" +
     	orig + "/" +
     	destination + "/"  + 
     	outboundDate + 
     	"?inboundpartialdate=" + inboundpartialdate ,
     	headers={
     	"X-RapidAPI-Key": "a0915c4020mshf5be91092680fb8p158548jsn0ace0d03560a"
      })
    return response.body

# Minimum price of origin to destination
def cheapest_option(origin, destination, outboundDate, inboundpartialdate):
    if (origin == destination) :
        return 0
    
    dic = make_request(origin, destination, outboundDate, inboundpartialdate)
    # There are no flights from origin to this destination
    if (not dic['Quotes']):
        print("flight to " + destination + " does not exist.")
        return sys.maxsize

    cheapest_option = dic['Quotes'][0]['MinPrice']
    pp.pprint("Cheapset option from " + origin + " to " +
        destination + " is: " + str(cheapest_option))
    return cheapest_option

# Cheapest destination from list of origins. 
def find_cheapest_destination(origins, outboundDate, inboundpartialdate):
    total_cost = 0
    total_destination_cost = sys.maxsize # Trying to improve this

    # Iterate over popular airport destinations
    for destination in list_of_destinations() :
        # Check cost from given origin
        for origin in origins:
            total_cost += cheapest_option(origin, destination, inboundpartialdate, outboundDate)
            print(total_cost)
        cheapest_destination

        # Update cheapest option
        if (total_cost < total_destination_cost) :
            print("updating total cost to " + str(total_cost))
            cheapest_destination = destination
            total_destination_cost = total_cost
        total_cost = 0

    print("cheapest destination is " + str(cheapest_destination)
        + " with total cost of " + str(total_destination_cost))

def main():

    origins = ["BOS", "JFK", "ATL", "JFK"]
    find_cheapest_destination(origins, "2019-05-06", "2019-05-17")
    #make_request("JFK", "EWR")

main()

