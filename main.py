import asyncio
import websockets
import json

import os

from datetime import datetime
from play_audio import *


with open('theatre-id.txt') as file:
    theatre_id = file.read()

WS_URL = "wss://www.scan2food.com/ws/all-seat-datasocket/"

# download the audio
download_audios()

# Initialize the text-to-speech engine

with open("pending_seats.json", 'w') as file:
    json_data = {
        "all_seats": [],
        "data": {}
    }
    json.dump(json_data, file, indent=4)

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
                        order_received()

                        if pending_orders != 0:
                            time_gap = get_time_difference()
                            if time_gap > 5:
                                pending_order()

                    elif "Order Successfylly Deliver" in test_message:
                        seat = data['seat_name']
                        remove_seat(seat)
                
                else:
                    pending_orders = add_seat("")
                    if pending_orders != 0:
                        time_gap = get_time_difference()
                        if "New Order Come From" in test_message:
                            if time_gap > 5:
                                pending_order()


                
            except Exception as e:
                n += 1
                print("Error:", e)
                await asyncio.sleep(2)  # Retry after delay if error occurs
                if n == 3:
                    break

# Run the WebSocket listener
while True:
    asyncio.run(listen_orders())