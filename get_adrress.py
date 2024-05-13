import sqlite3

def get_address(street, housenumber):
    conn = sqlite3.connect('addresses.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT street || ', ' || housenumber AS full_address, latitude, longitude 
                      FROM addresses 
                      WHERE street LIKE ? AND housenumber = ?''', ('%' + street + '%', housenumber))
    result = cursor.fetchone()

    conn.close()

    if result:
        full_address, latitude, longitude = result
        return f"Полный адрес: {full_address}, Широта: {latitude}, Долгота: {longitude}"
    else:
        return "Адрес не найден в базе данных"
