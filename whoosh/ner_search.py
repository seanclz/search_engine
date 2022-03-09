import pandas as pd
import json

catalog_fridges = [json.loads(line) for line in open('../catalogs/full_refrigerators.json', 'r')]
catalogs_grills = [json.loads(line) for line in open('../catalogs/full_grills.jsonl', 'r')]
#catalog_clothes = json.load(open('../catalogs/catalog_clothes.json'))
#catalog_clothes = pd.read_json('../catalogs/catalog_clothes.json')

import crf
from crf import ner_extract
crf = crf.train_crf()

from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, NUMERIC
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.analysis.tokenizers import default_pattern


class NERTokenizer(RegexTokenizer):
     """Named Entity centric version of RegexTokenizer"""
     def __init__(self, expression= default_pattern, gaps=False):
         super().__init__(expression=expression, gaps=gaps)

     def __call__(self, text, **kwargs):
        text = ner_extract(crf,text)
        #print(text)
        return super().__call__(text, **kwargs)

def NERAnalyzer(expression= default_pattern, minsize=2, maxsize=None, gaps=False):
     """Named Entity centric version of StandardAnalyzer"""
     chain = NERTokenizer(expression, gaps)
     chain |= LowercaseFilter()
     chain |= StopFilter(minsize=minsize, maxsize=maxsize)
     return chain

class LowesCatalogSchema(SchemaClass):
    description = TEXT(stored=True)
    full_description = TEXT(stored=True)
    product_url = TEXT
    image_url = TEXT(stored=True)
    title = TEXT(stored=True)
    brand = TEXT(stored=True)
    title_NE = TEXT(stored=True, analyzer=NERAnalyzer())
    description_NE = TEXT(stored=True, analyzer=NERAnalyzer())
    #min_price = NUMERIC
    #max_price = NUMERIC
    #rating = NUMERIC
    #categories = TEXT
    #details = TEXT
    #omni_item_id = NUMERIC
    #model_id = ID(stored=True)
    #item_number = TEXT


schema = LowesCatalogSchema

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

from whoosh import index
ix = index.create_in("indexdir", schema)

ix = index.open_dir("indexdir")
writer = ix.writer()

for doc in catalog_fridges:

    d = {}
    for k,v in doc.items():
        if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
            d[k] = v
            if k == 'title':
                d['title_NE'] = d['title']
            '''if k == 'description':
                d['description_NE'] = d['description']'''
        if k == 'details':
            for k2,v2 in v.items():
                if k2 in ['Full Description']:
                    d['full_description'] = v2
                    d['description_NE'] = d['full_description']

    writer.add_document(**d)
    #d = {k: v for k,v in doc.items() if k in ['Full Description', 'description', 'product_url', 'image_url', 'title', 'brand']}
    #print(d)
    #writer.add_document(**d)

for doc in catalogs_grills:

    d = {}
    for k, v in doc.items():
        if k in ['description', 'product_url', 'image_url', 'title', 'brand']:
            d[k] = v
            if k == 'title':
                d['title_NE'] = d['title']
                '''if k == 'description':
                d['description_NE'] = d['description']'''
        if k == 'details':
            for k2,v2 in v.items():
                if k2 in ['Full Description']:
                    d['full_description'] = v2
                    d['description_NE'] = d['full_description']

    writer.add_document(**d)
    '''d = {k: v for k, v in doc.items() if k in ['description', 'product_url', 'image_url', 'title', 'brand']}
    # print(d)
    writer.add_document(**d)'''


writer.commit(optimize=True)

from whoosh.qparser import QueryParser, MultifieldParser, WildcardPlugin
print(ix.schema)


'''while(True):
        sentence = input("Insert your query  \n")
'''
f = open("tailqueries_ner.txt","w")
for query in tail_queries:
#while(True):
    qp = MultifieldParser(["title", "full_description", "brand", "title_NE", "description_NE", "description"],
                           schema=ix.schema)
    #for query in tail_queries:
    print("*************************************************************************")
    print(query + "\n")
    f.write("***********************************************************************\n")
    f.write(query + "\n")
    #query = input(u"Insert query: \n")
    ne = ner_extract(crf,query)
    q = qp.parse(ne)
    with ix.searcher() as s:
            results = s.search(q, limit=10)
            for result in results:
                f.write(result["title"]+"\n")
                f.write(result["full_description"]+"\n")
                f.write("_________________________\n")
                print(result["title"]+"\n")
                print(result["full_description"]+"\n")
                print("____________________________")
f.close()