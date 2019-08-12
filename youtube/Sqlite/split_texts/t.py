from sqlitedict import SqliteDict
from time import time


new_value_dict = SqliteDict(f'test_split10000000.sqlite', tablename="value")


for key, value in new_value_dict.items():
   print(key, value)
