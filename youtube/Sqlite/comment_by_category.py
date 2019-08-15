from sqlitedict import SqliteDict

splits = [i*10000000 for i in range(8)]

actual_category = "none"
category_dict = SqliteDict(f"./split_texts/non.sqlite", tablename="value", journal_mode="OFF")

for i in splits:
    text_dict = SqliteDict(f"./split_texts/text_dict_{splits[0]}", tablename="value", flag="r")
    for id_c, value in text_dict.items():
        if value["category"] is not actual_category:
            actual_category = value["category"]

            category_dict.commit()
            category_dict.close()
            category_dict = SqliteDict(f"./split_texts/{actual_category}.sqlite",
                                       tablename="value", journal_mode="OFF")

        category_dict[id_c] = value

category_dict.commit()
category_dict.close()
