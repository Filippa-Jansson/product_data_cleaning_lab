
#Här på den nedre raden så importerar jag pandas så att den funkar här i denna fil.
#Jag använder dataframe för att läsa av json filen med pandas, sen la jag till sep=";" så pandas vet vilken seperator som används i filen,
#-så jag kan dela upp de i kolumner i gitbashen.
#I den här delen så skulle jag nog kunna säga att jag ingestar datan för att jag läser in rådata från jsonlab filen med pandas och laddar den in i en dataframe.
#Samt så lagrar jag all data i pandas dataframe minnet.

import pandas as pd

df = pd.read_csv("data/products_raw.csv", sep=";")

#Här läser jag fram datan från json filen, jag la till print som en liten "titel" för att göra det lite snyggt.
#Med df.head så får jag fram uppdelat i kollumner för id, name, price, currency.
#Därefter med skrev jag df.info för att få fram data infot från filen.

print("Data inläst:")
print(df.head(10))
print("\nInfo om datan:")
df.info()

#Här omvandlar jag allt inom price från filen till siffror, så det inte blir några error
for column in ["id", "name", "currency"]:
    df[column] = df[column].str.strip()
df["price"] = pd.to_numeric(df["price"], errors="coerce")

#Här försöker jag flagga problem från listan för de som fattas en currency. Jag använder .isna som ett sätt att upptäcka odentifierande/missing värden,
#-istället för att använda true/false metoden som man brukar använda inom kodning. 
#Jag försöker också koda så att de som har ingen pris är lika med 0 och ska flaggas.
#Därefter lägger jag en price limit på 10k så de produkterna som kostar över 10k ska flaggas

df["missing_currency"] = df["currency"].isna()

df["zero_price"] = df["price"] == 0

EXTREME_PRICE_LIMIT = 10000   # flagged as possible luxury products
MAX_VALID_PRICE = 100000      # higher prices are treated as data errors
df["extreme_price"] = df["price"] > EXTREME_PRICE_LIMIT

#Här försöker jag rensa så att de "konstiga" värden inte kommer i kodningen t.ex. priser som visar negativt, saknade priser och priser som saknar valuta.
#Jag använder .notna för att göra en true/false för de värden som finns i filen och >= 0 så att det inte visas negativa priser (mindre än 0).
#Sedan print för att visa alla giltiga produkter från listan, vilket jag får fram 46 giltiga produkter.

valid_products = df[
    (df["id"].notna()) &
    (df["name"].notna()) &
    (df["price"].notna()) &
    (df["price"] >= 0) &
    (df["currency"].notna()) &
    (df["price"] <= MAX_VALID_PRICE)
]
#Här skickar jag alla giltiga produkter i rensade produkter listan för att göra det lite snyggare och lagrar datan i en anna fil.
valid_products.to_csv("output/valid_products.csv", index=False)

print("\nAntal giltiga produkter:", len(valid_products))

#Här sammanfattar jag min analytics summary för snittpris, medianpris, antal giltiga produkter och antal produkter som saknar pris.
#Jag använder .mean för att få fram snitpriset från listan, .median för att får median pris, len för att lista alla giltiga produkter,
#-isna för att få fram produkterna som saknar pris.
#Därefter skapar jag en ny fil med all sammanfattning från jsonlab filen med titlarna, gjorde också en print för att informera att en summary 
#-har skapats.

average_price = valid_products["price"].mean()
median_price = valid_products["price"].median()
total_products = len(valid_products)
missing_price_count = df["price"].isna().sum()

analytics_summary = pd.DataFrame({
    "snittpris": [average_price],
    "medianpris": [median_price],
    "antal_produkter": [total_products],
    "antal_produkter_med_saknat_pris": [missing_price_count]
})

analytics_summary.to_csv("output/analytics_summary.csv", index=False)

print("\nanalytics_summary.csv har skapats")

print(analytics_summary)

#Pandas är ett vertyg som man använder för att samla all data och för att kunna analysera som jag har gjort i denna uppgift (om man ska vara kortfattat).
#Psychopg3 är en populär postgreSQL-databasadaptern för python. Tyvärr så använder jag inte den i denna uppgift men den ska vara bra för att läsa av json filer.