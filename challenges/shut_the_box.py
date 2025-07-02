
import random


class ShutTheBox:
    def __init__(self, max_number: int = 9, dice_sides: int = 6, initial_state: str | None = None, last_roll: int = 0):
        if initial_state is None:
            self._state = "1" * max_number
        elif len(initial_state) != max_number:
            raise ValueError(f"Initial state must be of length {max_number}")
        else:
            self._state = initial_state
        if last_roll < 0 or last_roll > dice_sides*2:
            raise ValueError(f"Last roll must be between 0 and {dice_sides*2}")
        self._dice_sides = dice_sides
        self._last_roll = last_roll

    def can_use_one_die(self) -> bool:
        """Check if it's allowable to use only one die based on current game _state."""
        # Get all unflipped numbers (indices + 1 where _state[i] == '1')
        unflipped = [i + 1 for i, chip in enumerate(self._state) if chip == '1']
        
        if not unflipped:
            # All chips are flipped, game is over
            return False
        
        # Find the highest unflipped chip
        max_unflipped = max(unflipped)
        max_single_die_roll = self._dice_sides
        
        # Can use one die if all unflipped chips are <= max single die roll
        return max_unflipped <= max_single_die_roll

    def roll(self, one_die: bool = False) -> int:
        if self._last_roll > 0:
            return self._last_roll
        # Use one die only if one_die is True AND it's allowable
        if one_die and self.can_use_one_die():
            self._last_roll = random.randint(1, self._dice_sides)
        else:
            self._last_roll = random.randint(1, self._dice_sides) + random.randint(1, self._dice_sides)
        return self._last_roll

    def available_moves(self, roll: int) -> list[list[int]]:
        # Get all unflipped numbers (indices + 1 where _state[i] == '1')
        unflipped = [i + 1 for i, chip in enumerate(self._state) if chip == '1']
        
        # Find all combinations that sum to the roll
        valid_moves = []
        
        # Use a recursive helper function to find all combinations
        def find_combinations(target, available, current_combination, start_idx):
            if target == 0:
                # Found a valid combination, add it to results
                valid_moves.append(current_combination[:])
                return
            if target < 0:
                return
            
            for i in range(start_idx, len(available)):
                num = available[i]
                if num <= target:
                    current_combination.append(num)
                    find_combinations(target - num, available, current_combination, i + 1)
                    current_combination.pop()
        
        find_combinations(roll, unflipped, [], 0)
        
        # Return all valid moves
        return valid_moves

    def auto_roll_and_get_available_moves(self, one_die: bool = False) -> list[list[int]]:
        roll = self.roll(one_die=one_die)
        return self.available_moves(roll)
    
    def apply_move(self, move: list[int]):
        if self._last_roll == 0:
            raise ValueError("No roll has been made yet")
        available_moves = self.available_moves(self._last_roll)
        if move not in available_moves:
            raise ValueError(f"Move {move} is not available with roll {self._last_roll}. Available moves: {available_moves}")
        for num in move:
            self._state = self._state[:num-1] + '0' + self._state[num:]
        self._last_roll = 0
    
    def get_state(self) -> str:
        return self._state

    def is_game_over(self) -> bool:
        return all(chip == '0' for chip in self._state)

    def score(self) -> int:
        return sum(int(chip) * (i + 1) for i, chip in enumerate(self._state) if chip == '1')

    def copy(self) -> 'ShutTheBox':
        return ShutTheBox(max_number=len(self._state), dice_sides=self._dice_sides, initial_state=self._state, last_roll=self._last_roll)
    
    def __str__(self) -> str:
        return self._state
    
    def __repr__(self) -> str:
        return f"ShutTheBox(_state={self._state})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ShutTheBox):
            return False
        return self._state == other._state
    
    def __hash__(self) -> int:
        return hash(self._state)


class ShutTheBoxPlayer:
    def __init__(self):
        return
    
    def get_move(self, stb: ShutTheBox) -> list[int] | None:
        available_moves = stb.auto_roll_and_get_available_moves(one_die=True)
        if len(available_moves) == 0:
            return None
        return available_moves[0]
    
    def play_game(self) -> int:
        stb = ShutTheBox()
        while not stb.is_game_over():
            move = self.get_move(stb)
            if move is None:
                break
            stb.apply_move(move)
        return stb.score()
    
    def get_win_rate(self, number_of_games: int = 1_000_000, verbose: bool = False) -> float:
        wins = 0
        for _ in range(number_of_games):
            if self.play_game() == 0:
                wins += 1
            if verbose and (_ % 10_000 == 0) and (_ > 0):
                print(f"Games played: {_}, Win rate: {wins / _}")
        return wins / number_of_games

class RandomPlayer(ShutTheBoxPlayer):
    def __init__(self, one_die: bool = True):
        self._one_die = one_die

    def get_move(self, stb: ShutTheBox) -> list[int] | None:
        available_moves = stb.auto_roll_and_get_available_moves(one_die=self._one_die)
        if len(available_moves) == 0:
            return None
        return random.choice(available_moves)

class SimpleLookaheadPlayer(ShutTheBoxPlayer):
    def __init__(self, one_die: bool = True):
        self._one_die = one_die
        self._max_depth = 3
    
    def get_move(self, stb: ShutTheBox) -> list[int] | None:
        available_moves = stb.auto_roll_and_get_available_moves(one_die=self._one_die)
        if len(available_moves) == 0:
            return None
        n_next_moves = []
        for move in available_moves:
            stb_copy = stb.copy()
            stb_copy.apply_move(move)
            expected_roll = 7
            if stb_copy.can_use_one_die() and self._one_die:
                expected_roll = 4
            next_moves = stb_copy.available_moves(expected_roll)
            n_next_moves.append(len(next_moves))
        return available_moves[n_next_moves.index(max(n_next_moves))]   
    
    
## Testing
#player = ShutTheBoxPlayer()
#print(player.get_win_rate(verbose=True))
# player = RandomPlayer(one_die=False)
# print(player.get_win_rate(verbose=True))
# player = SimpleLookaheadPlayer(one_die=False)
# print(player.get_win_rate(verbose=True))