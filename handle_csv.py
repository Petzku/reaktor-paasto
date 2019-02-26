# -*- coding: utf-8 -*-
import csv

def read_data_csv(csvfile):
    data = []
    # first four lines don't contain relevant data
    for i in range(4):
        csvfile.readline()
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

def load_data(data_pop_filename, data_co2_filename, meta_country_filename):
    with open(data_pop_filename) as popfile:
        popdata = {x['Country Code']: x for x in read_data_csv(popfile)}
    with open(data_co2_filename) as co2file:
        co2data = {x['Country Code']: x for x in read_data_csv(co2file)}

    # each row starts with '\ufeff' if encoding isn't set
    with open(meta_country_filename, encoding='utf-8-sig') as countryfile:
        countrydata = read_metadata_csv(countryfile)
    
    countries = {}
    for row in countrydata:
        code = row['Country Code']

        # first four rows don't have important data: country code & name, indicator name & code
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
            

