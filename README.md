Reaktor kesätyö ennakkotehtävä
==============================

Sovellus, jonka avulla on helppo tutkia hiilidioksidipäästöjen kehitystä viime vuosina. Toteutetaan sekä oma frontend, että API jotta myöhemmin on helppoa tehdä muita frontendejä.

Toiminnallisuus
---------------

- tietokoneella ja mobiililla toimiva selainfrontend
- automaattisesti tuoreen datan hakeminen
- mahdollisuus tutkia päästöjä eri tavoin:
  - maakohtaisesti
  - per capita
- muita mahdollisuuksia:
  - halutulle ajanjaksolle
  - vertailla maiden välillä

Toteutus
--------

Backend pythonilla, käyttäen flaskia. Frontend HTML-sivu, joka lataa AJAX:lla tiedot.

Ajaminen
--------

Ajaaksesi sovelluksen: `pipenv install && pipenv run gunicorn 'app:create_app()'`.
