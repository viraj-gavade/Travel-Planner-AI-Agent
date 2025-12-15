The data consits of following three 

1. Flight Records - 30 json objects 
2. Hotels Records - 40 json objects 
3. Places Records - 40 json objects 

### Flight Sample :
{'flight_id': 'FL0001',
 'airline': 'IndiGo',
 'from': 'Hyderabad',
 'to': 'Delhi',
 'departure_time': '2025-01-04T11:32:00',
 'arrival_time': '2025-01-04T15:32:00',
 'price': 2907}

 keys :
 - flight_id - unique identification for each flight 
 - airline - name of the airlines.
 - from - place from where the flight took off (Starting Destination).
 - to - place where flight landed (Final Destination).
 - depature time - time flight departed from the  airport.
 - arrival time - time fligh arrived to the destination. 
 - price of the ticket of the flight.


### Hotel Sample :
{'hotel_id': 'HOT0001',
 'name': 'Grand Palace Hotel',
 'city': 'Delhi',
 'stars': 4,
 'price_per_night': 3897,
 'amenities': ['wifi', 'pool']}

 keys : 
 hotel_id : unique id of the hotel
 name : name of the hotel 
 city : city of the hotel
 starts : service category of the hotel
 price_per_night : price per night of the hotel 
 amenities : different amenities which hotel has example [wifi pool]

### Places sample
{'place_id': 'PLC0001',
 'name': 'Famous Fort',
 'city': 'Delhi',
 'type': 'lake',
 'rating': 4.6}

keys : 
 place_id : unique id of the place
 name : name of the place 
 city : city of the hotel 
 type : what type of loaction it is 
 rating : rating of that places 


#### Unique source cities (flight from): 
['Hyderabad' 'Delhi' 'Chennai' 'Bangalore' 'Goa' 'Kolkata' 'Jaipur'
 'Mumbai']


#### Unique destination cities(flight to ): 

['Delhi' 'Kolkata' 'Hyderabad' 'Mumbai' 'Bangalore' 'Jaipur' 'Goa'
 'Chennai']

 ## Price description of flights 
 count      30.000000
mean     5510.866667
std      1758.539240
min      2792.000000
25%      4088.750000
50%      5422.000000
75%      6760.250000
max      8981.000000
Name: price, dtype: float64


#### Unique hotel cities
['Delhi', 'Mumbai', 'Goa', 'Bangalore', 'Chennai', 'Hyderabad',
       'Kolkata', 'Jaipur']


#### Price per night description
count      40.000000
mean     4129.800000
std      1638.216153
min      1232.000000
25%      2806.750000
50%      4069.500000
75%      5652.000000
max      6481.000000
Name: price_per_night, dtype: float64



#### Unique values in places column : 
Unique values in 'name': ['Famous Fort' 'Beautiful Temple' 'Historic Fort' 'Popular Museum'
 'Famous Museum' 'Beautiful Fort' 'Historic Temple' 'Famous Lake'
 'Popular Lake' 'Famous Park' 'Historic Park' 'Beautiful Park'
 'Beautiful Lake' 'Popular Fort' 'Scenic Museum' 'Historic Lake'
 'Scenic Temple' 'Popular Temple' 'Scenic Park' 'Famous Temple']
Unique values in 'city': ['Delhi' 'Mumbai' 'Goa' 'Bangalore' 'Chennai' 'Hyderabad' 'Kolkata'
 'Jaipur']
Unique values in 'type': ['lake' 'temple' 'museum' 'park' 'fort' 'beach' 'market' 'monument']


#### Unique Values in flights 
Unique values in 'airline': ['IndiGo' 'Air India' 'SpiceJet' 'Go First' 'Vistara']
Unique values in 'from': ['Hyderabad' 'Delhi' 'Chennai' 'Bangalore' 'Goa' 'Kolkata' 'Jaipur'
 'Mumbai']
Unique values in 'to': ['Delhi' 'Kolkata' 'Hyderabad' 'Mumbai' 'Bangalore' 'Jaipur' 'Goa'
 'Chennai']



#### Unique values in hotels 
Unique values in 'name': ['Grand Palace Hotel' 'Comfort Suites' 'Green Leaf Resort' 'Sunrise Hotel'
 'Blue Lagoon Resort' 'Budget Stay Inn' 'Royal Heritage' 'Sea View Resort'
 'City Center Hotel']
Unique values in 'city': ['Delhi' 'Mumbai' 'Goa' 'Bangalore' 'Chennai' 'Hyderabad' 'Kolkata'
 'Jaipur']
 


