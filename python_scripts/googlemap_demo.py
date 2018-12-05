import googlemaps
from time import sleep
import pandas as pd
from tqdm import tqdm
import numpy as np
from datetime import datetime
from pprint import pprint
API_KEY = 'AIzaSyD9mARopyCHqRvb8_dTYlaPOo90fPwKvhw'
gmaps = googlemaps.Client(key=API_KEY)


target_geo = (22.3964, 114.1095)
search_keyword = 'Siu On Court'

res = gmaps.places(location=target_geo,query=search_keyword,radius=150)['results']
pprint(res)