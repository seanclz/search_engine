'''import json

catalog_fridges = [json.loads(line) for line in open('catalogs/full_refrigerators.json', 'r')]
catalog_grills = [json.loads(line) for line in open('catalogs/full_grills.jsonl', 'r')]
    # catalog_clothes = json.load(open('../catalogs/catalog_clothes.json'))

for doc in catalog_grills:
    dic = {}
    for k, v in doc.items():
        if k  == 'title':
            print(v)
'''

'Calculator for DCG'

import math
import pandas as pd
'''queries = ["0.7-cu concord mini fridge in blue",
"12.9-cu refrigerator",
"14-cu ft top freezer",
"1500 watt electric grill",
"189-sq portable grill",
"2.8-cu ft fridge",
"21.5-in kettle charcoal grill",
"22-in grill from kamado",
"289-sq grill",
"3 burner gas grill",
"36-in refrigerator",
"4-door refrigerator",
"5-burner gas grill from broil king",
"barrel grill",
"better chef grill in red",
"black barrel grill",
"black bottom-freezer refrigerator",
"black bottom-freezer refrigerator",
"black kettle grill in porcelain",
"black refrigerator top-freezer",
"blue rhino grill",
"bottom freezer in stainless steel",
"bottom-freezer refrigerator with ice maker",
"built-in grill",
"cal flame propane gas grill",
"ceramic grill",
"char-broil natural gas grill",
"charcoal grill from apollo series",
"charcoal grill from picnic time",
"charcoal grill in black",
"charcoal smoker",
"concord mini fridge",
"cooluli mini fridge",
"counter depth black fridge",
"counter-depth refrigerator in black",
"dual door fridge",
"electric black grill",
"electric grill in satin black",
"electric grill in white",
"energy star freezer",
"family hub refrigerator",
"fingerprint resistant fridge",
"flat top grill",
"freestanding mini fridge",
"freezerless refrigerator",
"french door refrigerator with printshield",
"frigidaire freezer in white",
"garage ready refrigerator in black",
"garage ready top-freezer",
"gas grill from Rogue XT",
"grill in grey from prestige series",
"grill with 1 side burner in black",
"grill with 1 side burner in stainless steel",
"grill with 4 main burners",
"grill with rotisserie burner",
"imperial international bucket grill",
"infinity fridge",
"infrared gas grill",
"instaview refrigerator",
"kettle charcoal grill",
"LG wi-fi refrigerator",
"lifesmart grill",
"lightweight grill",
"mini fridge freezer",
"napoleon grill rotisserie",
"napoleon grill with 1 side burner",
"napoleon travel q grill",
"natural gas ruby grill",
"oklahoma joe grill",
"pellet grill",
"pellet grill and smoker",
"pit boss grill",
"pit boss pellet grill",
"portable gas grill in aluminum",
"premium kettle grill",
"premium levella refrigerator",
"prime pellet grill",
"propane grill with 4 burners",
"red mini fridge",
"refrigerator bottom-freezer",
"refrigerator with dual ice maker",
"refrigerator with water dispenser",
"side by side refrigerator with ice maker",
"side-by-side  refrigerator",
"silver fridge",
"smart refrigerator",
"Stainless steel  gas grill",
"stainless steel black fridge",
"stainless steel french door refrigerator",
"titanium portable grill",
"top-freezer fridge in white",
"weber black grill",
"weber grill",
"weber grill spirit",
"weber liquid propane grill",
"whirlpool refrigerator",
"white grill",
"white mini fridge",
"white refrigerator with ice maker",
"wi-fi fridge with ice maker"]'''

queries = ["energy star freezer",
"garage ready top-freezer",
"side by side refrigerator with ice maker",
"bottom-freezer refrigerator with ice maker",
"black bottom-freezer refrigerator ",
"instaview refrigerator",
"barrel grill",
"black barrel grill",
"napoleon travel q grill",
"189-sq portable grill",
"289-sq grill",
"premium kettle grill",
"1500 watt electric grill",
"propane grill with 4 burners",
"kettle charcoal grill",
"17.5 cu fridge",
"silver fridge",
"bottom freezer in stainless steel",
"smart refrigerator",
"family hub refrigerator",
"red mini fridge",
"dual door fridge",
"lightweight grill",
"pit boss pellet grill",
"weber grill",
"weber black grill",
"white grill",
"blue rhino grill",
"weber grill spirit",
"prime pellet grill",
"lifesmart grill",
"12.9-cu ft fridge",
"infinity fridge",
"garage ready refrigerator in black",
"cooluli mini fridge",
"grill with rotisserie burner",
"napoleon grill rotisserie"]

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

