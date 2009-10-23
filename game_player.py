# Represent/contains the logic for an individual player in a game
#
# Intended to be subclassed for a particular game type
# Override the following methods in a subclass:
#   evaluate()
#   minimax_move()
#   alpha_beta_move()
#   tournament_move()
class GamePlayer:
	# "name" is a string identifier for the player (the default game framework
	# value is the module name)
	#
	# "game_id" is a game-type-specific identifier for the player (e.g., 1 for
	# player 1)
	def __init__(self, name, game_id):
		self.name = name
		self.game_id = game_id
		
	def get_name(self):
		return self.name
	
	def get_game_id(self):
		return self.game_id
	
	# Override in subclass!
	#
	# Gives an evaluation value for a game state
	#
	# "state" is an object whose type is a game-specific subclass of GameState
	def evaluate(self, state):
		pass
	
	# Override in subclass!
	#
	# Returns a move object of a game-type-specific GameMove subclass
	# representing the move the player will make from the indicated
	# state
	#
	# "state" is an object whose type is a game-specific subclass of GameState
	def minimax_move(self, state):
		pass
	
	# Override in subclass!
	#
	# Does the same thing as minimax_move() but with alpha-beta pruning.
	def alpha_beta_move(self, state):
		pass
		
	# Override in subclass!
	#
	# Calls minimax_move() or alpha_beta_move()
	#
	# Or, performs special behavior if you like
	def tournament_move(self, state):
		pass