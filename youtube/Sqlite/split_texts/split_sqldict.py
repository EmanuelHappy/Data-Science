from sqlitedict import SqliteDict
from time import time

source = "/../../../../scratch/manoelribeiro/helpers/text_dict.sqlite"

value_dict = SqliteDict(source, tablename="text", flag="r")
new_value_dict = SqliteDict(f'text_dict_{0}.sqlite', tablename="value")

c=0
for key, value in value_dict.items():
    c+=1
    if c%10000000 == 0:
        new_value_dict.commit()
        new_value_dict.close()
        
        new_value_dict = SqliteDict(f'test_split{c}.sqlite', tablename="value")
    
    new_value_dict[key] = value