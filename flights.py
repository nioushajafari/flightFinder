import unirest
import pprint

pp = pprint.PrettyPrinter(indent=4)
url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/"
currency = "USD"
locale = "en-US"
orig = "SFO-sky"
destination = "JFK-sky"
outboundDate = "2019-05-06"
inboundpartialdate = "2019-05-17"

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
  }
)


pp.pprint(response.body)