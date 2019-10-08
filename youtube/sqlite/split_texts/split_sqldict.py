from sqlitedict import SqliteDict
from time import time

source = "/../../../../scratch/manoelribeiro/helpers/text_dict.sqlite"

print("Start")
value_dict = SqliteDict(source, tablename="text", flag="r")
print("value_dict")
new_value_dict = SqliteDict(f'text_dict_{0}_new2.sqlite', tablename="value", journal_mode='OFF')

c = 0
for key, value in value_dict.items():
	c += 1
	
	if c % 10000000 == 0:
		print(c)
		new_value_dict.commit()
		new_value_dict.close()
		
		new_value_dict = SqliteDict(f'text_dict_{c}_new2.sqlite', tablename="value", journal_mode='OFF')
	
	new_value_dict[key] = value
	
new_value_dict.commit()
new_value_dict.close()
