# Google Maps API Wrapper
A simple Python wrapper for Google Maps API with HTTP requests and returning
the data you need without going through parsing JSONs. Built with the
requests library.

## Prerequisites
This library uses the **requests** library to send and parse HTTP requests and
**polyline** to decode the polyline strings (optional if you have your own
decoder).
```text
pip install requests
pip install polyline
```

## Getting Started
The library includes wrappers for all API offerings (Directions, Places, 
Geocoding, and Roads API). You can import the wrapper you need by selecting
which class to import.
```python
# example with the Directions API
from GoogleMapsAPI import Directions
```
It's important to note that all classes **must be instantiated with your API
key**. Go to [this link](https://console.cloud.google.com/) to get started.
(PS: You need an active credit card to avail the free credits.)
## Directions API
### Example
Here, I want to see the coordinates of Toronto (start point) and Montreal
(end point).
```python
from GoogleMapsAPI import Directions

gMaps = Directions("your key here")
gMaps.find("Toronto", "Montreal")

# This is a workaround to get typehints in your IDE. You can get away without it.
result : Directions.Place = gMaps.places[0]

print(result.get_coordinates())

# Without typehints: print(gMaps.places[0].get_coordinates())

print(result.get_steps())
print(result.steps[0].polyline)
```

#### Output
```python
{
    'start': [43.6533096, -79.3827656], # Toronto
    'end': [45.5017123, -73.5672184] # Montreal
}
20 # Number of steps
e`miGhmocNs@Rm@N]JmA^KBcAXQDUFc@JOFYNk@Rc@J # Polyline string to be decoded
```

### How to Use

You use ``find(origin : str, endpoint : str)`` to query the route between
two locations. This creates an instance of the Place class that has the methods
for extracting data from the JSON response.

After that, you have a few methods to choose from:

#### Get Coordinates (Directions.Place)
``get_coordinates(typeof : str)`` - Returns the coordinates of one or either
locations. ``typeof`` is set to ``all`` by default, returning a ``dict``. If
``typeof`` is set to either ``start`` or ``end``, it will only return a ``list``

#### Get Steps (Directions.Place)
``get_steps()`` - Creates a list of instances of the Step class then returns
the total number of steps. **You need to execute this method to load the
step data into the Step class**

**Example**
```python
x = gMaps.places[0].get_steps()
print(x)

# Output: 20
```

### Step

This class has the coordinates and polyline string of each step in the route
provided by the API. Most of the details like coordinates and HTML instructions
are set as properties and can be read. Some other methods are provided, however,
such as decoding the polyline string into a list of coordinates, or getting the
distances of each step from the next.

<table>
  <tr><td>Data</td><td>Property Name</td><td>Type</td></tr>
  <tr><td>HTML Instructions</td><td>.html_instructions</td><td>HTML (String)</td></tr>
  <tr><td>Polyline</td><td>.polyline</td><td>String</td></tr>
  <tr><td>Start Location</td><td>.start</td><td>List [lat,lng]</td></tr>
  <tr><td>End Location</td><td>.end</td><td>List [lat,lng]</td></tr>
</table>

#### Get Distance
``get_distance(typeof : str)`` - Returns the distance of the current step
from the next step. ``typeof`` is set to ``text`` in default, returning the
distance followed by a unit. Use ``value`` to get the raw integer (in meters)

**Example**
```python
print(gMaps.places[0].steps[0].get_distance())

# Output: 0.3km or 280 if typeof="value"
```

#### Decode Polyline
``decode_polyline()`` - Uses the decoder inside the polyline library to
return a ``list`` of ``tuples`` containing the LatLng coordinates.

**Example**
```python
print(gMaps.places[0].steps[0].decode_polyline())
# Output: [(43.65331, -79.38277),... (43.65573, -79.38373)]
```