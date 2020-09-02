from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms as flask_rooms
from time import sleep
from threading import Thread
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

rooms = {}
threads = list()

@app.route('/')
def sessions():
    return render_template('session.html')

@app.route('/reset')
def handle_reset_event():
    global rooms
    print('reseting')
    rooms = {}

@socketio.on('new_connect')
def new_connect():
    print(f'new client {request.sid}')
    emit('new_connect', {'id': request.sid}, json=True, room=request.sid)

@socketio.on('join_room')
def on_join(data):
    global rooms
    username = data['name']
    room = data['room']
    if room not in rooms:
        print(f'new room: {room}')
        rooms[room] = {}
        rooms[room]['fill'] = 0
        rooms[room]['users'] = []

    join_room(room)
    rooms[room]["users"].append({"user":username,"id":request.sid})
    print(f'{username} joined {room} of rooms {flask_rooms(request.sid)} ')
    emit('join_room', {'user': username, 'id': request.sid, 'room': room}, json=True, room=room)

@socketio.on('leave_room')
def on_leave(data):
    username = data['name']
    room = data['room']
    leave_room(room)
    print(f'{username} left {room} of rooms {flask_rooms(request.sid)} ')
    emit('leave_room', {'user': username, 'id': request.sid, 'room': room}, json=True, room=room)

@socketio.on('here')
def on_here(data):
    username = data['name']
    room = data['room']
    print(f'!!! HERE {username} is in {room} of rooms {flask_rooms(request.sid)} ')
    emit('here', {'user': username, 'id': request.sid, 'room': room}, json=True, room=room)

@socketio.on('pour')
def handle_pour_event(data, methods=['GET', 'POST']):
    global rooms
    print('pouring: ' + str(data))

    rooms[data['room']]['fill']+= random.randint(1,5)
    if rooms[data['room']]['fill'] >= 150:
        socketio.emit('game_over', data, room=data['room'])

    socketio.emit('pour', { "room": data['room'],"fill":rooms[data['room']]['fill'] }, room=data['room'])

def beep(room, time):
    sleep(time)
    socketio.emit('beep', room=room)

@app.route('/start/<room>/<int:time>')
def start(room, time):
    t = Thread(target=beep, args=(room, time))
    threads.append(t)
    t.start()
    return "OK"

if __name__ == '__main__':
    socketio.run(app, port=8088, debug=True, host="127.0.0.1")
