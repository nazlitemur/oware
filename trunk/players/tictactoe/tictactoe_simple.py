import game_state
import game_player
import tictactoe


# A ludicrously stupid TicTacToePlayer agent.
class TicTacToePlayer(game_player.GamePlayer):

	# Make a note of our name and player ID
	# see comments on GamePlayer for more details
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# This agent doesn't evaluate states, so just return 0
	#
	# "state" is a TicTacToeState object
	def evaluate(self, state):
		return 0
	
	# Don't perform any game-tree expansions, just pick the first move
	# that's available in the list of successors.
	#
	# "state" is still a TicTacToeState object
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
