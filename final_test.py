import requests
import csv
import sqlite3
import pandas as pd
import seaborn as sns; sns.set(color_codes=True)
import matplotlib.pyplot as plt

#Calling Data

conn = sqlite3.connect("test.sqlite")
cur = conn.cursor()
cur.execute("drop table if exists Drug_Death_County;")
cur.execute("""
create table if not exists Drug_Death_County(
    FIPS varchar(5),
    Year varchar (4),
    State varchar (20),
    FIPS_State varchar (2),
    County varchar (100),
    Population varchar (20),
    Estimated_Age_Adjusted_Death_Rate varchar (15)    
    );
""")

url = "https://data.cdc.gov/api/views/p56q-jrxg/rows.csv?accessType=DOWNLOAD"
response = requests.get(url)
if response.status_code !=200:
    print('Failed to get data:', response.status_code)
else:
    wrapper = csv.reader(response.text.strip().split('\n'))
    headerline = True
    for record in wrapper:
        if headerline:
            headerline = False
        else:
            cur.execute("INSERT INTO Drug_Death_County(FIPS, Year, State, FIPS_State, County, Population, Estimated_Age_Adjusted_Death_Rate) VALUES(?,?,?,?,?,?,?)", (record))

#Pulling Wet Counties information

cur.execute("select * from Drug_Death_County WHERE State='Kentucky' AND FIPS IN (21005,21015,21017,21019,21021,21023,21029,21035,21037,21041,21047,21049,21051,21059,21067,21071,21077,21079,21093,21095,21097,21101,21103,21107,21111,21113,21115,21117,21133,21135,21141,21151,21153,21155,21161,21163,21173,21177,21179,21181,21185,21191,21193,21195,21199,21205,21209,21211,21213,21215,21219,21221,21225,21227,21229,21235,21237,21239,21073,21075,21145);")
Drug_Death_County_Wet = cur.fetchall()
Drug_Death_County_Wet = [list(elem) for elem in Drug_Death_County_Wet]

df_Wet = pd.DataFrame(Drug_Death_County_Wet)
df_Wet.columns=['FIPS', 'Year', 'State', 'FIPS_State', 'County', 'Population', 'Estimated_Age_Adjusted_Death_Rate']

cs_Wet = df_Wet['County']
clean_cs_Wet = cs_Wet.str.replace(" County, KY", "")
df_cs_Wet = pd.DataFrame(clean_cs_Wet)

merged_Wet = pd.merge(df_Wet, df_cs_Wet, right_index=True, left_index=True)

cdr_Wet = df_Wet['Estimated_Age_Adjusted_Death_Rate']

clean_cdr_Wet = cdr_Wet.str.replace("<2", "1")
clean_cdr_Wet = clean_cdr_Wet.str.replace("+", "")
clean_cdr_Wet = clean_cdr_Wet.str.rsplit('-', 1, True)
del clean_cdr_Wet[1]
df_cdr_Wet = pd.DataFrame(clean_cdr_Wet)

final_df_Wet = pd.merge(merged_Wet, df_cdr_Wet, right_index=True, left_index=True)
del final_df_Wet['Estimated_Age_Adjusted_Death_Rate']
del final_df_Wet['County_x']
del final_df_Wet['FIPS_State']
del final_df_Wet['FIPS']
final_df_Wet.columns=['Year', 'State', 'Population', 'County', 'Estimated_Age_Adjusted_Death_Rate']
final_df_Wet['Estimated_Age_Adjusted_Death_Rate'] = final_df_Wet['Estimated_Age_Adjusted_Death_Rate'].astype('int64')
final_df_Wet['Year'] = final_df_Wet['Year'].astype('int64')

#Pulling Dry Counties information

cur.execute("select * from Drug_Death_County WHERE State='Kentucky' AND FIPS IN (21001,21003,21007,21009,21011,21013,21025,21027,21031,21033,21039,21043,21045,21053,21055,21057,21061,21063,21065,21069,21081,21083,21085,21087,21089,21091,21099,21105,21109,21119,21121,21123,21125,21127,21129,21131,21137,21139,21143,21147,21149,21157,21159,21165,21167,21169,21171,21175,21183,21187,21189,21197,21201,21203,21207,21217,21223,21231,21233);")
Drug_Death_County_Dry = cur.fetchall()
Drug_Death_County_Dry = [list(elem) for elem in Drug_Death_County_Dry]

df_Dry = pd.DataFrame(Drug_Death_County_Dry)
df_Dry.columns=['FIPS', 'Year', 'State', 'FIPS_State', 'County', 'Population', 'Estimated_Age_Adjusted_Death_Rate']

cs_Dry = df_Dry['County']
clean_cs_Dry = cs_Dry.str.replace(" County, KY", "")
df_cs_Dry = pd.DataFrame(clean_cs_Dry)

merged_Dry = pd.merge(df_Dry, df_cs_Dry, right_index=True, left_index=True)

cdr_Dry = df_Dry['Estimated_Age_Adjusted_Death_Rate']

clean_cdr_Dry = cdr_Dry.str.replace("<2", "1")
clean_cdr_Dry = clean_cdr_Dry.str.replace("+", "")
clean_cdr_Dry = clean_cdr_Dry.str.rsplit('-', 1, True)
del clean_cdr_Dry[1]
df_cdr_Dry = pd.DataFrame(clean_cdr_Dry)

final_df_Dry = pd.merge(merged_Dry, df_cdr_Dry, right_index=True, left_index=True)
del final_df_Dry['Estimated_Age_Adjusted_Death_Rate']
del final_df_Dry['County_x']
del final_df_Dry['FIPS_State']
del final_df_Dry['FIPS']
final_df_Dry.columns=['Year', 'State', 'Population', 'County', 'Estimated_Age_Adjusted_Death_Rate']
final_df_Dry['Estimated_Age_Adjusted_Death_Rate'] = final_df_Dry['Estimated_Age_Adjusted_Death_Rate'].astype('int64')
final_df_Dry['Year'] = final_df_Dry['Year'].astype('int64')

#Plotting the data

plt.figure(1)
p_Dry = sns.regplot(x='Year', y='Estimated_Age_Adjusted_Death_Rate', data=final_df_Dry).set_title('Dry Counties')
plt.xticks([1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016])

plt.figure(2)
p_Wet = sns.regplot(x='Year', y='Estimated_Age_Adjusted_Death_Rate', data=final_df_Wet).set_title('Wet Counties')
plt.xticks([1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016])

plt.show()
