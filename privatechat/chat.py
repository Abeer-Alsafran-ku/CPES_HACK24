import streamlit as st
import sqlite3
import string
import random
# from cryptography.fernet import Fernet

# Create and connect to SQLite database
conn = sqlite3.connect('global_data.db')
c = conn.cursor()

def load_global_dict():
    c.execute("SELECT * FROM rooms")
    rows = c.fetchall()
    global_dict = {}
    for row in rows:
        room_name, user1,user2, encKey = row
        global_dict[room_name] = {'user1': user1,'user2':user2, 'encKey': encKey}
    return global_dict

# Create a table to store rooms
c.execute('''
CREATE TABLE IF NOT EXISTS rooms (
    room_name TEXT PRIMARY KEY,
    user1 TEXT,
    user2 TEXT,
    encKey TEXT
)
''')
conn.commit()


if 'data' not in st.session_state:
    st.session_state.data = {}

if 'user_name1' not in st.session_state:
    st.session_state.user_name1 = {}

if 'user_name2' not in st.session_state:
    st.session_state.user_name2 = {}



# def generate_encryption_key():
#     return Fernet.generate_key()

# def encrypt_key(plain_text_key, encryption_key):
#     # Create a Fernet instance with the encryption key
#     fernet = Fernet(encryption_key)
    
#     # Encrypt the plain text key (it must be converted to bytes)
#     encrypted_key = fernet.encrypt(plain_text_key.encode())
    
#     return encrypted_key

# def decrypt_key(encrypted_key, encryption_key):
#     fernet = Fernet(encryption_key)
#     decrypted_key = fernet.decrypt(encrypted_key).decode()
    
#     return decrypted_key


# def encrypt_key(plain_text_key, encryption_key):
#     # Create a Fernet instance with the encryption key
#     fernet = Fernet(encryption_key)
    
#     # Encrypt the plain text key (it must be converted to bytes)
#     encrypted_key = fernet.encrypt(plain_text_key.encode())
    
#     return encrypted_key

# def decrypt_key(encrypted_key, encryption_key):
#     fernet = Fernet(encryption_key)
#     decrypted_key = fernet.decrypt(encrypted_key).decode()
    
#     return decrypted_key


def check_data(chatroom_name,username,key):
    data = load_global_dict()
    print(f'data = {data}')
    if chatroom_name in data:
        if data[chatroom_name]['encKey'] == key:
            if data[chatroom_name]['user2'] == username or data[chatroom_name]['user1'] == username:
                return True
            if data[chatroom_name]['user2'] == None:
                update_room(username,chatroom_name)
                return True
            else:
                print('Users are full')
                return False
        else:
            print('key unmatched')
            return False
    else:
        print('Chat room name dne')



def crate_rand_room_name(length = 5):
        # Define the possible characters: letters, digits, and special characters
    characters = string.ascii_letters + string.digits + string.punctuation
    # Randomly select 'length' number of characters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

# Function to display the home page
def homePage():
    data = load_global_dict()
    print(f' data = {data}')
    st.title("Welcome to pMsg!")
    st.subheader("Your #1 private chat!")

    st.write("""
    In this app, you are the only one who knows about your chat history 
    because it is 100% secure.
    """)

    # Button to navigate to the login page
    if st.button('Enter a room'):
        st.session_state.page = 'login_page'
    if st.button('Create chatroom'):
        st.session_state.page = 'create_chatroom'
    if st.button('Delete chatroom'):
        st.session_state.page = 'delete_chatroom'
    # Add an image (replace with your image path)
    st.image("/Users/abeeralsafran/Desktop/CPES_HACK24/tw.jpg")

    # Features description
    st.markdown("""
    ### Features of this App:
    - Simple and easy to use
    - Real-time interaction
    - Beautifully designed interface
    """)

def update_room(username,room_name):
    c.execute("UPDATE rooms SET user2 = ? WHERE room_name = ?", (username, room_name))
    conn.commit()