jina_tail_queries = ["refrigerator with french door and ice maker in stainless steel",
"portable gas grill in black with gray accents",
"black kettle charcoal grill in porcelain from Performer Deluxe",
"infrared gas grill with rotisserie burner from prestige black",
"propane gas grill with 2 burners from spirit II",
"natural gas infrared grill in silver with 1-burner",
"liquid propane gas grill with 3 burner in red color",
"natural gas infrared grill in silver with 1 burner",
"gas grill with side burner from rogue XT in stainless steel",
"side by side refrigerator with ice maker in stainless steel from Profile",
"electric barbecue grill from Better Chef",
"black pellet grill from LG Series",
"portable lightweight charcoal grill",
"counter-depth refrigerator with ice maker in white",
"stainless steel grill with 4-burner and 1 side-burner from Rogue XT",
"charcoal grill from Napoleon with 4 burner",
"triple-function combo grill in black",
"built-in grill with liquid propane gas in stainless steel",
"liquid propane gas grill in stainless steel with 6-burner",
"natural gas grill with 5-burner from ruby"]

with open('dcg_scores.txt', 'w') as f:

    for query in jina_queries:
        print(query)
        list_values_whoosh = []
        list_values_whooshner = []
        print("Calculating DCG for JINA")
        for i in range(0,10):
            number = input("Input Document evaluation: \n")
            try:
                number = int(number)
                list_values_whooshner.append(number)
            except ValueError:
                break
        '''print("Calculating DCG for WHOOSH")
        for i in range(0, 10):
            number = input("Input Document evaluation: \n")
            try:
                number = int(number)
                list_values_whoosh.append(number)
            except ValueError:
                break'''

        list_dcg_whooshner = []
        for i in range(0, len(list_values_whooshner)):
            reli = list_values_whooshner[i]
            dcg = reli / (math.log(i + 2, 2))
            list_dcg_whooshner.append(dcg)

        list_dcg_whoosh = []
        for i in range (0, len(list_values_whoosh)):
            reli = list_values_whoosh[i]
            dcg = reli / (math.log(i+2,2))
            list_dcg_whoosh.append(dcg)

        df_whoosh_dcg_ner = pd.DataFrame(list(zip(list_values_whooshner, list_dcg_whooshner)), columns=["Rel i", "DCG"])
        print(query)
        print(df_whoosh_dcg_ner)
        print("\n")
        print("DCG ranking for JINA is:  " + str(sum((map(float, list_dcg_whooshner)))))
        print("\n")
        f.write(query+"\n")
        dfAsString = df_whoosh_dcg_ner.to_string()
        f.write(dfAsString)
        f.write("\n")
        f.write("\n")
        f.write("DCG ranking for JINA is:  " + str(sum((map(float, list_dcg_whooshner)))))
        f.write("\n")
        f.write("\n")
        f.write("*********************************************************************")
        f.write("\n")
        f.write("\n")

        '''df_whoosh_dcg = pd.DataFrame(list(zip(list_values_whoosh, list_dcg_whoosh)), columns=["Rel i", "DCG"])
        print(df_whoosh_dcg)
        print("\n")
        print("DCG ranking for Whoosh_NER_FULLTEXT is:  " + str(sum((map(float, list_dcg_whoosh)))))
        print("\n")
        f.write(query + "\n")
        dfAsString = df_whoosh_dcg.to_string()
        f.write(dfAsString)
        f.write("\n")
        f.write("\n")
        f.write("DCG ranking for Whoosh_NER_FULLTEXT is:  " + str(sum((map(float, list_dcg_whoosh)))))
        f.write("\n")
        f.write("\n")
        f.write("*********************************************************************")
        f.write("\n")
        f.write("\n")'''




f.close()
'''list_values_jina = []
print("Calculating DCG for JINA")
while(True):
    number = input("Input Document evaluation: \n")
    try:
        number = int(number)
        list_values_jina.append(number)
    except ValueError:
        break

list_dcg_jina = []
for i in range (0, len(list_values_jina)):
    reli = list_values_jina[i]
    dcg = reli / (math.log(i+2,2))
    list_dcg_jina.append(dcg)'''


'''df_whoosh_dcg = pd.DataFrame(list(zip(list_values_whoosh,list_dcg_whoosh)), columns = ["Rel i", "DCG"])
print(df_whoosh_dcg)
print("\n")
print("DCG ranking for WHOOSH is:  "+str(sum((map(float,list_dcg_whoosh)))))
print("\n")'''
'''df_jina_dcg = pd.DataFrame(list(zip(list_values_jina,list_dcg_jina)), columns = ["Rel i", "DCG"])
print(df_jina_dcg)
print("\n")
print("DCG ranking for JINA is:  "+str(sum((map(float,list_dcg_jina)))))
print("\n")
print("_______________________________________________________________________")
print("\n Query  ")'''