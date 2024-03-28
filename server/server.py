from flask import Flask, request, jsonify
from flask_cors import CORS
import main

app = Flask(__name__)

CORS(app)

@app.route('/hotels', methods=['POST'])
def hotel_scrap():
    if request.json != {}:
        print(request.json)
        hotel_info = request.json
        # print(hotel_info['location'])
        hotels = main.scrape_hotel_prices(hotel_info['location'], str(hotel_info['checkInDate']), str(hotel_info['checkOutDate']))
    return jsonify({'hotels' : "hello"})

if __name__ == '__main__':
   app.run(debug=True)