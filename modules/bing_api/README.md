# Bing API

Python 3 module acting as a simple wrapper for the [Microsoft/Bing Maps Traffic API](https://msdn.microsoft.com/en-us/library/hh441725.aspx).

## Setup

Install the following pip dependency:
* `requests`

Setup the [Logger](https://github.com/jleung51/scripts/tree/master/modules/logger) module in this directory.

### Creating a Bing Maps Authentication Key

An authentication key is required to use Bing Maps. A key looks like this: `Aqcn-mAQ276K6K4Xl6gnx-Ld5hDQ8a3MVB-awpLpKLJak3aZsqWf7gs3t1IIKl3v`.

To create a key, go to the [Bing Maps Portal](https://www.bingmapsportal.com/). Create an account or sign in. Under _My Account_ select _My Keys_. Follow the instructions to create a new key.

For more details about the authentication key, see [Bing Maps REST URL Structure](https://msdn.microsoft.com/en-ca/library/ff701720.aspx).

## Usage

Add the `bing_api.py` module to the directory of the Python program. Import the module in your program:
```
from bing_api import BingApi
```

Create a `BingApi` object with the authentication key created during _Setup_:
````
b = BingApi(auth_key)
```

And retrieve the traffic data from Bing Maps using coordinates to create a box around the incident area:
```
coordinate_southwest = "45.219, -122.325"
coordinate_northeast = "46.610, -122.107"
results = b.get_traffic_data(coordinate_southwest, coordinate_northeast)
print(results.json())
```

Or using coordinates as well as severity and type to filter results:
```
coordinate_southwest = "45.219, -122.325"
coordinate_northeast = "46.610, -122.107"
severity = "1, 2, 3, 4"
type = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
results = b.get_traffic_data(coordinate_southwest, coordinate_northeast, severity, type)
print(results.json())
```

Or do the same, but with simpler human-readable output:
```
results = b.get_traffic_data_readable(coordinate_southwest, coordinate_northeast, severity, type)
print(results)
```

For detailed information on the parameters and usage, see the documentation in the class for the desired API.
