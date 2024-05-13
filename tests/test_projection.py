import os, sys
from os.path import abspath

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

import pprint as pp
import json

from models.projection import Projection
from models.projection_data import ProjectionData
from models.monthtype import Month
from data_api.jsonfile_api import *

p = Projection("Financial forecast 2024")

d1 = ProjectionData("2024", Month.JAN)
d1.add_item("income", "salary", 500)
d1.add_item("income", "interest", 10)
d1.add_item("expense", "living", 200.50)

d2 = ProjectionData("2024", Month.APR)
d2.add_item("income", "salary", 500)
d2.add_item("income", "interest", 40)
d2.add_item("expense", "living", 350.50)
d2.add_item("expense", "travel", 200)

p.add_new_projection_data(d1)
p.add_new_projection_data(d2)

res = p.get_projection_in_dict()

#write data to json file
FILENAME = "data/projection_2024.json"
print(f"Writing data to {FILENAME}")
with open(FILENAME, "w") as f:
    json.dump(res, f)

#read data from json file
absolute = abspath(FILENAME)
api = JsonFileApi(absolute)
data = api.extract_data()

print(f"Extracting data from {FILENAME}")
print(data)
