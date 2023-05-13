# Distributed chess game using MQTT

The script will ask you for username and password to connect to an mqtt broker, along with the channel in which you want to play chess. Both players have to coordinate and pick the same channel to play in the same game. After that the players can start to write their moves, which will be displayed for both players.

## Example

<table>
<tr>
<th>Client 1</th>
<th>Client 2</th>
</tr>
<tr>
<td>

```
$ python ./mqtt-chess.py
My client_id: mqtt-chess-67
Please provide login credentials.
Username: steve
Password: sa1
Connected to MQTT Broker!
Please provide game name (mqtt topic): chess
Please pick whether you want to play white or black: white
Your opponent mqtt-chess-82 joined the game.
Your move: e4
White: e4
Black: e5
Your move: Nf3
White: Nf3
```

</td>
<td>

```
$ python ./mqtt-chess.py
My client_id: mqtt-chess-82
Please provide login credentials.
Username: test
Password: test
Connected to MQTT Broker!
Please provide game name (mqtt topic): chess
My color: black, opponent's color: white
Your opponent mqtt-chess-67 joined the game.
White: e4
Your move: e5
Black: e5
White: Nf3
Your move: h1
Illegal move, try again.
```

</td>
</tr>
</table>