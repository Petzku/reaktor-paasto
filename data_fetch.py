# -*- coding: utf-8 -*-
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import codecs

DATASET_CO2_URL = "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=csv"
DATASET_POP_URL = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv"

def get_dataset_files():
    """ fetches the .zip archives from each URL and unpacks the datasets and one country metadata file """
    co2_resp = urlopen(DATASET_CO2_URL)
    with ZipFile(BytesIO(co2_resp.read())) as zipfile:
        data_co2_filename = [x for x in zipfile.namelist() if x.startswith("API_EN")][0]
        data_co2_file = zipfile.open(co2_filename)
        for i in range(4):
            # first four lines are useless, and WILL break the CSV reader, so skip them
            data_co2_file.readline()
        # we need this iterdecode, because csv.DictReader breaks if not given a file object
        # however, this method of extracting the csv gives us a file in byte mode, which DictReader can't parse.
        data_co2_file = codecs.iterdecode(data_co2_file, 'utf-8')

        meta_country_filename = [x for x in zipfile.namelist() if x.startswith("Metadata_Country")]
        # this one is encoded in utf-8-sig for some reason, others seem to be utf-8
        meta_country_file = codecs.iterdecode(zipfile.open(meta_country_filename), 'utf-8-sig')

    pop_resp = urlopen(DATASET_POP_URL)
    with ZipFile(BytesIO(pop_resp.read())) as zipfile:
        data_pop_filename = [x for x in zipfile.namelist() if x.startswith("API_SP")][0]
        data_pop_file = zipfile.open(data_pop_filename)
        for i in range(4):
            # same first four line thing here
            data_pop_file.readline()
        data_pop_file = codecs.iterdecode(data_pop_file, 'utf-8')

    return data_pop_file, data_co2_file, meta_country_file