# Function to display the login page
def login_page():
    if 'chatroom_name' not in st.session_state:
        st.session_state.chatroom_name = None

    if 'user_name1' not in st.session_state:
        st.session_state.user_name1 = None

    st.title("Login Page")
        # Button to navigate back to home page
    if st.button('Go Back to Home'):
        st.session_state.page = 'home'
    st.subheader("Please enter your username, chatroom name, and encryption key to log in.")

    # Input fields for login
    username = st.text_input('Username', key='username')
    plain_text_key = st.text_input('Encryption Key', key='encryption_key')
    chatroom_name = st.text_input('Chatroom Name', key='chatroom_name')
    # encryption_key = generate_encryption_key()
    # decrypted_key = decrypt_key(encrypted_key_input.encode(), encryption_key_input.encode())
    # Button to login
    if st.button('Login'):
        if username and chatroom_name and plain_text_key:
            if check_data(chatroom_name,username,plain_text_key):
                # update_room(username,chatroom_name)
                # st.session_state.chatroom_name = chatroom_name
                st.session_state.user_name1 = username
                st.session_state.page = 'chat'
            else:
                st.error("Some error occured!")

        else:
            st.error("Please fill in all fields before logging in.")


def del_chatroom(chatroom_name,key):
    data = load_global_dict()
    if chatroom_name in data:
        # del st.session_state.data[chatroom_name]
        c.execute("DELETE FROM rooms where room_name = ? AND encKey = ?",(chatroom_name,key))
        conn.commit()
    # this is to check if the room exists and then delete it 
        return True
    else:
        return False

def delete_chatroom():
    data = load_global_dict()
    st.title("Delete a chatroom")
    if st.button('Go Back to Home'):
        st.session_state.page = 'home'
    st.write("To delete a chatroom you need to enter the room name and the encrypted key")

    chatroom_name = st.text_input('Chatroom Name', key='chatroom_name')
    key = st.text_input('Encryption Key', key='encryption_key')

    if st.button('Delete'):
        if del_chatroom(chatroom_name,key):
            st.write(f'Room {chatroom_name} has been deleted successfully!')
        else:
            st.write(f'Room {chatroom_name} has not been deleted successfully!, try again!')


def new_room(room_name, user1, enc_key):
    c.execute("INSERT INTO rooms (room_name, user1, encKey) VALUES (?, ?, ?)",
              (room_name, user1, enc_key))
    conn.commit()


def create_chatroom():
    if 'chatroom_name' not in st.session_state:
        st.session_state.chatroom_name = None

    if 'user_name1' not in st.session_state:
        st.session_state.user_name1 = None

    st.title('To create a chatroom enter the encryption key and then click the below button and it will create for you the channel name ')
    
    username = st.text_input('Username', key='username')
    
    plain_text_key = st.text_input('Encryption key', key='enc_key')
    # encryption_key = generate_encryption_key()
    # encrypted_key = encrypt_key(plain_text_key, plain_text_key)

    if st.button('Create a chatroom '):
        chatroom_name = crate_rand_room_name()
        # st.session_state.chatroom_name = chatroom_name
        # st.session_state.user_name1 = username
        new_room(chatroom_name,username,plain_text_key)
        st.session_state.page = 'chat'

def leave_chatroom(username,room_name):
    # st.session_state.data[room_name][]
    # a code to remove a member from the room i.e remove from data 
    data = load_global_dict()
    if room_name in data:
        room_data = data[room_name]
        if username in room_data['user1']:
            c.execute("UPDATE rooms SET user1 = ? WHERE room_name = ?", (None, room_name))
            conn.commit()
            st.write(f"User '{username}' removed from '{room_name}'")
        elif username in room_data['user2']:
            c.execute("UPDATE rooms SET user2 = ? WHERE room_name = ?", (None, room_name))
            conn.commit()        
            st.write(f"User '{username}' removed from '{room_name}'")
        else:
            st.write(f"User '{username}' not found in '{room_name}'")
    else:
        st.write(f"Room '{room_name}' not found")

    return;

# Function to display the chat page
def chat():
    
    data = load_global_dict()
    print(f'data in chat = {data}')
    uname = st.session_state.user_name1
    # room_name = st.session_state.chatroom_name
    # st.title(f"Chat Room: {st.session_state.chatroom_name}")
    # st.title(f"Chat Room: {room_name}")

    if st.button('Leave chatroom'):
        leave_chatroom(uname,'o/(56')
        st.session_state.page = 'home'

    prompt = st.chat_input("Say something")
    if prompt:
        st.write(f"me: {prompt}")



########### MAIN #############
# Main function to manage page routing
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Render the correct page based on session state
if st.session_state.page == 'home':
    homePage()
elif st.session_state.page == 'login_page':
    login_page()
elif st.session_state.page == 'chat':
    chat()
elif st.session_state.page == 'create_chatroom':
    create_chatroom()
elif st.session_state.page == 'delete_chatroom':
    delete_chatroom()