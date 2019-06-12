import unirest
import pprint
import sys
from selenium import webdriver
from secrets import *

pp = pprint.PrettyPrinter(indent=4)


# Top 30 US airports.
def list_of_destinations():
    return ["ATL", "LAX", "ORD", "DFW", "JFK", "SFO", "LAS", "SEA",
            "CLT", "EWR", "MCO", "PHX", "MIA", "IAH", "BOS", "MSP", "DTW",
            "PHL", "LGA", "BWI", "SLC", "DCA", "IAD", "SAN", "MDW", "TPA",
            "HNL", "PDX", "FLL", "PWM", "RSW"]


# Scrape from googleFlights
def scrape_flights():
    # url = 'http://kanview.ks.gov/PayRates/PayRates_Agency.aspx'
    url = 'https://www.google.com/flights/#flt=JFK.CDG.2019-04-15*CDG.JFK.2019-04-25;c:USD;e:1;sd:1;t:f'

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(15)
    driver.get(url)
    #python_button = driver.find_element_by_class_name('gws-flights-form__menu-label')
    #python_button.click()  #
    print(driver.save_screenshot())


# API Request from origin to destination
def make_request(orig, destination, outbound_date, inbound_partial_date):
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/"
    currency = "USD"
    locale = "en-US"

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


def make_request_try():
    response = unirest.get(
        "https://apidojo-kayak-v1.p.rapidapi.com/flights/create-session?origin1=pwm&destination1=rsw&departdate1=2019-12-20&cabin=e&currency=USD&adults=1&bags=0",
        headers={
            "X-RapidAPI-Host": "apidojo-kayak-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "968bbe113amsh24779accb4e225bp173f65jsn5292c5285800"
        }
    )
    print(response.body)


# Minimum price of origin to destination
def cheapest_option(origin, destination, outbound_date, inbound_partial_date):
    if origin == destination:
        return 0

    dic = make_request(origin, destination, outbound_date, inbound_partial_date)
    # There are no flights from origin to this destination
    if not dic['Quotes']:
        print("flight from " + origin + " to " + destination + " does not exist.")
        # this should be optimized
        return sys.maxsize

    min_price = dic['Quotes'][0]['MinPrice']
    print("Cheapest option from " + origin + " to " +
          destination + " is: " + str(min_price))
    return min_price


# Cheapest destination from list of origins.
def find_cheapest_destination(origins, outbound_date, inbound_partial_date):
    cheapest_destination = "none"
    total_cost = 0
    total_destination_cost = sys.maxsize  # Trying to improve this
    destinations_to_cost = {}  # map of destination and total cost

    # Iterate over popular airport destinations
    for destination in list_of_destinations():
        # Check cost from given origin
        for key in origins:
            total_cost += (origins.get(key) * cheapest_option(key, destination, outbound_date, inbound_partial_date))
            total_cost += (origins.get(key) * cheapest_option(destination, key, inbound_partial_date, outbound_date))
        destinations_to_cost[str(destination)] = total_cost

        # Update cheapest option
        if total_cost < total_destination_cost:
            print("updating total cost to " + str(total_cost))
            print("updating destination to " + destination)
            cheapest_destination = destination
            total_destination_cost = total_cost
        total_cost = 0

    print("cheapest destination is " + str(cheapest_destination)
          + " with total cost of " + str(total_destination_cost))

    sorted_dest = sorted(destinations_to_cost.items(), key=lambda kv: kv[1])
    for dest in range(5):
        print(sorted_dest.__getitem__(dest))


def main():
    origins = {"BOS": 2, "SEA": 4, "JFK": 2}
    # origins = {"rsw": 4}
    # find_cheapest_destination(origins, "2019-12-20", "2019-12-30")
    # response = make_request("RSW", "LAX", "2019-12-20", "2019-12-30")
    scrape_flights()
    # make_request_try()


main()
