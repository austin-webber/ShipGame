# Author: Austin Webber
# GitHub username: austin-webber
# Date: 3/5/2022
# Description: Program that contains a class and methods that allow two players to play the game Battleship. Start
#              a new game with the ShipGame class. Each player uses the "place_ship" method to place their units on
#              a 10x10 grid. Using the "fire_torpedo" method, 'first' gets the first turn to fire a torpedo, after
#              which players alternate. Hit all squares of an enemy ship to sink it. Player wins when all of
#              their enemy's ships have sunk! Check this using the methods get_num_ships_remaining and
#              get_current_state.

class ShipGame:
    """Represents a two player game of Battleship. Each player has their own 10x10 grid they place their ships on.
    On their turn, they can fire a torpedo at a square on the enemy’s grid. Player ‘first’ gets the first turn to
    fire a torpedo, after which players alternate firing torpedoes. A ship is sunk when all of its squares have
    been hit. When a player sinks their opponents final ship, they win."""

    def __init__(self):
        """Constructor for the ShipGame class. Takes no parameters. Creates a new game and initializes all
        data members to their initial values. All data members are private."""

        self._turn_counter = "first"        # player 'first' takes first turn in fire_torpedo
        self._valid_square_counter = 0      # used in place_ship method
        self._first_ships_counter = 0       # used in get_current_state to confirm ships have been placed
        self._second_ships_counter = 0

        # so I can convert coordinates in the place_ship method for indexing into the grids
        # "Z" is on the end as a buffer so place_ships can work. Not very clean, but it works
        self._grid_dict = {"A": 0, "B": 1, "C": 2, "D": 3, 'E': 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "Z": 10}

        self._first_ships = []
        self._second_ships = []

        self._first_board = []
        self._second_board = []
        # Initializing the players' empty boards
        for row in range(10):
            self._first_board.append([" "] * 10)
            self._second_board.append([" "] * 10)

    def place_ship_rec(self, player_number, squares_to_check, current_coordinate, orientation):
        """Takes four parameters:
            player_number - represents which player (‘first’ or ‘second’) is placing the ship.
            squares_to_check - represents how many squares this method needs to validate are empty for placement.
            current_coordinate - current square that this method is checking to validate placement.
            orientation - ‘R’ if the ship’s squares occupy the same row, or ‘C’ if its squares occupy the same column.
        Purpose: This recursive method allows a player to add a ship to their 10x10 grid with a specific length,
        position, and orientation. Does not enforce turn order. Assumes that calls to this method are made before any
        other methods are called.
        return:
            False - if a ship wouldn't fit entirely on that player’s grid, if it would overlap any previously
            placed ships, or if the length of the ship is less than 2.
            True - otherwise."""

        row = self._grid_dict.get(current_coordinate[0])    # unpacking the coordinate so I can index into the lists
        column = int(current_coordinate[1:]) - 1

        # IF PLAYER 'FIRST' IS CALLING THE METHOD

        if player_number == "first":

            # establish the base cases
            if str(current_coordinate[0]) not in self._grid_dict:
                return False                                # row not in grid_dict
            if row < 0 or row >= len(self._first_board):
                return False                                # row out of bounds
            if column < 0 or column > (len(self._first_board) - 1):
                return False                                # column out of bounds
            if self._first_board[row][column] == "x":
                return False                                # ship already at coordinate

            # IF SHIP'S SQUARES OCCUPY SAME ROW

            if orientation == "R":
                same_row = str(current_coordinate[0])
                next_column = str(column + 2)  # + 2 because we subtracted 1 at the start for proper indexing
                square_to_right = same_row + next_column
                squares_to_check -= 1          # - 1 because initial square is free if we're here
                self._valid_square_counter += 1          # counter for number of valid squares

                if squares_to_check > 0:       # there are more squares to check
                    if self.place_ship_rec(player_number, squares_to_check, square_to_right, "R"):
                        return True            # returns True on the way back out if True
                    else:
                        return False           # returns False on the way back out if False

                elif squares_to_check == 0:    # no more squares_to_check, place ship
                    ship_length = 0
                    ship_coordinates_list = []
                    for i in range(self._valid_square_counter):
                        self._first_board[row][column] = "x"
                        ship_coordinates_list.append(str(row) + str(column))
                        ship_length += 1
                        column -= 1
                    self._valid_square_counter = 0      # resetting the counter for future method calls
                    self._first_ships_counter += 1
                    self._first_ships.append(Ship(ship_length, ship_coordinates_list))      # storing ship object
                    return True

            # IF SHIP'S SQUARES OCCUPY SAME COLUMN

            elif orientation == "C":

                dict_list = list(self._grid_dict.keys())
                next_row = str(dict_list[dict_list.index(current_coordinate[0]) + 1])
                same_column = str(column + 1)  # + 1 because we subtracted 1 at the start for proper indexing
                square_down = next_row + same_column
                squares_to_check -= 1  # - 1 because initial square is free if we're here
                self._valid_square_counter += 1  # counter for number of valid squares

                if squares_to_check > 0:  # there are more squares to check
                    if self.place_ship_rec(player_number, squares_to_check, square_down, "C"):
                        return True  # returns True on the way back out if True
                    else:
                        return False  # returns False on the way back out if False

                elif squares_to_check == 0:  # no more squares_to_check, place ship
                    ship_length = 0
                    ship_coordinates_list = []
                    for i in range(self._valid_square_counter):
                        self._first_board[row][column] = "x"  # placing the ship in the player's grid
                        ship_coordinates_list.append(str(row) + str(column))
                        ship_length += 1
                        row -= 1
                    self._valid_square_counter = 0  # resetting the counter for future method calls
                    self._first_ships_counter += 1
                    self._first_ships.append(Ship(ship_length, ship_coordinates_list))  # storing ship object
                    return True

        # IF PLAYER 'SECOND' IS CALLING THE METHOD

        if player_number == "second":

            # establish the base cases
            if str(current_coordinate[0]) not in self._grid_dict:
                return False                                # row not in grid_dict
            if row < 0 or row >= len(self._second_board):
                return False                                # row out of bounds
            if column < 0 or column > (len(self._second_board) - 1):
                return False                                # column out of bounds
            if self._second_board[row][column] == "x":
                return False                                # ship already at coordinate

            # IF SHIP'S SQUARES OCCUPY SAME ROW

            if orientation == "R":             # SHIP'S SQUARES OCCUPY SAME ROW
                same_row = str(current_coordinate[0])
                next_column = str(column + 2)  # + 2 because we subtracted 1 at the start for proper indexing
                square_to_right = same_row + next_column
                squares_to_check -= 1          # - 1 because initial square is free if we're here
                self._valid_square_counter += 1          # counter for number of valid squares

                if squares_to_check > 0:       # there are more squares to check
                    if self.place_ship_rec(player_number, squares_to_check, square_to_right, "R"):
                        return True            # returns True on the way back out if True
                    else:
                        return False           # returns False on the way back out if False

                elif squares_to_check == 0:    # no more squares_to_check, place ship
                    ship_length = 0
                    ship_coordinates_list = []
                    for i in range(self._valid_square_counter):
                        self._second_board[row][column] = "x"
                        ship_coordinates_list.append(str(row) + str(column))
                        ship_length += 1
                        column -= 1
                    self._valid_square_counter = 0
                    self._second_ships_counter += 1
                    self._second_ships.append(Ship(ship_length, ship_coordinates_list))  # storing ship object
                    return True

            # IF SHIP'S SQUARES OCCUPY SAME COLUMN

            elif orientation == "C":           # SHIP'S SQUARES OCCUPY SAME COLUMN
                dict_list = list(self._grid_dict.keys())
                next_row = str(dict_list[dict_list.index(current_coordinate[0]) + 1])
                same_column = str(column + 1)       # + 1 because we subtracted 1 at the start for proper indexing
                square_down = next_row + same_column
                squares_to_check -= 1          # - 1 because initial square is free if we're here
                self._valid_square_counter += 1          # counter for number of valid squares

                if squares_to_check > 0:       # there are more squares to check
                    if self.place_ship_rec(player_number, squares_to_check, square_down, "C"):
                        return True  # returns True on the way back out if True
                    else:
                        return False  # returns False on the way back out if False

                elif squares_to_check == 0:    # no more squares_to_check, place ship
                    ship_length = 0
                    ship_coordinates_list = []
                    for i in range(self._valid_square_counter):
                        self._second_board[row][column] = "x"    # placing the ship in the player's grid
                        ship_coordinates_list.append(str(row) + str(column))
                        ship_length += 1
                        row -= 1
                    self._valid_square_counter = 0          # resetting the counter for future method calls
                    self._second_ships_counter += 1
                    self._second_ships.append(Ship(ship_length, ship_coordinates_list))  # storing ship object
                    return True

        else:
            return False            # if player_number argument isn't 'first' or 'second'

    def place_ship(self, player_number, ship_length, closest_coordinate, orientation):
        """Takes four parameters:
                player_number - represents which player (‘first’ or ‘second’) is placing the ship.
                ship_length - how long (in grid squares) the ship is.
                closest_coordinate - the coordinates, e.g. ‘B7’ of the square it will occupy that is closest to A1
                of the grid.
                orientation - ‘R’ if the ship’s squares occupy the same row, or ‘C’ if its squares occupy the same
                column.
            Purpose: Helper method for the recursive place_ship_rec method. In this case, the helper method was
            used in order to check ship_length before entering the recursive function. Then ship_length is free to be
            assigned to another variable.
            return:
                False - if a ship wouldn't fit entirely on that player’s grid, if it would overlap any previously
                placed ships, or if the length of the ship is less than 2.
                True - otherwise."""

        if ship_length < 2:
            return False

        else:
            squares_to_check = ship_length       # the amount of squares we'll need to confirm are empty
            return self.place_ship_rec(player_number, squares_to_check, closest_coordinate, orientation)

    def get_current_state(self):
        """Takes no parameters.
        Purpose: Returns the current state of the game
        return:
        ‘FIRST_WON’ - if the first player has won.
        ‘SECOND_WON’ - if the second player has won.
        ‘UNFINISHED’ - if no player has won the game yet"""

        # the ships_counter is incremented when a valid ship is placed. If either one is 0,
        # then that player hasn't placed any ships yet.
        if self._first_ships_counter == 0 or self._second_ships_counter == 0:
            return "UNFINISHED"

        # if both players have placed a valid ship, we check to see if there are any still standing
        elif self._first_ships_counter > 0 and self._second_ships_counter > 0:

            if len(self._first_ships) == 0:
                return "SECOND_WON"

            elif len(self._second_ships) == 0:
                return "FIRST_WON"

            else:
                return "UNFINISHED"         # both players have ships still standing

    def fire_torpedo(self, player_number, target_coordinates):
        """Takes two parameters:
            player_number - represents which player (‘first’ or ‘second’) is firing the torpedo.
            target_coordinates - the coordinates of the target square, e.g. ‘B7’.
        Purpose: Allows the player to fire a torpedo at a square on the enemy’s grid. A ship is sunk when all of its
        squares have been hit. Player ‘first’ gets the first turn to fire a torpedo, after which players alternate.
        Assumes the place_ship method will not be called after firing of the torpedoes has started.
        return:
            False - if it is not that player’s turn to fire, or if the game has already been won. If the player has
            fired on that square before, they just waste a turn.
            True - otherwise. Records the move, updates the turn counter.
        """

        target_row = self._grid_dict.get(target_coordinates[0])  # unpacking so I can index into the lists
        target_column = int(target_coordinates[1:]) - 1

        if self.get_current_state() == "FIRST_WON" or self.get_current_state() == "SECOND_WON":
            return False                                                        # False if game is already over

        if str(target_coordinates[0]) not in self._grid_dict:
            return False                                                        # False if row not in grid_dict
        if target_row < 0 or target_row >= len(self._first_board):
            return False                                                        # False if row out of bounds
        if target_column < 0 or target_column > (len(self._first_board) - 1):
            return False                                                        # False if column out of bounds

        if player_number == self._turn_counter:                         # confirming it is that player's turn

            if player_number == "first":
                self._second_board[target_row][target_column] = "o"
                self._turn_counter = "second"

                for ship in self._second_ships:                         # checking to see if a ship was at those coords
                    if target_coordinates in ship.get_coordinates():    # if so, increment that ship's hit counter
                        ship.hit()
                    if ship.get_length() == ship.get_hits():            # if hits == length, sink it
                        self._second_ships.remove(ship)
                return True

            if player_number == "second":
                self._first_board[target_row][target_column] = "o"
                self._turn_counter = "first"

                for ship in self._first_ships:
                    if target_coordinates in ship.get_coordinates():
                        ship.hit()
                    if ship.get_length() == ship.get_hits():
                        self._first_ships.remove(ship)
                return True

        else:
            return False

    def get_num_ships_remaining(self, player_number):
        """Takes one parameter:
            player_number - represents which player (‘first’ or ‘second’) we want to find information about.
        Purpose: Returns the number of ships the specified player has left.
        """

        if player_number == "first":
            return len(self._first_ships)

        elif player_number == "second":
            return len(self._second_ships)


