import sys
import zerorpc
import windows.main_window as main_window
from PyQt5.QtWidgets import QApplication, QStyleFactory
import gevent
import threading

client = None
group = gevent.pool.Group()

def connect():
    global client

    print("Connecting to tcp://127.0.0.1:8899")
    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:8899")
    try:
        client._zerorpc_ping()
    except Exception as ex:
        print("Failed to connect because " + str(ex))
    print("Connected!")

APP_RUNNING = True

def event_loop(app):
    timer = 0
    while APP_RUNNING:
        app.processEvents()
        timer = timer + 1
        if timer % 800 == 0:
            timer = 0
            gevent.sleep()

def close():
    global APP_RUNNING
    APP_RUNNING = False

def main():
    global group
    print("Starting MF")
    connect()

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    window = main_window.MainWindow(client, group, close)
    
    window.show()
    group.spawn(event_loop, app)
    group.join()


if __name__ == "__main__":
    main()
