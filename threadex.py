import threading
import queue
import time
import random
import cv2
import numpy as np

class NumberProducer(threading.Thread):
    def __init__(self, producer_id, data_queue):
        super().__init__()
        self.producer_id = producer_id
        self.data_queue = data_queue
        self.running = True

    def run(self):
        num = 1
        while self.running:
            value = (self.producer_id, num)
            self.data_queue.put(value)
            print(f"Producer {self.producer_id} produced: {num}")
            num += 1
            time.sleep(random.uniform(0.3, 1.0))  # Simulate random delay

    def stop(self):
        self.running = False

# Shared queue
data_queue = queue.Queue()

# Create multiple producers
producers = [NumberProducer(i, data_queue) for i in range(3)]

# Start all producers
for producer in producers:
    producer.start()

# Consumer runs in the main thread
while True:
    if not data_queue.empty():
        value = data_queue.get()
        if value is None:  # Stop signal
            break
        
        producer_id, num = value
        print(f"Displaying from Producer {producer_id}: {num}")

        # Create an OpenCV image to display
        img = np.zeros((300, 500, 3), dtype=np.uint8)
        text = f"Producer {producer_id} -> {num}"
        cv2.putText(img, text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Queue Consumer", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

# Stop all producers
for producer in producers:
    producer.stop()

# Send stop signals to producers
for _ in producers:
    data_queue.put(None)

# Wait for all threads to finish
for producer in producers:
    producer.join()

cv2.destroyAllWindows()
print("Processing complete.")
