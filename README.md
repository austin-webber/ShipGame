# ShipGame

This was the Portfolio Project Final for CS162 at OSU.

The ShipGame Python file includes a class that allows two players to play the game Battleship.

Each player has their own 10x10 grid they place their ships on using the "place_ship" method which is implemented with a recursive helper function.

Players take turns firing torpedos at a square on the enemy's grid using the "fire_torpedo" method.

A player wins when they sink their opponent's final ship. 

The current state of the game can be retrieved using the "get_current_state" method, and "get_num_ships_remaining" returns how many ships the specified player has left.
