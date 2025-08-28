import re

import pandas as pd
import numpy as np


df=pd.read_csv('/Users/sujitkumarpatsani/PycharmProjects/PythonProject/resources/USA_cars_datasets.csv')
print(df)

# chck types of each column
#print(df.dtypes)

# Question 1 Extract the month out of the date in the format "Jan" "Feb" etc and create a separate column
# step-1 convert Date Object type to DateTime
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
#print(df.dtypes)
df['Month']=df['Date'].dt.strftime('%b')
print(df)

'''
Without .dt, df["Date"] is just a pandas Series.
With .dt, you can reach into each datetime value inside that Series and use datetime methods (like year, month, day, weekday, strftime, etc.).
'''
# Using .dt to extract parts
'''df["Year"] = df["Date"].dt.year        # 2013, 2025
df["MonthNum"] = df["Date"].dt.month  # 5, 8
df["Month"] = df["Date"].dt.strftime("%b")  # May, Aug
df["Weekday"] = df["Date"].dt.day_name()    # Tuesday, Friday
'''

print(df)

#Question -2 Extract the time out of it and create a separate column with values " afternoon , morning , evening , night " based on the hour .

df['Hour']=pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.hour
bins=[0,5,12,17,21,24]
labels = ["night", "morning", "afternoon", "evening", "night"]

df["TimeOfDay"] = pd.cut(df["Hour"], bins=bins, labels=labels, right=False, include_lowest=True,ordered=False)

print(df)

unique_states = df["state"].unique()
print(unique_states)

#3 3 - Create another data frame with the names of states and abbreviation of the state and join with the original data frame .

# Your unique states
states = [
    'new jersey','tennessee','georgia','virginia','florida','texas',
    'california','north carolina','ohio','new york','pennsylvania',
    'south carolina','michigan','washington','arizona','utah','kentucky',
    'massachusetts','nebraska','ontario','missouri','minnesota','oklahoma',
    'connecticut','indiana','arkansas','kansas','wyoming','colorado',
    'illinois','wisconsin','mississippi','maryland','oregon','west virginia',
    'nevada','rhode island','louisiana','alabama','new mexico','idaho',
    'new hampshire','montana','vermont'
]

# State → Abbreviation dictionary
abbr_dict = {
    "new jersey": "NJ", "tennessee": "TN", "georgia": "GA", "virginia": "VA",
    "florida": "FL", "texas": "TX", "california": "CA", "north carolina": "NC",
    "ohio": "OH", "new york": "NY", "pennsylvania": "PA", "south carolina": "SC",
    "michigan": "MI", "washington": "WA", "arizona": "AZ", "utah": "UT",
    "kentucky": "KY", "massachusetts": "MA", "nebraska": "NE", "ontario": "ON",  # Ontario = Canada
    "missouri": "MO", "minnesota": "MN", "oklahoma": "OK", "connecticut": "CT",
    "indiana": "IN", "arkansas": "AR", "kansas": "KS", "wyoming": "WY",
    "colorado": "CO", "illinois": "IL", "wisconsin": "WI", "mississippi": "MS",
    "maryland": "MD", "oregon": "OR", "west virginia": "WV", "nevada": "NV",
    "rhode island": "RI", "louisiana": "LA", "alabama": "AL", "new mexico": "NM",
    "idaho": "ID", "new hampshire": "NH", "montana": "MT", "vermont": "VT"
}

# Create dataframe
df_abbr = pd.DataFrame({
    "state": states,
    "abbr": [abbr_dict.get(s, None) for s in states]  # safely map abbreviations
})

print(df_abbr)

df_merged=pd.merge(df, df_abbr, on='state', how='left')
print(df_merged)

#instead
df['abbr_state']=df['state'].map(abbr_dict)
print(df)

#4 - change the value of condition to number of hours left for all the records .

def condition_apply(condition):
    match=re.match(r"(\d+)\s+(day|days|hour|hours)",condition)
    if match:
        value=(int(match.group(1)))
        unit=match.group(2)
        if "day" in unit:
            return 24*value
        else:
            return value
    return None
df['condition_hours']=df['condition'].apply(condition_apply)
print(df[['condition','condition_hours']])

#5 - create bins of mileage and separate them into different groups based on the values . < cut function >
bins=[0,10000,50000,100000,200000,300000]
labels=['0-10k','10k-50k','50k-100k','100k-200k','200k-300k']

df['milage_group']=pd.cut(df['mileage'],bins=bins,labels=labels,right=False)
print(df[['mileage','milage_group']])

#6 - Does each vehicle have a unique vin ( vehicle identification number ) ?

is_unique=df['vin'].is_unique
print(is_unique)

duplicates=df['vin'].duplicated().sum()
print(duplicates)

#7 - Which is the most  and least selling colour of the car  in the dataset ?

val_counts=df['color'].value_counts()
print(val_counts)
max=val_counts.idxmax()
max_count=val_counts.max()
print(max,max_count)
min=val_counts.idxmin()
min_count=val_counts.min()
print(min,min_count)

#8 - Does the number of car purchased increase year on year ?

cars_per_year=df.groupby('year').size()
print(cars_per_year)

#9 Which state observed the highest number of cars sold ?

# Group by state and count number of cars
cars_per_state = df.groupby("state")["vin"].count()

print("Cars sold per state:\n", cars_per_state)

# Get the top state
top_state = cars_per_state.idxmax()
top_count = cars_per_state.max()
print(f"\nHighest cars sold in: {top_state} ({top_count} cars)")

#10 - Which brand of the car has the highest mileage ?

milage_group=df.groupby('brand')['mileage'].max().sort_values(ascending=False)

print("Maximum mileage per brand:\n", milage_group)

# Get the top brand
top_brand = milage_group.idxmax()
top_mileage = milage_group.max()
print(f"\nBrand with highest mileage: {top_brand} ({top_mileage} miles)")

#11- Convert the Date column into proper datetime format and find the earliest and latest sale date in the dataset.
df['Date']=pd.to_datetime(df['Date'], format='%d-%m-%Y')

min=df['Date'].min()
max=df['Date'].max()
print(min,max)

#12 - Group the data by brand and calculate the average price of cars for each brand.

brand_avg=df.groupby('brand')['price'].mean().sort_values(ascending=False)
print(brand_avg)

#13 - Find the top 5 most expensive cars in the dataset (brand, model, year, price).




