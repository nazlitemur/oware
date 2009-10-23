import copy
import weakref

# A class to represent one move to be made in the game
# Has to represent both what the move is and and the player making it
# Allows the player to give up by setting is_forfeit() True
#
# Intended to be subclassed for a specific game type
# Override all methods in subclass
class GameMove:
	# Returns an informal string representation (used to print out the move
	#  during gameplay)
	def __str__(self):
		return "Base GameMove object"
	# Returns the player whose move this is
	#  return val is an object whose type is a game-specific subclass of
	#  GamePlayer
	def get_player(self):
		return None
	# Returns the move made
	#  return val is an object whose type is a game-specific subclass of
	#  GameMove
	def get_move(self):
		return None
	# Returns a boolean indicating whether this move is a forfeiture
	#  (useful for human players who want to quit)
	def is_forfeit(self):
		return False

# A class to represent a state in the game
#
# Can use implicit or explicit (external) representation of any game board
# But the latter is up to the implementer of a particular game
#
# Intended to be subclassed for a specific game type
# Override the following methods in a subclass:
#   __str__()
#	repeats()
#	repeated_rep()
#   copy_into()
#   make_copy()
#   clear()
#   is_win()
#   get_players()
#   get_next_player()
#   get_player_state()
#   is_valid_move()
#   move()
#	handle_cycle()
#   successor_moves()
class GameState:
	def __init__(self):
		self.controller = None
	
	# Sets a weak reference to the GameController object which is running
	# the game (weakref because the controller holds a reference to the game
	# state, want to avoid circular references)
	#
	# Having this reference allows us to check legality of certain actions with
	# the controller (like how many times the player is allowed to ask us about
	# successor states)
	def setController(self, controller):
		self.controller = weakref.proxy(controller)
		
	# Override in subclass
	#
	# Must return a printable representation of the game in the state
	# represented by this object, so we can show the game state as it progresses
	def __str__(self):
		return "Base game state object"
		
	# Override in subclass ONLY if game has cycles
	#
	# Returns True if the game can cycle infinitely, False else
	def repeats(self):
		return False
	
	# Override in subclass ONLY if game has cycles
	#
	# Returns a representation of the state which is suitable for hashing
	def repeated_rep(self):
		pass
	
	# Override in subclass
	# Be sure to call this super method to get the controller!
	#
	# "other" is another GameState object
	#
	# Intent is to populate a copy the player can perform game moves on
	# without modifying the original game state held by the controller
	#
	# Not using copy module because it's grumpy about weakref objects
	# TODO: Figure out how to just use copy.deepcopy()?
	def copy_into(self, other):
		other.controller = self.controller
	
	# Override in subclass
	#
	# Actually creates a copy for player experiments without modifying original
	# game state
	#
	# See copy_into() above
	def make_copy(self):
		pass
	
	# Override in subclass
	#
	# Reset to a starting game
	def clear(self):
		pass
	
	# Override in subclass
	#
	# returns True if indicated player has won, False else
	#
	# "player" parameter is a player's game ID
	def is_win(self, player):
		pass
	
	# Override in subclass
	#
	# Returns a list of legal player game IDs
	def get_players(self):
		pass
		
	# Override in subclass
	#
	# Returns the game ID of the player who should move next
	def get_next_player(self):
		pass
	
	# Override in subclass
	#
	# returns a representation of the game state particular to a player
	# which may be a partial or probabilistic picture of the entire game state
	#
	# player is an object whose type is a game-specific subclass of GamePlayer
	def get_player_state(self, player):
		return None
	
	# Override in subclass
	#
	# Returns True if the indicated move is valid on the current state,
	# False otherwise
	#
	# move is an object whose type is a game-specific subclass of GameMove
	def is_valid_move(self, move):
		return False
		
	# Override in subclass
	#
	# Make the indicated move and modify the state accordingly
	# should modify self, return next player
	# or return None if the move is invalid
	#
	# move is an object whose type is a game-specific subclass of GameMove
	def move(self, move):
		pass
	
	# Override in subclass ONLY if the game can cycle.
	#
	# Responsible for handling a cycle situation (e.g., by declaring a draw,
	#  awarding pieces to players, etc.)
	def handle_cycle(self):
		pass
	
	# returns # of expansions the controller will allow for the remainder
	# of the turn
	def expansions_count(self):
		if self.controller == None:
			return None
		else:
			return self.controller.expansions_count()
		
	# Override in subclass
	# be sure to call this super function and return None if it returns None
	# override should return empty list if no moves are possible
	#
	# Generates a list of valid moves to make on the current state
	# Each move is an object whose type is a game-specific subclass of GameMove
	#
	# Returns None if the GameController indicates that we are not allowed to
	# generate any more successors
	def successor_moves(self):
		if self.controller == None or self.controller.successor_generated():
			return []
		else:
			return None
	
	# Like move(), above, but returns a copy of the game state after the
	# indicated move instead of modifying the current state (useful for looking
	# ahead in a minimax tree without destroying the original state)
	#
	# Returns None if the move is invalid
	#
	# move is an object whose type is a game-specific subclass of GameMove
	def move_copy(self, move):
		if not self.is_valid_move(move):
			return None
		r = self.make_copy()
		player = r.move(move)
		return (player, r)
	
	# Returns a valid list of (player, state, move) tuples.  Each one contains
	# a valid move on the current state (obtained with successor_moves() above),
	# a GameState resulting from applying that move (obtained with move_copy()
	# above), and the next player to move.
	#
	# Returns None if the GameController indicates that we are not allowed to
	# generate any more successors, empty list if no moves are possible
	def successors(self):
		moves = self.successor_moves()
		if moves == None:
			return None
		s = map(self.move_copy, moves)
		s = zip([x[0] for x in s], [x[1] for x in s], moves)
		return s
	