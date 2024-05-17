import geopandas as gpd
import sqlite3

gdf = gpd.read_file("export.geojson")

conn = sqlite3.connect('addresses.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS addresses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  street TEXT,
                  housenumber TEXT,
                  latitude REAL,
                  longitude REAL)''')

for index, row in gdf.iterrows():
    street = row['addr:street']
    housenumber = row['addr:housenumber']
    try:
        latitude = row.geometry.y
        longitude = row.geometry.x
    except AttributeError:
        latitude = row.geometry.xy[1]
        longitude = row.geometry.xy[0]

    cursor.execute('''INSERT INTO addresses (street, housenumber, latitude, longitude)
                          VALUES (?, ?, ?, ?)''', (street, housenumber, latitude, longitude))

conn.commit()
conn.close()

print("База данных успешно создана и заполнена.")
