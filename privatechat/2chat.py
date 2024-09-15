import sqlite3
import streamlit as st

# Create and connect to SQLite database
conn = sqlite3.connect('global_data.db')
c = conn.cursor()

# Create a table to store rooms
c.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    room_name TEXT PRIMARY KEY,
    user1 TEXT,
    encKey TEXT
)
''')
conn.commit()

# Load data from database into session state
def load_global_dict():
    c.execute("SELECT * FROM rooms")
    rows = c.fetchall()
    global_dict = {}
    for row in rows:
        room_name, user1, encKey = row
        global_dict[room_name] = {'user1': user1, 'encKey': encKey}
    return global_dict

# Save room to database
def add_or_update_room_in_db(room_name, user1, enc_key):
    c.execute("REPLACE INTO rooms (room_name, user1, encKey) VALUES (?, ?, ?)",
              (room_name, user1, enc_key))
    conn.commit()

# Delete room from database
def delete_room_from_db(room_name):
    c.execute("DELETE FROM rooms WHERE room_name = ?", (room_name,))
    conn.commit()

# Initialize the global dictionary from database (only once)
if 'global_dict' not in st.session_state:
    st.session_state.global_dict = load_global_dict()

# Function to add or update a room in the global dictionary
def add_or_update_room(room_name, user, enc_key):
    st.session_state.global_dict[room_name] = {'user1': user, 'encKey': enc_key}
    add_or_update_room_in_db(room_name, user, enc_key)

# Function to delete a room
def delete_room(room_name):
    if room_name in st.session_state.global_dict:
        del st.session_state.global_dict[room_name]
        delete_room_from_db(room_name)

# Display the current state of the global dictionary
st.write(f"Global Dictionary: {st.session_state.global_dict}")

# Inputs to edit the global dictionary
room_name = st.text_input('Enter Room Name')
user = st.text_input('Enter User Name')
enc_key = st.text_input('Enter Encryption Key')

# Button to add or update the dictionary
if st.button('Add/Update Room'):
    add_or_update_room(room_name, user, enc_key)
    st.write(f"Updated Global Dictionary: {st.session_state.global_dict}")

# Button to delete a room
if st.button('Delete Room'):
    delete_room(room_name)
    st.write(f"Global Dictionary after deletion: {st.session_state.global_dict}")
