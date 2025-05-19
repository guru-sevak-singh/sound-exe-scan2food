'''
this exe pla the sound when order is received and it play the sound by reading the text
using text to speach library
name pyttsx3
and this code of exe is not used for the real production
because of some compatibility issues
and the code which run in all the system is in main.py file

'''

import asyncio
import websockets
import json
import pyttsx3

import os
from text_to_speech import save

from datetime import datetime

def playSound(Screen, Seat):
    alpha = Seat[0]
    seat_no = Seat.replace(alpha, '')

    text = f"Scan to Food Recieved New Order, From Seat Number, {alpha} , {seat_no} , in , {Screen}"

    engine.say(text)
    engine.runAndWait()

with open('theatre-id.txt') as file:
    theatre_id = file.read()

print(theatre_id)
WS_URL = "wss://www.scan2food.com/ws/all-seat-datasocket/"

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)

engine.setProperty('volume', 1.0)

engine.setProperty('rate', 150)  # Adjust speech rate if needed

# with open("pending_seats.json", 'w') as file:
#     json_data = {
#         "all_seats": [],
#         "data": {}
#     }
#     json.dump(json_data, file, indent=4)

def add_seat(seat_name):
    current_time = datetime.now().timestamp()  # Get current time in seconds

    with open('pending_seats.json') as file:
        all_seats = json.load(file)

    pending_orders = len(all_seats['all_seats'])

    if seat_name == "":
        return pending_orders
    
    all_seats['all_seats'].append(seat_name)
    all_seats['data'][seat_name] = current_time

    with open('pending_seats.json', 'w') as file:
        json.dump(all_seats, file, indent=4)
    
    return pending_orders


def remove_seat(seat_name):
    with open('pending_seats.json') as file:
        all_seats = json.load(file)
    try:
        all_seats['all_seats'].remove(seat_name)
        del all_seats['data'][seat_name]

        with open('pending_seats.json', 'w') as file:
            json.dump(all_seats, file, indent=4)
    except:
        pass

def get_time_difference():
    FILE_PATH = "pending_seats.json"
    with open(FILE_PATH, "r") as file:
        data = json.load(file)
        first_seat = data["all_seats"][0]
        stored_time = data["data"][first_seat]
    
    current_time = datetime.now().timestamp()
    time_diff_minutes = (current_time - stored_time) / 60  # Convert seconds to minutes
    return round(time_diff_minutes, 2)

async def listen_orders():
    async with websockets.connect(WS_URL) as websocket:
        print("Connected to WebSocket server...")
        n = 0
        while True:
            try:
                message = await websocket.recv()
                print("Message received:", message)
                
                # Assuming the message is in JSON format with seat_no
                data = json.loads(message)
                data = data['updated_table_data']
                data = json.loads(data)

                if str(data['theatre_id']) == theatre_id:
                    print('\ntheatre id and selected id are same.....!\n')
                    test_message = data["message"]
                    
                    if "New Order Come From" in test_message:    
                        # Generate and play the speech
                        seat_data = data['seat_name']
                        pending_orders = add_seat(seat_data)

                        seat_data = seat_data.split("|")
                        screen = seat_data[0]
                        seat = seat_data[1]
                        playSound(screen, seat)

                        if pending_orders != 0:
                            time_gap = get_time_difference()
                            if time_gap > 5:
                                another_text = f"There Are {pending_orders} are still pending Which Have Been Orderd More then 5 Minutes"
                                engine.say(another_text)
                                engine.runAndWait()

                    elif "Order Successfylly Deliver" in test_message:
                        seat = data['seat_name']
                        remove_seat(seat)
                
                else:
                    pending_orders = add_seat("")
                    if pending_orders != 0:
                        time_gap = get_time_difference()
                        if "New Order Come From" in test_message:
                            if time_gap > 5:
                                another_text = f"There Are {pending_orders} are still pending Which Have Been Orderd More then 5 Minutes"
                                engine.say(another_text)
                                engine.runAndWait()


                
            except Exception as e:
                n += 1
                print("Error:", e)
                await asyncio.sleep(2)  # Retry after delay if error occurs
                if n == 3:
                    break

# Run the WebSocket listener
while True:
    asyncio.run(listen_orders())