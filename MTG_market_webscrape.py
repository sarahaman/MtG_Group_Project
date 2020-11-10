from bs4 import BeautifulSoup as soup
import requests
import pandas as pd

link = 'https://shop.tcgplayer.com/price-guide/magic/'

page = requests.get(
    'https://shop.tcgplayer.com/price-guide/magic/commander-collection-green', 
                    timeout=10)

content = soup(page.text, "html.parser")

sets = content.find_all(class_='priceGuideDropDown')

sets = sets[1]

set_links = []
set_names = []

options = sets.find_all('option')

for i in options:
    val = i['value']
    set_links.append(val)
    name = i.text
    set_names.append(name)

setTuples = tuple(zip(set_names, set_links))

finalDF = pd.DataFrame(columns=['Card Name', 'Rarity', 'Serial no.', 
                           'Market Price', 'Buylist Price', 'Listed Median',
                           'Set Name'])
frames = []

for n, p in enumerate(setTuples):
    page = requests.get(link+p[1], timeout = 10)
    content = soup(page.text, "html.parser")
    tbody = content.find('tbody')
    trs = tbody.find_all('tr')
    final_results = []
    
    try:
        if len(trs) > 0:
            for i in trs:
                results = i.text.strip().splitlines()
                results = [i for i in results if i]
                final_results.append(results)
            df = pd.DataFrame.from_records(final_results)
            drops = []
    
            for i in df:
                for j in df[i]:
                    if (j =='View') or (j =='                            '):
                        drops.append(i)
                        break
                    else:
                        break
            
            df = df.drop(df.columns[drops], axis=1)
            if len(df.columns) < 6:
                inserts = []
                for b in range(len(df)):
                    inserts.append('—')
                df.insert(loc=2, column=2, value=inserts)
            df.columns = ['Card Name', 'Rarity', 'Serial no.', 
                      'Market Price', 'Buylist Price', 'Listed Median']
            setName = []
            
            for j in range(len(df['Card Name'])):
                setName.append(str(p[0]))
            df['Set Name'] = setName
            finalDF = pd.concat([finalDF, df])
    except:
        continue
    
finalDF.to_csv(r'C:\Users\howle\Desktop\Data Munging\MTG Market Info.csv',
               index=False)