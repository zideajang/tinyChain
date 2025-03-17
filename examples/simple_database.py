
from pydantic import BaseModel, Field
import sqlite3
import random

class FlightDetail(BaseModel):
    id: str = Field(title="flight id", description="航班 id")
    origin: str = Field(title="origin of flight", description="出发城市", examples=['沈阳'])
    destination: str = Field(title="destination of flight", description="到达城市", examples=['上海'])
    price: float = Field(title="price of flight", description="机票价格", examples=[700])
    date: str = Field(title="date of flight", description="航班日期", examples=['2025年03月16日'])

def create_table():
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id TEXT PRIMARY KEY,
            origin TEXT,
            destination TEXT,
            price REAL,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(flight: FlightDetail):
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (id, origin, destination, price, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (flight.id, flight.origin, flight.destination, flight.price, flight.date))
    conn.commit()
    conn.close()

def generate_fake_data():
    origins = ['沈阳', '北京', '上海', '广州', '深圳']
    destinations = ['北京', '上海', '广州', '深圳', '成都']
    dates = ['2025年03月' + str(i).zfill(2) + '日' for i in range(16, 26)]

    flights = []
    for i in range(10):
        origin = random.choice(origins)
        destination = random.choice(destinations)
        while origin == destination:  # 确保出发地和目的地不同
            destination = random.choice(destinations)
        flight = FlightDetail(
            id=f'FLT{i + 1:03}',
            origin=origin,
            destination=destination,
            price=random.uniform(500, 2000),
            date=random.choice(dates)
        )
        flights.append(flight)
    return flights

def read_data(flight_id: str):
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights WHERE id = ?', (flight_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return FlightDetail(id=row[0], origin=row[1], destination=row[2], price=row[3], date=row[4])
    return None

def update_data(flight: FlightDetail):
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE flights SET origin = ?, destination = ?, price = ?, date = ?
        WHERE id = ?
    ''', (flight.origin, flight.destination, flight.price, flight.date, flight.id))
    conn.commit()
    conn.close()

def delete_data(flight_id: str):
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM flights WHERE id = ?', (flight_id,))
    conn.commit()
    conn.close()




# class FlightDetail(BaseModel):
#     id:str = Field(title="flight id",description="航班 id")
#     origin:str = Field(title="origin of flight",description="出发城市",examples=['沈阳'])
#     destination:str = Field(title="destination of flight",description="到达城市",examples=['上海'])
#     price:float = Field(title="price of flight",description="机票价格",examples=[700])
#     date:str = Field(title="date of flight",description="航班日期",examples=['2025年03月16日'])
