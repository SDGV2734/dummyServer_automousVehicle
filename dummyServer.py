import asyncio
import websockets
import random
import json
import cv2
import base64

async def car_dashboard_server(websocket):
    speed = 0
    battery_level = 100
    latitude, longitude = 37.7749, -122.4194  # Starting GPS coordinates (San Francisco)

    # Open video file or webcam
    video_capture = cv2.VideoCapture(r"/Users/yontenkinleytenzin/Desktop/dummyServer_automousVehicle/cameraFeed.mp4")


    while True:
        # Simulate speed (accelerating and decelerating)
        if random.choice([True, False]):
            speed = min(120, speed + random.uniform(0.5, 2.0))
        else:
            speed = max(0, speed - random.uniform(0.5, 2.0))

        # Simulate temperature
        temperature = random.uniform(-10, 50)  # Example range in Fahrenheit

        # Simulate GPS coordinates
        latitude += random.uniform(-0.0001, 0.0001)
        longitude += random.uniform(-0.0001, 0.0001)

        # Simulate battery level
        battery_level = max(0, battery_level - random.uniform(0.01, 0.1))

        # Capture video frame
        ret, frame = video_capture.read()
        if ret:
            # Encode frame as base64 to send over WebSocket
            _, buffer = cv2.imencode('.jpg', frame)
            frame_data = base64.b64encode(buffer).decode('utf-8')
        else:
            frame_data = None

        # Create data packet
        data = {
            "speed": round(speed, 2),
            "temperature": round(temperature, 2),
            "gps": {"latitude": round(latitude, 6), "longitude": round(longitude, 6)},
            "battery_level": round(battery_level, 2),
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
