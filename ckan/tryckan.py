#!/usr/bin/env python
from urllib.request import urlopen
import urllib
import json
import pprint

# Make the HTTP request.
response = urlopen('https://data.gov.au/data/api/3/action/organization_list')
assert response.code == 200
print(response)

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.read())

# Check the contents of the response.
assert response_dict['success'] is True
result = response_dict['result']
pprint.pprint(result)

