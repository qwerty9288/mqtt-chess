import paho.mqtt.client as mqtt
import time
import random
import re

broker = 'localhost'
port = 1883
client_id = f'mqtt-chess-{random.randint(0, 100)}'
color = None
opponent_color = None

def login(client):
   print("Please provide login credentials.")
   username = str(input("Username: "))
   password = str(input("Password: "))
   client.username_pw_set(username, password)
   return client

def connect(client: mqtt):
    def on_connect(client: mqtt, userdata, flags, rc):
        global client_id
        if rc == 0:
            print("Connected to MQTT Broker!")
            topic = str(input("Please provide game name (mqtt topic): "))
            client = subscribe(client, topic)
            client.publish(f"{topic}/join/{client_id}", client_id, retain = True)
        else:
            print("Failed to connect, return code %d\n", rc)
            client.loop_stop()

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt, topic: str):
    def on_message(client, userdata, msg):
        global color, opponent_color, client_id
        payload = msg.payload.decode('utf-8')
        #print(f"*** received {payload} from {msg.topic}")
        if msg.topic == f"{topic}/join/{client_id}":
            if color == None:
                color = str(input("Please pick whether you want to play white or black: "))
                opponent_color = 'white' if color == 'black' else 'black'
                client.publish(f"{topic}/color/{color}", client_id, retain = True)
        elif msg.topic.startswith(f"{topic}/join/") and payload != '':
            print(f"Your opponent {payload} joined the game.")
            client.publish(f"{topic}/join/{payload}", '', retain = True)
        elif msg.topic == f"{topic}/color/white" and color == None and payload != '':
            color = 'black'
            opponent_color = 'white'
            print(f"My color: {color}, opponent's color: {opponent_color}")
            client.publish(f"{topic}/color/white", '', retain = True)
            client.publish(f"{topic}/start", client_id)
        elif msg.topic == f"{topic}/color/black" and color == None and payload != '':
            color = 'white'
            opponent_color = 'black'
            print(f"My color: {color}, opponent's color: {opponent_color}")
            client.publish(f"{topic}/color/black", '', retain = True)
            client.publish(f"{topic}/start", client_id)
        elif msg.topic == f"{topic}/start" and color == "white":
            client.publish(f"{topic}/move/white", client_id)
        elif msg.topic == f"{topic}/move/{color}":
            move = str(input("Your move: "))
            if move == 'end':
                client.disconnect()
                client.loop_stop()
            elif is_legal(move):
                client.publish(f"{topic}/game/{color}", move)
                client.publish(f"{topic}/move/{opponent_color}", 'doit')
            else:
                print("Illegal move, try again.")
                client.publish(f"{topic}/move/{color}", client_id)
        elif msg.topic == f"{topic}/game/white":
            print(f"White: {payload}")
        elif msg.topic == f"{topic}/game/black":
            print(f"Black: {payload}")

    client.subscribe(f"{topic}/#")
    client.on_message = on_message
    return client

def is_legal(move):
    pawnpattern1 = r"[a-h][3-7][#|+]?"
    pawnpattern2 = r"^[a-h][x][a-h][3-7][#|+]?"
    pawnpattern3 = r"^[a-h][8][=][QBNR][#|+]?"
    pawnpattern4 = r"^[a-h][x][a-h][8][=][QBNR][#|+]?"
    piecepattern1 = r"^[BQNRK][a-h][1-8][#|+]?"
    piecepattern2 = r"^[BQNRK][x][a-h][1-8][#|+]?"
    piecepattern3 = r"^[BQNR][a-h1-8][a-h][1-8][#|+]?"
    piecepattern5 = r"^[BQNR][a-h1-8][x][a-h][1-8][#|+]?"
    piecepattern6 = r"^[BQNR][a-h][1-8][a-h][1-8][#|+]?"
    piecepattern4 = r"^[BQNR][a-h][1-8][x][a-h][1-8][#|+]?"

    if re.match(pawnpattern1, move) is not None:
        return True
    elif re.match(piecepattern1, move) is not None:
        return True
    elif re.match(pawnpattern3, move) is not None:
        return True
    elif re.match(pawnpattern4, move) is not None:
        return True
    elif re.match(piecepattern2, move) is not None:
        return True
    elif re.match(pawnpattern2, move) is not None:
        return True
    elif re.match(piecepattern3, move) is not None:
        return True
    elif re.match(piecepattern4, move) is not None:
        return True
    elif re.match(piecepattern5, move) is not None:
        return True
    elif re.match(piecepattern6, move) is not None:
        return True
    elif move == "O-O-O" or move == "O-O":
        return True
    return False

def run():
    print(f"My client_id: {client_id}")
    client = mqtt.Client(client_id)
    client = login(client)
    client = connect(client)
    client.loop_forever()

if __name__ == '__main__':
    run()