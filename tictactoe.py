import game_state
import game_player

# Subclass of GameMove representing one move by one player in a
# tic-tac-toe class
class TicTacToeMove(game_state.GameMove):
	# player: a TicTacToePlayer object representing the player making the
	#  move
	# move: a number representing the square being moved to
	# forfeit: a boolean which is True only if the player wishes to give up
	def __init__(self, player, move, forfeit=False):
		self.move = move
		self.player = player
		self.forfeit = forfeit
	
	# Returns an informal string representation for printing
	def __str__(self):
		# Tell us which player moves where
		return "Player %.1s moves to square %s" \
			% (TicTacToeState.val_to_char(self.player), \
				str(self.move+1) if self.move != None else "(None)")
	
	# Returns the TicTacToePlayer object who's moving
	def get_player(self):
		return self.player
	
	# Returns the number indicating the square being moved to
	def get_move(self):
		return self.move
	
	# Returns True if the player gives up
	# False else
	def is_forfeit(self):
		return self.forfeit

# Subclass of GameState representing a (past, current, future) state in
#  a game of tic-tac-toe
class TicTacToeState(game_state.GameState):
	X = 1
	O = 2
	EMPTY = -1
	
	# A class method that gives you a character value for a player ID
	# (useful for building a string representation of a player or a board)
	@classmethod
	def val_to_char(cls, x):
		if x == TicTacToeState.X:
			return 'X'
		elif x == TicTacToeState.O:
			return 'O'
		else:
			return ' '
	
	# Just clears the board and initializes it for playing
	# Player X goes first
	def __init__(self):
		self.clear()
	
	# Returns an informal string representation of the board
	# useful for printing the board before every move
	def __str__(self):
		s = "%.1s | %.1s | %.1s\n"\
				"---------\n"\
				 "%.1s | %.1s | %.1s\n"\
				 "---------\n"\
				 "%.1s | %.1s | %.1s\n" % \
				 tuple(map(TicTacToeState.val_to_char, self.board))
		return s
		
	# Clears the board and sets X as the next player
	def clear(self):
		self.board = [TicTacToeState.EMPTY for x in range(9)]
		self.player = TicTacToeState.X;
	
	# returns a list of valid positions on the board
	def board_positions(self):
		return range(9)
	
	# returns the value at the indicated board position
	#
	# "pos" should be one of the values returned by board_positions()
	# (i.e., 0-8)
	def board_value(self, pos):
		return self.board[pos]
	
	# copies relevant information into another state object
	#
	# "other" is the TicTacToeState object to be copied into
	# Warning: destroys data in "other"
	def copy_into(self, other):
		game_state.GameState.copy_into(self, other)
		other.player = self.player
		other.board = [x for x in self.board]
	
	# Returns a TicTacToeState object, functionally identical to this one,
	# which may be modified without modifying this state object's internals
	def make_copy(self):
		r = TicTacToeState()
		self.copy_into(r)
		return r
	
	# Returns a list of valid player IDs
	def get_players(self):
		return [TicTacToeState.X, TicTacToeState.O]
	
	# Returns the player who should play next
	def get_next_player(self):
		return self.player
	
	# Returns a state representation specific to the indicated player
	# For tic-tac-toe that's just a copy of this state obtained with
	# make_copy() above.
	#
	# "player" is a valid player ID returned by get_players()
	# (i.e., 1 or 2)
	def get_player_state(self, player):
		return self.make_copy()
	
	# Returns True if this state represents a win for the indicated player
	# False else
	#
	# "player" is a valid player ID returned by get_players()
	def is_win(self, player):
		if self.board[0] == self.board[4] == self.board[8] == player:
			return True
		if self.board[6] == self.board[4] == self.board[2] == player:
			return True
		for i in range(3):
			if self.board[3*i] == self.board[(3*i)+1] == self.board[(3*i)+2] \
					== player:
				return True
			if self.board[i] == self.board[i+3] == self.board[i+6] == player:
				return True
		return False
	
	# Returns true if the indicated move is valid on this state
	#
	# "move" is a TicTacToeMove object
	def is_valid_move(self, move):
		return move.get_player() == self.player and \
					self.board[move.get_move()] == TicTacToeState.EMPTY
	
	# Destructively modifies this state object by performing the indicated
	# move (if valid).
	#
	# Returns the player ID of the player who should play next, or None
	# if the move was invalid.
	#
	# "move" is a TicTacToeMove object
	def move(self, move, clearRepeats=False):
		if not self.is_valid_move(move):
			return None
		self.board[move.get_move()] = move.get_player()
		self.player = (self.player % 2) + 1
		return self.player
	
	# Returns a list of the valid moves which may be performed on this state,
	# or None if the game controller refuses to allow any more expansions
	# this turn.
	#
	# If the return value is an empty list, there are no valid moves to be
	# made on this state.
	#
	# Each move in the list is a TicTacToeMove object.
	def successor_moves(self):
		moves = game_state.GameState.successor_moves(self)
		if(moves == None):
			return None
		for i in range(9):
			move = TicTacToeMove(self.player, i)
			if(self.is_valid_move(move)):
				moves.append(move)
		return moves