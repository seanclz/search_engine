import pandas as pd
import json

catalog_fridges = [json.loads(line) for line in open('../catalogs/full_refrigerators.json', 'r')]
catalogs_grills = [json.loads(line) for line in open('../catalogs/full_grills.jsonl', 'r')]
#catalog_clothes = json.load(open('../catalogs/catalog_clothes.json'))
#catalog_clothes = pd.read_json('../catalogs/catalog_clothes.json')

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC

class LowesCatalogSchema(SchemaClass):
    #omni_item_id = NUMERIC
    #model_id = ID(stored=True)
    #item_number = TEXT
    description = TEXT(stored=True)
    full_description = TEXT(stored=True)
    product_url = TEXT
    image_url = TEXT(stored=True)
    title = TEXT(stored=True)
    #min_price = NUMERIC
    #max_price = NUMERIC
    brand = TEXT(stored=True)
    #rating = NUMERIC
    #categories = TEXT
    #details = TEXT

'''class ClothesCatalogSchema(SchemaClass):
    #pid = ID(stored = True)
    #id = ID(stored=True)
    product_url = TEXT
    image_url = TEXT
    #category_url = TEXT
    title = TEXT(stored=True)
    description = TEXT
    # LABEL = BRAND
    label = TEXT(stored=True)
    #standard_price = NUMERIC
    #sales_price = NUMERIC
    #size = TEXT
    #attr_type = TEXT
    #color = TEXT
    #attr_values = TEXT'''

schema = LowesCatalogSchema

from whoosh import index
ix = index.create_in("indexdir", schema)

ix = index.open_dir("indexdir")
writer = ix.writer()

for doc in catalog_fridges:

    d = {}
    for k,v in doc.items():
        if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
            d[k] = v
        if k == 'details':
            for k2,v2 in v.items():
                if k2 in ['Full Description']:
                    d['full_description'] = v2

    writer.add_document(**d)
    #d = {k: v for k,v in doc.items() if k in ['Full Description', 'description', 'product_url', 'image_url', 'title', 'brand']}
    #print(d)
    #writer.add_document(**d)

for doc in catalogs_grills:

    d = {}
    for k, v in doc.items():
        if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
            d[k] = v
        if k == 'details':
            for k2,v2 in v.items():
                if k2 in ['Full Description']:
                    d['full_description'] = v2

    writer.add_document(**d)
    '''d = {k: v for k, v in doc.items() if k in ['description', 'product_url', 'image_url', 'title', 'brand']}
    # print(d)
    writer.add_document(**d)'''

'''for doc in catalog_clothes:
    d = {k: v for k,v in doc.items() if k in ['desc','url', 'img_url','title', 'label']}
    d['product_url'] = d.pop('url')
    d['description'] = d.pop('desc')
    d['image_url'] = d.pop('img_url')
    d['brand'] = d.pop('label')
    writer.add_document(**d)'''

tail_queries = ["liquid propane gas grill from clearview with 2 stainless burners",
"gas grill with 3-burner from char broil",
"refrigerator with french door and ice maker in stainless steel",
"stainless printproof refrigerator with french door and wi-fi",
"mini fridge with freezer compartment in green",
"top-freezer refrigerator in stainless steel from ENERGY STAR",
"side by side refrigerator in black with ice maker",
"refrigerator with ice maker in black stainless steel with printshield",
"fridge in stainless steel from hisense",
"electric grill in satin black with 1500-watt",
"portable gas grill in black with gray accents",
"black charcoal grill from charcoal grill series",
"black kettle charcoal grill in porcelain from Performer Deluxe",
"infrared gas grill with rotisserie burner from prestige black",
"propane gas grill with 2 burners from spirit II",
"natural gas infrared grill in silver with 1-burner",
"liquid propane gas grill with 3 burner in red color",
"natural gas infrared grill in silver with 1 burner",
"gas grill with side burner from rogue XT in stainless steel",
"natural gas built-in grill with 5-burner in liquid propane",
"side by side refrigerator with ice maker in stainless steel from Profile",
"refrigerator in stainless steel with 2-Drawer",
"mini fridge with freezer compartment black",
"french door refrigerator with 4 door with ice maker and in stainless steel",
"freestanding mini fridge in silver",
"freestanding mini fridge with  freezer compartment in stainless steel",
"top-freezer refrigerator with ice maker in stainless steel from ENERGY STAR",
"white top-freezer refrigerator with ice maker",
"top-freezer refrigerator in stainless steel and fingerprint resistant",
"natural gas built-in grill with 4-burner from Ruby ",
"electric barbecue grill from Better Chef",
"black pellet grill from LG Series",
"portable lightweight charcoal grill",
"red kettle charcoal grill from Coca Cola",
"Freestanding 2-Drawer Refrigerator in stainless steel ",
"bottom-freezer refrigerator in stainless steel and black",
"counter-depth refrigerator with ice maker in white",
"counter-depth refrigerator side-by-side with ice maker in black ",
"smudge proof refrigerator with ice maker in stainless steel",
"metallic freestanding mini fridge in red",
"refrigerator with ice maker in stainless steel with wi-fi",
"liquid propane gas grill in silver with 1-burner",
"propane gas grill in stainless steel with 3-burner in black and silver color",
"portable gas grill in red from travel q",
"portable gas grill in cast aluminum in blue color",
"charcoal smoker and grill from AC Milan ",
"kamado charcoal grill in black from LG Ceramic Series",
"gas grill with 5-burner in Prestige black",
"gas grill with rotisserie and side burner in prestige grey",
"liquid propane gas grill with 3-burner in black",
"stainless steel grill with 4-burner and 1 side-burner from Rogue XT",
"charcoal grill from Napoleon with 4 burner",
"pellet grill in bronze from Smoke Pro ",
"triple-function combo grill in black",
"built-in grill with liquid propane gas in stainless steel",
"liquid propane gas grill in stainless steel with 6-burner",
"4-burner stainless steel gas grill kamado",
"natural gas grill with 5-burner from ruby",
"refrigerator with dual doors in stainless steel ",
"freestanding mini fridge from Cooluli 0.14-cu"]

writer.commit(optimize=True)

from whoosh.qparser import QueryParser, MultifieldParser

print(ix.schema)
f = open("tailqueries_fulltext.txt","w")
for query in tail_queries:
#while(True):
    qp = MultifieldParser(["title", "full_description","description","brand"], schema=ix.schema)
    print("*************************************************************************")
    print(query + "\n")
    f.write("***********************************************************************\n")
    f.write(query + "\n")
    #user_query = input(u"Insert what you are searching for:")
    #q = qp.parse(user_query)
    q = qp.parse(query)
    with ix.searcher() as s:
            results = s.search(q, limit=10)
            for result in results:
                f.write(result["title"] + "\n")
                f.write(result["full_description"]+"\n")
                f.write("_________________________\n")
                print(result["title"])
                print(result["full_description"]+"\n")
                print("____________________________")
f.close()