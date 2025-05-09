#test the isalive function in threading
import threading
import time

def task(name, duration):
    print(f'Thread {name} starting')
    time.sleep(duration)
    print(f'Thread {name} finished')

# Create two threads
thread1 = threading.Thread(target=task, args=('A', 2))
thread2 = threading.Thread(target=task, args=('B', 4))

# Start the threads
thread1.start()
thread2.start()

# Check if threads are alive
while thread1.is_alive() or thread2.is_alive():
    print(f'Thread A alive: {thread1.is_alive()}, Thread B alive: {thread2.is_alive()}')
    time.sleep(1)

print('Both threads have completed.')
