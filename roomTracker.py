#!/usr/bin/python
# pipelineTracker.py Jacob Kern
# Stores which pipelines are running on which nodes

import os
import json
import sqlite3

DB_NAME = 'users.db'

def _exec(sql, parameters=''):
    conn = sqlite3.connect(config["db_name"])
    data = conn.execute(sql, parameters)
    conn.commit()
    conn.close()
    return data

def create():
    _exec('CREATE TABLE users_id INTEGER PRIMARY KEY, user TEXT NOT NULL, sid TEXT NOT NULL)')
    _exec('CREATE UNIQUE INDEX idx_users ON users (sid)')
    _exec('CREATE TABLE rooms (room_id INTEGER PRIMARY KEY, room TEXT NOT NULL, fill INTEGER)')
    _exec('CREATE UNIQUE INDEX idx_rooms ON rooms (room)')
    _exec('''CREATE TABLE room_map (room_id INTEGER, user_id INTEGER)
               PRIMARY KEY (room_id, user_id),
               FOREIGN KEY (room_id)
                  REFERENCES rooms (room_id)
                     ON DELETE CASCADE
                     ON UPDATE NO ACTION,
               FOREIGN KEY (user_id)
                  REFERENCES users (user_id)
                     ON DELETE CASCADE
                     ON UPDATE NO ACTION
    ''')

def set(user, id, room):
    ''' Args in order Who, What, 'When', Where, Why'''
    if not os.path.exists(DB_NAME):
        create(
    conn = sqlite3.connect(config["db_name"])
    conn.execute('INSERT INTO users VALUES (?,?)', (user, sid))
    conn.execute('INSERT INTO rooms VALUES (?,?)', (room, 0))
    conn.commit()
    user_id = conn.execute('SELECT * FROM users WHERE sid=?', (id)).fetchone()
    room_id = conn.execute('SELECT * FROM rooms WHERE room=?', (pipeline_id,)).fetchone()
    _exec('INSERT INTO room_map VALUES (?,?)', (, 0))


def get(pipeline_id):
    conn = sqlite3.connect(config["db_name"])
    data = conn.execute('SELECT * FROM pipelines WHERE pipeline_id=?', (pipeline_id,)).fetchone()
    conn.commit()
    conn.close()
    return data

def remove(pipeline_id):
    _exec('DELETE FROM pipelines WHERE pipeline_id=?', (pipeline_id,))

def clear_db():
    _exec('DELETE FROM pipelines')
