from bs4 import BeautifulSoup
from pprint import pprint
with open('json_report/people-2024-04-29.json', 'r') as f:
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "xml")

print(Bs_data)
# Using find() to extract attributes
# of the first instance of the tag
b_name = Bs_data.find('raws', {'email':'guzmantello.2091184@studenti.uniroma1.it'})

print(b_name)

# Extracting the data stored in a
# specific attribute of the
# `child` tag
#value = b_name.get('test')
#
#print(value)
