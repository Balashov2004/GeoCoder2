import geopandas as gpd
import sqlite3

# Чтение данных из файла GeoJSON
gdf = gpd.read_file("export.geojson")

# Подключаемся к базе данных (если она существует) или создаем новую
conn = sqlite3.connect('addresses.db')
cursor = conn.cursor()

# Создаем таблицу для адресов
cursor.execute('''CREATE TABLE IF NOT EXISTS addresses
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  street TEXT,
                  housenumber TEXT,
                  latitude REAL,
                  longitude REAL)''')

# Вставляем данные в таблицу
for index, row in gdf.iterrows():
    street = row['addr:street']
    housenumber = row['addr:housenumber']
    try:
        latitude = row.geometry.y
        longitude = row.geometry.x
    except AttributeError:
        latitude = row.geometry.xy[1]  # Исправлено
        longitude = row.geometry.xy[0]  # Исправлено

    cursor.execute('''INSERT INTO addresses (street, housenumber, latitude, longitude)
                          VALUES (?, ?, ?, ?)''', (street, housenumber, latitude, longitude))

# Сохраняем изменения и закрываем соединение с базой данных
conn.commit()
conn.close()

print("База данных успешно создана и заполнена.")
