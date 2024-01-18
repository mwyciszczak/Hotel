from flask import Flask, render_template, request
from datetime import datetime
from sqlalchemy import and_
from models import db, City, Room, Reservation, Restaurant, Table_Reservation, Table


app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
     if request.method == 'POST':
        location = request.form['location']
        check_in_date = datetime.strptime(request.form['check-in'], '%Y-%m-%d').date()
        check_out_date = datetime.strptime(request.form['check-out'], '%Y-%m-%d').date()
        guests = int(request.form['guests'])
        city = City.query.filter_by(name=location).first()
     
        available_rooms = Room.query.filter(
                Room.hotel.has(city_id=city.id),
                Room.capacity >= guests,
                ~Room.reservations.any(and_(
                Reservation.check_in_date < check_out_date,
                Reservation.check_out_date > check_in_date
                ))
            ).all()

        return render_template('result_index.html', 
                               rooms=available_rooms, 
                               data=[check_in_date, check_out_date, guests])
     
     else:
        cities = db.session.execute(db.select(City))
        cities = [x[0].name for x in cities]
        return render_template('index.html', cities=cities)


@app.route('/rezerwuj', methods=['POST'])
def dodaj_rezerwacje():
    selected_room_id = request.form.get('selected_room')
    check_in_date = datetime.strptime(request.form['check-in'], '%Y-%m-%d').date()
    check_out_date = datetime.strptime(request.form['check-out'], '%Y-%m-%d').date()
    guests = request.form.get('guests')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone_number = request.form.get('phone_number')

    room = Room.query.get(selected_room_id)

    reservation = Reservation(
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        number_of_people=guests,
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        room=room
    )

    db.session.add(reservation)
    db.session.commit()

    return render_template('udana.html')


@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


@app.route('/rezerwacja', methods=['GET', 'POST'])
def rezerwacja():
    if request.method == 'POST':
        nr = request.form['telefon']
        reservations = Reservation.query.filter_by(phone_number=nr).all()
        table_reservations = Table_Reservation.query.filter_by(phone_number=nr).all()
        return render_template('rezerwacja.html', reservations=reservations, tables=table_reservations)

    else:
        return render_template('rezerwacja.html')


@app.route('/restauracja', methods=['GET', 'POST'])
def restauracja():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant')
        phone_number = request.form.get('telefon')
        name = request.form.get('Imie')
        reservation_date = datetime.strptime(request.form.get('data_rezerwacji'), '%Y-%m-%d').date()
        reservation_time = datetime.strptime(request.form.get('godz_rezerwacji'), '%H:%M').time()
        guests = int(request.form.get('guests'))

        restaurant_id = Restaurant.query.filter_by(name=restaurant_name).first()
        restaurant_id = restaurant_id.id
        available_tables = Table.query.filter_by(restaurant_id=restaurant_id).all()

        return render_template('result_restauracja.html', tables=available_tables, data=[
            phone_number, name, reservation_date, reservation_time, guests
        ])
    
    else:
        restaurants = Restaurant.query.all()
        return render_template('restauracja.html', restaurants=restaurants)


@app.route('/rezerwuj_stolik', methods=['POST'])
def dodaj_stolik():
    phone_number = request.form.get('telefon')
    first_name = request.form.get('Imie')
    number_of_people = request.form.get('guests')
    date = datetime.strptime(request.form['data_rezerwacji'], '%Y-%m-%d').date()
    time = datetime.strptime(request.form['godz_rezerwacji'], '%H:%M:%S').time()
    table_id = request.form.get('selected_table')
    
    table_reseravtion = Table_Reservation(
        phone_number=phone_number,
        first_name=first_name,
        number_of_people=number_of_people,
        date=date,
        time=time,
        table_id=table_id
    )
    db.session.add(table_reseravtion)
    db.session.commit()


    return render_template('udana.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
