from pathlib import Path
from threading import Thread
from flask import Flask, render_template
from mqtt.jwt import authenticate
from subscriber import subscriber

app = Flask(__name__, template_folder='./templates')

subscriber_instance = None
def make_subscriber():
     global subscriber_instance 
     subscriber_instance = subscriber()

subscriber_thread = Thread(target=make_subscriber)
subscriber_thread.start()

@app.route('/', methods=['GET'])
def get_dashboard():
    if subscriber_instance is None:
         return render_template('dashboard.html', weather_data=None, traffic_data=None, traffic_offense_data=None)
     
    #subscribe code
    payload_weather = subscriber_instance.process_weather_forecast()
    payload_traffic = subscriber_instance.process_collision()
    payload_traffic_offense = subscriber_instance.process_traffic_offense()


    if (payload_weather != None and payload_traffic != None):
        if ('Detection' in payload_traffic and 'Conditions' in payload_weather):
            return render_template('dashboard.html', weather_data=payload_weather, traffic_data=payload_traffic, traffic_offense_data=payload_traffic_offense)
    return render_template('dashboard.html', weather_data=None, traffic_data=None, traffic_offense_data=None)

def is_file_present(file_name):
    file_path = Path(file_name)
    return file_path.is_file()

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        # Run the simulation in a separate thread
        if (is_file_present('key.pem')):
            from simulation import TrafficOffence

            simulation_thread = Thread(target=TrafficOffence.main)
            simulation_thread.start()
        # Run the Flask app
        app.run(debug=False)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt appropriately
        simulation_thread.join()
        subscriber_thread.join()

