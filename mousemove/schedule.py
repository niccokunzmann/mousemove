#!/usr/bin/python3

import socket
import select
import time
import subprocess
import sys
import traceback

PORT = 5083
ADDRESS = ('localhost', PORT)
print_to_stdout = False

def debug_file():
    f = open('server.out', 'a', encoding = 'utf8')
    if f.tell() == 0:
        f.write('\ufeff') # BOM
    return f

def debug(*args):
    if print_to_stdout:
        print(*args)
    with debug_file() as f:
        print(*args, file = f)

def serve():
    listener = socket.socket()
    try:
        listener.bind(ADDRESS)
    except socket.error:
        debug('Es wurde schon ein server gestartet.')
        return
    else:
        debug('Server wurde gestartet auf', ADDRESS)
    listener.listen(1)
    connections = []
    has_token = listener # ich bin an der reihe
    addrs = {}
    def connection_kaputt(connection):
        nonlocal has_token
        if has_token == connection:
            has_token = listener
        connections.remove(connection)
        debug('Verbindung verloren zu', addrs[connection])
    while 1:
        try:
            readers = select.select(connections + [listener], [], [])[0]
        except ValueError:
            for connection in connections[:]:
                if connection.fileno() < 0:
                    connections.remove(connection)
            continue
        for connection in readers:
            if connection == listener:
                sock, addr = listener.accept()
                sock.setblocking(0)
                addrs[sock] = addr
                debug('verbunden hat sich', addr[0], ':', addr[1])
                connections.insert(0, sock)
            else:
                try:
                    byte = connection.recv(1)
                except (socket.error):
                    connection_kaputt(connection)
                else:
                    if not byte:
                        connection_kaputt(connection)
                    elif has_token != connection:
                        debug('Meinte wohl, wäre dran!', addrs[connection])
                        connection.close()
                    else:
                        debug('Will nicht mehr dran sein:', addrs[connection])
                        has_token = listener
        if connections and has_token == listener:
            connection = connections.pop(0)
            connections.append(connection)
            try:
                bytes_sent = connection.send(b'!')
            except (socket.error):
                connection_kaputt(connection)
            else:
                if bytes_sent == 1:
                    has_token = connection
                    debug("Der ist dran:", addrs[connection])
        elif not connections:
            debug('keine Verbindungen, schließe!')
            break

server_process = None

def start_dedicated_server():
    global server_process
    server_process = subprocess.Popen([sys.executable, __file__])

connection = None
ich_bin_dran = False

wait_for_server_to_start = 1 # seconds

def connect():
    global connection
    if not connection:
        _connection = socket.socket()
        for i in range(10):
            try:
                _connection.connect(ADDRESS)
            except (socket.error):
                start_dedicated_server()
                time.sleep(wait_for_server_to_start)
            else:
                connection = _connection
                break
        if not connection:
            raise Exception('Could not connect to server at', ADDRESS)

def reconnect():
    disconnect()
    connect()

def disconnect():
    global connection
    if connection:
        connection.close()
    connection = None
    

def schedule():
    global ich_bin_dran
    connect()
    while 1:
        if ich_bin_dran:
            try:
                connection.send(b'?')
            except (socket.error):
                ich_bin_dran = False
                reconnect()
            else:
                ich_bin_dran = False
        if not ich_bin_dran:
            try:
                connection.recv(1)
            except (socket.error):
                reconnect()
            else:
                ich_bin_dran = True
                break

def main(_print_to_stdout = False):
    global print_to_stdout
    print_to_stdout = _print_to_stdout
    try:
        serve()
    except:
        traceback.print_exc(file = debug_file())

__all__ = 'connect disconnect reconnect main schedule serve debug_file debug '\
          'ADDRESS PORT start_dedicated_server'.split()

if __name__ == '__main__':
    main()
