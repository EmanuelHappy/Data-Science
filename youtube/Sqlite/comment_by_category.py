from sqlitedict import SqliteDict

splits = [i*10000000 for i in range(5, 8)]

actual_category = "none"
category_dict = SqliteDict(f"./split_texts/AL.sqlite", tablename="value", journal_mode="OFF")
text_dict = SqliteDict(f"./split_texts/text_dict_{0}.sqlite", tablename="value", flag="r")

c = 0;
try:
	for num in splits:
		category_dict.commit()
		text_dict.close()
		text_dict = SqliteDict(f"./split_texts/text_dict_{num}.1.sqlite", tablename="value", flag="r")

		print(num)
		for id_c, value in text_dict.items():
			if value["category"] == "Alt-lite":
				if c==0:
					print(c)
					c = 1
			
				category_dict[id_c] = value

except:
	category_dict.commit()
	category_dict.close()
category_dict.commit()
category_dict.close()
