import os
from flask import Flask, request, jsonify
import requests
import config


app = Flask(__name__)


@app.route('/railbutler', methods=['POST'])
def find_action():
    json_data = request.get_json()
    if json_data['result']['action'] == 'fetch_pnr_status':
        return fetch_pnr_status(json_data['result']['resolvedQuery'])


def fetch_pnr_status(PNR):
    PNR = PNR.replace('-', '')
    PNR = PNR.replace(' ', '')
    URL = 'https://api.railwayapi.com/v2/pnr-status/pnr/' + PNR + \
        '/apikey/' + config.RAILWAY_API_KEY

    json_response = requests.get(URL, verify=True)
    json_data = json_response.json()

    if json_data['response_code'] == '200':
        speech = ""
        idx = 1
        for passenger_detail in json_data['passengers']:
            speech += 'Status for passenger ' + str(idx) + ' is '
            speech += passenger_detail['booking_status']
            speech += '.\n'
            idx += 1

        answer = {
            'speech': speech,
            'displayText': speech,
            'source': 'fetch_pnr_status'
        }
        return jsonify(answer)

    else:
        speech = 'This PNR is invalid. Please try again.'
        answer = {
            'speech': speech,
            'displayText': speech,
            'source': 'fetch_pnr_status'
        }
        return jsonify(answer)


port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
