# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import database

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        # TODO
        return "index page"

    @app.route('/api/all')
    def request_all_countries():
        """ get information about all countries """
        year_start = int(request.args.get('start', 0))
        year_end = int(request.args.get('end', 0))
        per_capita = bool(request.args.get('percapita', None))

        data = database.get_all_countries_data(year_start, year_end, per_capita)
        return jsonify(data)

    @app.route('/api/country/<country_code>')
    def request_one_country(country_code):
        """ get information about a single country """
        year_start = int(request.args.get('start', 0))
        year_end = int(request.args.get('end', 0))
        per_capita = bool(request.args.get('percapita', None))

        data = database.get_one_country_data(country_code, year_start, year_end, per_capita)
        return jsonify(data)

    @app.route('/api/meta/all')
    def request_country_metadata():
        """ get metadata of all countries """
        metadata = database.get_countries_info()

        response_data = {code: {'name': name, 'region': region, 'income': income, 'notes': notes}
                         for name,code,region,income,notes in metadata}
        return jsonify(response_data)

    return app
