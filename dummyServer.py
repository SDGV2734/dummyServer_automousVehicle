import asyncio
import websockets
import random
import json
import cv2
import base64
import time

async def car_dashboard_server(websocket):
    speed = 0
    battery_level = 100
    latitude, longitude = 37.7749, -122.4194  # Starting GPS coordinates (San Francisco)

    # Initial temperature within the range -10 to 30
    temperature = random.randint(-10, 30)

    # Track the last time temperature and battery were updated
    last_temp_update_time = time.time()
    last_battery_update_time = time.time()

    # Open video file or webcam
    video_capture = cv2.VideoCapture(r"cameraFeed.mp4")  # Use 0 for webcam or replace with video file path

    if not video_capture.isOpened():
        print("Error: Unable to open video file or webcam.")
        return

    while True:
        # Simulate speed (accelerating and decelerating)
        if speed < 120:  # Gradually increase speed
            speed += 1
        else:  # Gradually decrease speed but never drop below 10
            speed = max(10, speed - 1)

        # Check if it's time to update the temperature
        current_time = time.time()
        if current_time - last_temp_update_time >= random.uniform(180, 300):  
            # Change temperature by 3 or 5 degrees, within the range [-10, 30]
            temp_change = random.choice([3, 5])
            new_temp = temperature + temp_change if random.choice([True, False]) else temperature - temp_change

            # Keep the temperature within the desired range
            temperature = min(max(new_temp, -10), 30)
            
            # Update the last temperature update time
            last_temp_update_time = current_time

        # Check if it's time to update the battery level
        if current_time - last_battery_update_time >= 30:  # Decrease battery level every 30 seconds
            battery_level = max(0, battery_level - 1)  # Ensure it doesn't go below 0
            last_battery_update_time = current_time

        # Simulate GPS coordinates
        latitude += random.uniform(-0.0001, 0.0001)
        longitude += random.uniform(-0.0001, 0.0001)

        # Capture video frame
        ret, frame = video_capture.read()
        if ret:
            # Resize frame to reduce size if necessary
            frame = cv2.resize(frame, (640, 480))
            # Encode frame as base64 to send over WebSocket
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
        else:
            # Restart video if end of video is reached
            print("Restarting video...")
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_data = None

        # Create data packet
        data = {
            "speed": round(speed, 2),
            "temperature": temperature,  # Temperature as a whole number (integer)
            "gps": {"latitude": round(latitude, 6), "longitude": round(longitude, 6)},
            "battery_level": battery_level,  # Battery level as an integer
            "video_frame": frame_data,
        }

        # Send data packet as JSON
        await websocket.send(json.dumps(data))

        # Wait for a short period to simulate real-time updates
        await asyncio.sleep(0.1)

async def main():
    async with websockets.serve(car_dashboard_server, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
