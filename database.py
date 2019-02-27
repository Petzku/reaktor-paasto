# -*- coding: utf-8 -*-
import sqlite3

DB_FILE = "data.db"

def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS country_data")
    cur.execute("DROP TABLE IF EXISTS country_meta")
    cur.execute("DROP TABLE IF EXISTS last_updated")
    
    cur.execute("CREATE TABLE country_data( \
                    code TEXT PRIMARY KEY,  \
                    year INTEGER NOT NULL,  \
                    co2 REAL,               \
                    population INTEGER )")
    cur.execute("CREATE TABLE country_meta( \
                    code TEXT PRIMARY KEY,  \
                    name TEXT NOT NULL,     \
                    region TEXT NOT NULL,   \
                    income TEXT NOT NULL,   \
                    notes TEXT )")
    cur.execute("CREATE TABLE last_updated( updated DATE )")
    cur.execute("INSERT INTO last_updated VALUES (date('now'))")

    conn.commit()
    conn.close()

def get_all_countries_data(time_start=None, time_end=None, per_capita=False):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    if per_capita:
        query = "SELECT code, year, co2/population AS co2_per_capita FROM country_data WHERE ? <= year AND year <= ?"
    else:
        query = "SELECT code, year, co2 FROM country_data WHERE ? <= year AND year <= ?"

    cur.execute(query, (time_start or 0, time_end or 999999))
    result = cur.fetchall()

    conn.close()
    return result

def get_one_country_data(country_code, time_start=None, time_end=None, per_capita=False):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    if per_capita:
        query = "SELECT code, year, co2/population AS co2_per_capita FROM country_data WHERE code = ? AND ? <= year AND year <= ?"
    else:
        query = "SELECT code, year, co2 FROM country_data WHERE code = ? AND ? <= year AND year <= ?"

    cur.execute(query, (country_code, time_start or 0, time_end or 999999))
    result = cur.fetchall()

    conn.close()
    return result

def get_countries_info():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT name, code, region, income, notes FROM country_meta")
    result = cur.fetchall()

    conn.close()
    return result

def update_database(csv_data):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Recreating the entire database is easiest way to update data
    # The whole dataset in csv form is under 400KB, so it shouldn't matter much
    cur.execute("DROP TABLE IF EXISTS country_data")
    cur.execute("DROP TABLE IF EXISTS country_meta")
    
    cur.execute("CREATE TABLE country_data( \
                    code TEXT NOT NULL,     \
                    year INTEGER NOT NULL,  \
                    co2 REAL,               \
                    population INTEGER )")
    cur.execute("CREATE TABLE country_meta( \
                    code TEXT PRIMARY KEY,  \
                    name TEXT NOT NULL,     \
                    region TEXT NOT NULL,   \
                    income TEXT NOT NULL,   \
                    notes TEXT )")

    for country_code in csv_data:
        row = csv_data[country_code]
        cur.execute("INSERT INTO country_meta VALUES (?,?,?,?,?)", (country_code, row['name'], row['region'], row['income'], row['notes']))
        for year in row['data']:
            co2, population = row['data'][year]
            cur.execute("INSERT INTO country_data VALUES (?,?,?,?)", (country_code, year, co2, population))

    cur.execute("UPDATE last_updated SET updated=date('now')")

    conn.commit()
    conn.close()


def get_database_updated():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT updated FROM last_updated")
    result = cur.fetchone()

    conn.close()
    return result
