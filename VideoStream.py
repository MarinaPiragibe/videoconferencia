from vidstream import CameraClient
from vidstream import StreamingServer

import threading
import time

time.sleep(3)
receiving = StreamingServer('192.168.0.71', 7777)
sending = CameraClient('192.168.15.10', 7777)

t1 = threading.Thread(target=receiving.start_server)
t1.start()

time.sleep(7)

t2 = threading.Thread(target=sending.start_stream)
t2.start()


while input("") != "q":
    continue

receiving.stop_server()
sending.stop_stream()