class Ship:
    """Creates a ship object with attributes that can be accessed and adjusted via get methods."""

    def __init__(self, length, coordinates_list):
        """Takes two parameters:
            length - represents the length of the ship in grid squares.
            coordinates_list - a list of coordinates, e.g. [B7, B8], that the ship is placed on.
        Purpose: The Ship class constructor. Creates a new ship and initializes all data members. All data members
        are private."""

        self._ship_length = length

        self._grid_dict = {"A": 0, "B": 1, "C": 2, "D": 3, 'E': 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
        dict_list = list(self._grid_dict.keys())

        self.ship_coordinates_list = []

        for coordinate in coordinates_list:
            row = str(dict_list[int(coordinate[0])])     # translating row index to row letter
            column = int(coordinate[1]) + 1              # + 1 because first square is A1 not A0
            self.ship_coordinates_list.append(row + str(column))    # now this list will, for example, look like
                                                                    # ["A1", "A2", "A3"]
        self._hits = 0

    def get_length(self):
        """Takes no parameters.
        Purpose: Returns the length of the ship"""
        return self._ship_length

    def get_hits(self):
        """Takes no parameters.
        Purpose: Returns how many times the ship has been hit"""
        return self._hits

    def hit(self):
        """Takes no parameters.
        Purpose: Increases the number of hits the ship has taken when a torpedo strikes it."""
        self._hits += 1

    def get_coordinates(self):
        """Takes no parameters.
        Purpose: Returns a list consisting of the coordinates on which the ship is placed."""
        return self.ship_coordinates_list


# game = ShipGame()
# print(game.get_current_state())
# print(game.place_ship("first", 2, "A1", "C"))
# print(game.place_ship("second", 2, "A3", "R"))
# print(game.get_num_ships_remaining("second"))
# print(game.get_current_state())
# print(game.fire_torpedo("first", "A3"))
# print(game.fire_torpedo("second", "A1"))
# print(game.fire_torpedo("first", "H7"))
# print(game.get_current_state())
# print(game.fire_torpedo("second", "B1"))
# print(game.get_current_state())
# print(game.get_num_ships_remaining("first"))
# print(game.get_num_ships_remaining("second"))
# for row in game._first_board:
#     print(row)
# for row in game._second_board:
#     print(row)
