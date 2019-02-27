# -*- coding: utf-8 -*-
import csv

def read_data_csv(csvfile):
    data = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)
    return data

def read_metadata_csv(csvfile):
    metadata = []
    reader = csv.DictReader(csvfile)
    for row in reader:
        metadata.append(row)
    return metadata

def load_data(popfile, co2file, countryfile):
    popdata = {x['Country Code']: x for x in read_data_csv(popfile)}
    co2data = {x['Country Code']: x for x in read_data_csv(co2file)}
    countrydata = read_metadata_csv(countryfile)
    
    countries = {}
    for row in countrydata:
        code = row['Country Code']

        # first four columns don't have important data: country code & name, indicator name & code
        years = list(popdata[code].keys())[4:]  # both sets have same starting year

        data = {int(year): (float(co2data[code][year]) if co2data[code][year] else None,
                            int(popdata[code][year]) if popdata[code][year] else None)
                for year in years if year}  # each line ends in a comma, so the last field is empty
        
        entry = {
            "name": row['TableName'],
            "region": row['Region'],
            "income": row['IncomeGroup'],
            "notes": row['SpecialNotes'],
            "data": data
        }
            
        countries[code] = entry

    return countries
            


