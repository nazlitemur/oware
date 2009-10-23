import game_state
import game_player
import oware

# A ludicrously stupid OwarePlayer agent.  You should be able to beat this
#  with no difficulty whatsoever.
class OwarePlayer(game_player.GamePlayer):
	# Make a note of our name (will be the module name)
	# and player ID (will be a valid player ID for an OwareState).
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# This agent doesn't evaluate states, so just return 0
	#
	# "state" is an OwareState object
	def evaluate(self, state):
		return 0
	
	# Don't perform any game-tree expansions, just pick the first move
	# that's available in the list of successors.
	#
	# "state" is still an OwareState object
	def minimax_move(self, state):
		# "successors" is a list of (player, state, move) tuples
		successors = state.successors()
		# Take the first tuple and its third element (i.e., the move)
		return successors[0][2]
	
	# Just call minimax
	def alpha_beta_move(self, state):
		return self.minimax_move(state)
	
	# Just call minimax
	def tournament_move(self, state):
		return self.minimax_move(state)
