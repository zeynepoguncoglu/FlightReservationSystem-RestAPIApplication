# Sample REST API Application for Flight Reservation System #

from flask import Flask, jsonify, request, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import random
import datetime
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

# Database tables creation - Start #

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(3), nullable=False)
    destination = db.Column(db.String(3), nullable=False)
    flightNumber = db.Column(db.String(6), nullable=False)
    flightDate = db.Column(db.String(10))
    departureTime = db.Column(db.String(5))
    arrivalTime = db.Column(db.String(5))
    lowestAvailableClass = db.Column(db.String(1))
    price = db.Column(db.Float)

    def __init__(self, origin, destination, flightNumber, flightDate, departureTime,
                arrivalTime, lowestAvailableClass, price):
        self.origin = origin
        self.destination = destination
        self.flightNumber = flightNumber
        self.flightDate = flightDate
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
        self.lowestAvailableClass = lowestAvailableClass
        self.price = price

    def __repr__(self):
        return f"{self.origin} - {self.destination} - {self.flightNumber} - {self.flightDate} " \
               f" - {self.departureTime} - {self.arrivalTime} - {self.lowestAvailableClass} - {self.price}"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eTicketNumber = db.Column(db.String(13), nullable=False)
    pnrNumber = db.Column(db.String(13), nullable=False)
    origin = db.Column(db.String(3), nullable=False)
    destination = db.Column(db.String(3), nullable=False)
    flightNumber = db.Column(db.String(6), nullable=False)
    flightDate = db.Column(db.String(10))
    reservationClass = db.Column(db.String(1))
    price = db.Column(db.Float)
    name = db.Column(db.String(13), nullable=False)
    surname = db.Column(db.String(13), nullable=False)
    birthDate = db.Column(db.String(10))
    creationTime = db.Column(db.DateTime(), index=True, default=datetime.datetime.now())

    def __init__(self, eTicketNumber, pnrNumber, origin, destination, flightNumber, flightDate, reservationClass,
                price, name, surname, birthDate):
        self.eTicketNumber = eTicketNumber
        self.pnrNumber = pnrNumber
        self.origin = origin
        self.destination = destination
        self.flightNumber = flightNumber
        self.flightDate = flightDate
        self.reservationClass = reservationClass
        self.price = price
        self.name = name
        self.surname = surname
        self.birthDate = birthDate

    def __repr__(self):
        return f"{self.eTicketNumber} - {self.pnrNumber} - {self.origin} - {self.destination} - {self.flightNumber} - " \
               f"{self.flightDate} - {self.reservationClass} - {self.price} - {self.name} - {self.surname} " \
               f"- {self.birthDate}  "

class TravelPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
    pnrNumber = db.Column(db.String(13), nullable=False)

    def __init__(self, name, data, pnrNumber):
        self.name = name
        self.data = data
        self.pnrNumber = pnrNumber

    def __repr__(self):
        return f"{self.name} - {self.data} - {self.pnrNumber} "

db.create_all()

# Database tables creation - End #

# REST API Endpoints creation - Start #

@app.route('/', methods=['GET'])
def index():
    return "Hello!"

@app.route('/flights', methods=['GET'])
def get_flights():
    time.sleep(10)
    flights = Flight.query.all()
    output = []
    for flight in flights :
        flight_data = {
                        'id': flight.id,
                        'origin': flight.origin,
                        'destination': flight.destination,
                        'flightNumber': flight.flightNumber,
                        'flightDate': flight.flightDate,
                        'departureTime': flight.departureTime,
                        'arrivalTime': flight.arrivalTime,
                        'lowestAvailableClass' : flight.lowestAvailableClass,
                        'price': flight.price
                        }
        output.append(flight_data)
    return {'flights': output}

@app.route('/flights/<origin>/<destination>', methods=['GET'])
def get_flight(origin,destination):
    time.sleep(3)
    flight = Flight.query.filter((Flight.origin==origin) & (Flight.destination==destination)).all()
    output = []
    for flight in flight :
        flight_data = {
                       'id': flight.id,
                       'origin': flight.origin,
                       'destination': flight.destination,
                       'flightNumber': flight.flightNumber,
                       'flightDate': flight.flightDate,
                       'departureTime': flight.departureTime,
                       'arrivalTime': flight.arrivalTime,
                       'lowestAvailableClass' : flight.lowestAvailableClass,
                       'price': flight.price
                       }
        output.append(flight_data)
    return {'flights': output}

