import game_state
import game_player
import oware
import os

class OwarePlayer(game_player.GamePlayer):
	# Make a note of our name (will be the module name)
	# and player ID (will be a valid player ID for an OwareState).
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
	
	# EXAMPLE: Loads a file from the same directory this module is stored in
	#  and returns its contents.  Pattern any file operations you do in your
	#  player on this model.
	#
	# NB: Make a note of the working directory before you cd to the module
	#  directory, and restore it afterward!  The rest of the program may break
	#  otherwise.
	def load_file(self, fname):
		wd = os.getcwd()
		os.chdir("players/oware")
		fin = open(fname)
		contents = fin.read()
		fin.close()
		os.chdir(wd)
		return contents
	
	# IMPLEMENT ME!
	def evaluate(self, state):
		pass
	
	# IMPLEMENT ME!
	def minimax_move(self, state):
		pass
	
	# IMPLEMENT ME!
	def alpha_beta_move(self, state):
		pass
	
	# IMPLEMENT ME!
	def tournament_move(self, state):
		pass
