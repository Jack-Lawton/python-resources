from random import randint, choice


class ColourLookup:
    NUMBERS = {
        2: '\033[92m',
        4: '\033[32m',
        8: '\033[94m',
        16: '\033[34m',
        32: '\033[35m',
        64: '\033[91m',
        128: '\033[95m',
        256: '\033[96m',
        512: '\033[33m',
        1024: '\033[93m',
        2048: '\033[36m',
        4096: '\033[31m'
    }
    X_BIG = '\033[31m'
    ENDC = '\033[0m'


class Cell:
    def __init__(self, value):
        self.v = value
        self.can_sum = True

    def __str__(self):
        value = str(self.v)
        if value == "0":
            value = ""

        if self.v in ColourLookup.NUMBERS:
            start_c = ColourLookup.NUMBERS[self.v]
        else:
            start_c = ColourLookup.X_BIG

        missing_ws = 7 - len(value)
        if missing_ws <= 0:
            ws_left = 0
            ws_right = 0
        else:
            ws_left = missing_ws // 2
            ws_right = ws_left + (missing_ws % 2)
        return "[{3}{1}{0}{2}{4}]".format(value, " " * ws_left, " " * ws_right, start_c, ColourLookup.ENDC)

    def empty(self):
        return self.v == 0

    def __eq__(self, other):
        return (self.v == other.v) & self.can_sum & other.can_sum & (not self.empty())

    def double(self):
        self.v *= 2
        self.can_sum = False
        return self

    def reset(self):
        self.can_sum = True

    def copy(self):
        return Cell(self.v)


# The main class to import vv
# Use move to make a move with a direction signified by an integer, 0, 1, 2 or 3 (couldn't be bothered to make pretty)
# use game_over to check if you have failed
# use highest_tile to check if you have reached 2048
# copy might be useful ;)
# define your own value function - if you want to!
# you can print a game straight to console as a pretty string i.e. print(my_game)
# you can reference positions with [] like: my_game[x, y] (indices start at 1 because I'm terrible)
class Game:
    def __add_random(self):
        if randint(1, 10) == 1:
            to_add = 4
        else:
            to_add = 2

        possible_locations = []
        for xy, value in self.values.items():
            if value.empty():
                possible_locations.append(xy)

        selected_location = choice(possible_locations)
        self.values[selected_location] = Cell(to_add)

    def __init__(self, t = False, vs = None):
        self.test = t
        if vs is None:
            self.values = {(x, y): Cell(0) for x in range(1, 5) for y in range(1, 5)}
            self.__add_random()
            self.__add_random()
        else:
            self.values = {key: value.copy() for key, value in vs.items()}

    def copy(self):
        return Game(self.test, self.values)

    def move(self, direction):
        for c in self.values.values():
            c.reset()

        if direction < 2:
            adjustment = 1
            prime_range = range(1, 4)
        else:
            adjustment = -1
            prime_range = range(4, 1, -1)
        if direction % 2 == 0:
            y_axis = False
        else:
            y_axis = True

        other_range = range(1, 5)

        checks = [((o, p), (o, p + adjustment)) for o in other_range for p in prime_range]
        if not y_axis:
            checks = [(xy[::-1], xy_ac[::-1]) for xy, xy_ac in checks]

        loop_changed = True
        move_changed = False

        while loop_changed:
            loop_changed = False
            for xy, xy_ac in checks:
                if self.values[xy_ac].empty() and not self.values[xy].empty():
                    self.values[xy_ac] = self.values[xy]
                    self.values[xy] = Cell(0)
                    loop_changed = True
                    move_changed = True
                elif self.values[xy_ac] == self.values[xy]:
                    self.values[xy_ac] = self.values[xy].double()
                    self.values[xy] = Cell(0)
                    loop_changed = True
                    move_changed = True

        if (not self.test) and move_changed:
            self.__add_random()

        return move_changed

    def game_over(self):
        c = self.copy()
        for d in range(0, 4):
            if c.move(d):
                return False
        return True

    def value_function(self):
        if self.game_over():
            return 0
        else:
            return 1  # TODO: Define something more useful here, this just avoids failure

    def highest_tile(self):
        return max([value.v for value in self.values.values()])

    def __str__(self):
        return "\n\n\n\n".join([" ".join([str(self.values[x, y]) for x in range(1, 5)]) for y in range(1, 5)])

    def __getitem__(self, key):
        return self.values[key].v

