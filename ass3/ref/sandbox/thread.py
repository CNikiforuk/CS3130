import threading

def worker(text):
    print('Worker' + t.getName() + ' '+text)
    return

threads = []
x="hello"
for i in range(5):
    t = threading.Thread(target=worker, args=(x,))
    threads.append(t)
    t.start()
