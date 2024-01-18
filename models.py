from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime, date

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hotels = db.relationship('Hotel', backref='city', lazy=True)


class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    rooms = db.relationship('Room', backref='hotel')
    restaurants = db.relationship('Restaurant', backref='hotel')


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    reservations = db.relationship('Reservation', backref='room')


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    number_of_people = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    tables = db.relationship('Table', backref='restaurant')


class Table(db.Model): # Nie nazywaj, nie nazywaj tabeli table, sql tego nie lubi 
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    table_reservations = db.relationship('Table_Reservation', backref='table')


class Table_Reservation(db.Model):
    __tablename__ = 'table_reservation'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String)
    first_name = db.Column(db.String)
    number_of_people = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    end_time = db.Column(db.Time) 
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'))

    def __init__(self, time, *args, **kwargs):
        super(Table_Reservation, self).__init__(*args, **kwargs)
        self.time = time
        self.end_time = (datetime.combine(date.min, time) + timedelta(hours=4)).time()