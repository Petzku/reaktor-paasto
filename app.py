# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template
import database
import handle_csv
import data_fetch
import datetime


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/api/all')
    def request_all_countries():
        """ get information about all countries """
        update_data()

        year_start = int(request.args.get('start', 0) or 0)
        year_end = int(request.args.get('end', 0) or 0)
        per_capita = bool(request.args.get('percapita', None))

        data = database.get_all_countries_data(year_start, year_end, per_capita)
        return jsonify(data)

    @app.route('/api/country/<country_code>')
    def request_one_country(country_code):
        """ get information about a single country """
        update_data()

        year_start = int(request.args.get('start', 0) or 0)
        year_end = int(request.args.get('end', 0) or 0)
        per_capita = bool(request.args.get('percapita', None))

        data = database.get_one_country_data(country_code, year_start, year_end, per_capita)
        return jsonify(data)

    @app.route('/api/meta/all')
    def request_country_metadata():
        """ get metadata of all countries """
        update_data()

        metadata = database.get_countries_info()

        response_data = {code: {'name': name, 'region': region, 'income': income, 'notes': notes}
                         for name,code,region,income,notes in metadata}
        return jsonify(response_data)

    return app

def update_data():
    """ checks to see if data needs updating, and update if so
    currently updates daily, could maybe be less frequent """

    last_update_str, = database.get_database_updated()  # returns a 1-tuple, unpack it
    last_update = datetime.date.fromisoformat(last_update_str)
    if last_update < datetime.date.today():
        popfile, co2file, countryfile = data_fetch.get_dataset_files()

        new_data = handle_csv.load_data(popfile, co2file, countryfile)
        popfile.close()
        co2file.close()
        countryfile.close()

        database.update_database(new_data)