@app.route('/flights/<origin>/<destination>/<flightNumber>/<flightDate>', methods=['GET', 'POST', 'PUT'])
def manage_flight(origin, destination, flightNumber,flightDate):

    flight = Flight.query.filter((Flight.origin == origin) & (Flight.destination == destination) &
                                 (Flight.flightNumber == flightNumber) & (Flight.flightDate == flightDate)).first()

    if request.method == 'GET':
        return {
                'origin': flight.origin,
                'destination': flight.destination,
                'flightNumber': flight.flightNumber,
                'flightDate': flight.flightDate
                }

    if request.method == 'POST':
        time.sleep(4)
        e_ticket_num = "235" + str(random.randrange(1000000000, 9999999999))
        pnr_num = "ABC" + str(random.randrange(100, 999)) + str(flight.lowestAvailableClass) + str(flightNumber)
        name = request.form['name']
        surname = request.form['surname']
        birthDate = request.form['birthDate']
        Reservation.creationTime = datetime.datetime.now()
        print(Reservation.creationTime)
        booking = Reservation(e_ticket_num, pnr_num, origin, destination, flightNumber, flightDate,
                              flight.lowestAvailableClass,
                              flight.price, name, surname, birthDate)
        db.session.add(booking)
        db.session.commit()
        return {
                'eTicketNumber': e_ticket_num,
                'pnrNumber': pnr_num,
                'origin': flight.origin,
                'destination': flight.destination,
                'flightNumber': flight.flightNumber,
                'flightDate': flight.flightDate,
                'reservationClass': flight.lowestAvailableClass,
                'price' : flight.price
                }

    if request.method == 'PUT':
        flight.lowestAvailableClass = request.form['lowestAvailableClass']
        flight.price = request.form['price']
        db.session.commit()

        return {
                'id': flight.id,
                'origin': flight.origin,
                'destination': flight.destination,
                'flightNumber': flight.flightNumber,
                'flightDate': flight.flightDate,
                'departureTime': flight.departureTime,
                'arrivalTime': flight.arrivalTime,
                'lowestAvailableClass' : flight.lowestAvailableClass,
                'price': flight.price
                }

@app.route('/<pnrNumber>', methods=['GET', 'DELETE', 'POST'])
def get_reservation(pnrNumber):

    reservation = Reservation.query.filter((Reservation.pnrNumber==pnrNumber)).first()

    if reservation is None:
        return {"error": "PNR Number is not found."}

    if request.method == 'GET':
        reservation_data = {
                            'eTicketNumber': reservation.eTicketNumber,
                            'pnrNumber': reservation.pnrNumber,
                            'origin': reservation.origin,
                            'destination': reservation.destination,
                            'flightNumber': reservation.flightNumber,
                            'flightDate': reservation.flightDate,
                            'reservationClass' : reservation.reservationClass,
                            'reservationPrice' : reservation.price,
                            'reservationCreationTime': reservation.creationTime,
                            'name' : reservation.name,
                            'surname' : reservation.surname,
                            'birthDate': reservation.birthDate
                           }
        return {'reservationDetails': reservation_data}

    if request.method == 'POST':
        time.sleep(5)
        file = request.files['inputFile']
        name = file.filename
        data = file.read()
        newFile = TravelPass(name, data, pnrNumber)
        db.session.add(newFile)
        db.session.commit()
        return file.filename

    if request.method == 'DELETE':
        time.sleep(8)
        db.session.delete(reservation)
        db.session.commit()
        return "Your reservation with PNR number " + (str(reservation.pnrNumber)) + " has been successfully cancelled."

@app.route('/<pnrNumber>/download', methods=['GET'])
def get_travelPass(pnrNumber):
    time.sleep(9)
    travelPass = TravelPass.query.with_entities(TravelPass.data).filter(TravelPass.pnrNumber == pnrNumber).first()
    travelPassDetail = travelPass[0]
    downloadName = "TravelPass_" + str(pnrNumber) + ".pdf"
    return send_file(BytesIO(travelPassDetail), download_name=downloadName, as_attachment=True)

# REST API Endpoints creation - End #

if __name__ == "__main__":
    app.run(debug=True)
