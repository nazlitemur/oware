import game_state
import game_player
import oware
import os
import math
import sys

class OwarePlayer(game_player.GamePlayer):
	# The expansion depth of a heuristic is initially 0
	depth = 0

	# Make a note of our name (will be the module name)
	# and player ID (will be a valid player ID for an OwareState).
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)

	# EXAMPLE: Loads a file from the same directory this module is stored in
	# and returns its contents.  Pattern any file operations you do in your
	# player on this model.
	#
	# NB: Make a note of the working directory before you cd to the module
	# directory, and restore it afterward!  The rest of the program may break
	# otherwise.
	def load_file(self, fname):
		wd = os.getcwd()
		os.chdir("players/oware")
		fin = open(fname)
		contents = fin.read()
		fin.close()
		os.chdir(wd)
		return contents

	# Evaluation strategy for expansion depth smaller than 5
	def shallow_evaluate(self, features):
		# Weights for each feature under the shallow evaluation strategy
		weights = (0.06, 0.20, 0.93, 0.93, 0.13, 0.87, 0.06, 0.93, 0.13, 0.60, 1.00, 0.67)
		#features = (o_cap_two, o_cap_three, p_cap_two, p_cap_three, o_reach_p,
		#					   p_reach_o, o_12, p_12, o_keep, p_keep, o_empty, p_empty)
		value = 0
		for i in range(12):
			value += (float)(weights[i]) * features[i]

		return value

	# Evaluation strategy for expansion depth no less than 5
	def deep_evaluate(self, features):
		# Weights for each feature under the deep evaluation strategy
		weights = (0.80, 1.00, 0.06, 0.00, 0.87, 0.60, 0.00, 0.20, 0.73, 0.93, 0.00, 0.80)
		#features = (o_cap_two, o_cap_three, p_cap_two, p_cap_three, o_reach_p,
		#					   p_reach_o, o_12, p_12, o_keep, p_keep, o_empty, p_empty)
		value = 0
		for i in range(12):
			value += (float)(weights[i]) * features[i]

		return value

	# An evaluation function for Oware
	#
	# Returns the sum of a bunch of feature values time its weight. The weight
	# for a feature may be different for different h. Reference:
	# http://users.encs.concordia.ca/~kharma/ResearchWeb/html/research/ayo.html
	#
	# state is a TicTacToeState object
	# depth is the expansion depth
	def evaluate(self, state):
		# player = state.get_next_player()
		# opponent = (player + 1) % 2
		player = 1
		opponent = 2
		pit = state.pits
		# The upper and lower bounds of the player and the opponent
		p_lowerBound = (player - 1) * 6
		p_upperBound = player * 6
		o_lowerBound = (opponent - 1) * 6
		o_upperBound = opponent * 6

		# 1. The number of pits that the opponent can use to capture 2 seeds
		o_cap_two = 0
		for i in range(12)[o_lowerBound:o_upperBound]:
			if pit[(pit[i] + i) % 12] == 1:
				o_cap_two += 1;

		# 2. The number of pits that the opponent can use to capture 3 seeds
		o_cap_three = 0
		for i in range(12)[o_lowerBound:o_upperBound]:
			if pit[(pit[i] + i) % 12] == 2:
				o_cap_three += 1;

		# 3. The number of pits that the player can use to capture 2 seeds
		p_cap_two = 0
		for i in range(12)[p_lowerBound:p_upperBound]:
			if pit[(pit[i] + i) % 12] == 1:
				p_cap_two += 1;

		# 4. The number of pits that the player can use to capture 3 seeds
		p_cap_three = 0
		for i in range(12)[p_lowerBound:p_upperBound]:
			if pit[(pit[i] + i) % 12] == 2:
				p_cap_three += 1;

		# 5. The number of pits on the opponent's side with enough seeds to reach to
		#    the player's side
		o_reach_p = 0
		for i in range(12)[o_lowerBound:o_upperBound]:
			if (pit[i] + i) % 12 >= o_upperBound or (pit[i] + i) % 12 < o_lowerBound:
				o_reach_p += 1;

		# 6. The number of pits on the player's side with enough seeds to reach to
		#    the opponent's side
		p_reach_o = 0
		for i in range(12)[p_lowerBound:p_upperBound]:
			if (pit[i] + i) % 12 >= p_upperBound or (pit[i] + i) % 12 < p_lowerBound:
				p_reach_o += 1;

		# 7. The number of pits with more than 12 seeds on the opponent's side
		o_12 = 0
		for i in range(12)[o_lowerBound:o_upperBound]:
			if pit[i] > 12:
				o_12 += 1;

		# 8. The number of pits with more than 12 seeds on the player's side
		p_12 = 0
		for i in range(12)[p_lowerBound:p_upperBound]:
			if pit[i] > 12:
				p_12 += 1;

		# 9. The current score of the opponent
		o_keep = state.get_keep_count(opponent)

		# 10. The current score of the player
		p_keep = state.get_keep_count(player)

		# 11. The number of empty pits on the opponent's side
		o_empty = 0
		for i in range(12)[o_lowerBound:o_upperBound]:
			if pit[i] == 0:
				o_empty += 1;

		# 12. The number of empty pits on the player's side
		p_empty = 0
		for i in range(12)[p_lowerBound:p_upperBound]:
			if pit[i] == 0:
				p_empty += 1;

		features = (o_cap_two, o_cap_three, p_cap_two, p_cap_three, o_reach_p, \
							  p_reach_o, o_12, p_12, o_keep, p_keep, o_empty, p_empty)

		# Use different strategies for expansion depths above and below 5
		if self.depth <= 4:
			return self.shallow_evaluate(features)
		else:
			return self.deep_evaluate(features)

	# Does most of the terminal checks for a single step in the search
	#
	# state is a Oware object
	# depth is steps to the ply horizon
	# players is the list of valid player IDs
	#
	# Returns None if no termination, (value, move) otherwise
	def terminal_checks(self, state, depth, players):
		# If first player wins, that's a positive
		if state.is_win(players[0]):
			return (sys.maxint, None)
		# If second player wins, that's a negative
		elif state.is_win(players[1]):
			return (-sys.maxint - 1, None)

		# If there are no more expansions allowed, or if
		# we hit the horizon, evaluate
		if state.expansions_count() <= 0 or depth <= 0:
			return (self.evaluate(state), None)

		# if no termination, return None
		return None

	# minimax_search function. A help function for minimax_move. This one returns
	# a (value, move) tuple that lets us back values up the tree and still return
  # a move at the top.
  #
  # state is an Oware object
	# depth is an integer representing the distance to the ply horizon
	def minimax_search(self, state, depth):
		# Get player IDs
		players = state.get_players()

		# Do most of our terminal checks
		term = self.terminal_checks(state, depth, players)
		if term != None:
			return term

		# Get successor states
		# We should check to see if this is None, but since we just
		# checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)

		# Recur on each of the successor states (note we take the state out
		# of the successor tuple with x[1] and decrease the horizon)
		values = map(lambda x: self.minimax_search(x[1], depth - 1), successors)
		# We're not interested in the moves made, just the minimax values
		values = [x[0] for x in values]
		# Look for the best among the returned values
		# Max if we're player 1
		# Min if we're player 2
		if state.get_next_player() == players[0]:
			max_idx = max(enumerate(values), key = lambda x: x[1])[0]
		else:
			max_idx = min(enumerate(values), key = lambda x: x[1])[0]
		# Return the minimax value and corresponding move
		return (values[max_idx], successors[max_idx][2])

	# A helper function for alpha_beta_move().  See minimax_search().
	#
	# a,b are alpha, beta values.
	def alpha_beta_search(self, state, depth, a, b):
		# Get player IDs
		players = state.get_players()
		player = state.get_next_player()

		# Do most of our terminal checks
		term = self.terminal_checks(state, depth, players)
		if term != None:
			return term

		# Get successor states
		# We should check to see if this is None, but since we just
		# checked to see if expansion_count was <= 0, we're safe
		successors = state.successors()
		# If there are no successors and nobody's won, it's a draw
		if len(successors) == 0:
			return (0, None)

		# We start out with a low best-value and no move
		v = -sys.maxint - 1 if player == players[0] else sys.maxint
		m = None
		for s in successors:
			# Recur on the successor state
			s_val = self.alpha_beta_search(s[1], depth - 1, a, b)
			# If our new value is better than our best value, update the best
			# value and the best move
			if (player == players[0] and s_val[0] > v) \
					or (player == players[1] and s_val[0] < v):
				v = s_val[0]
				m = s[2]
			# If we're maxing and exceeding the min above, just return
			# Likewise if we're minning and exceeding the max above
			if (player == players[0] and v >= b) \
					or (player == players[1] and v <= a):
				return (v, m)
			# Update a,b for the next successor
			a = a if player == players[1] else max(a, v)
			b = b if player == players[0] else min(b, v)
		# return the best value, move we found
		return (v, m)

	# Get the expansion depth due to current state and the number
	# of nodes for expansion
	#
	# state is an Oware object
	def get_depth(self, state):
		# Get the number of nodes for expansion
		exp = state.expansions_count()
		# Get successor states
		successors = state.successors()
		# Get the number of successors, or the branching factor
		branching_factor = len(successors)
		# If there are no successors, set depth as 0
		if branching_factor == 0:
			return 0
		# Else, set depth as the number of nodes for expansion divided by
		# the branching factor
		else:
		  return int(math.floor(float(exp) / branching_factor))

	# Get a move for the indicated state, using a minimax search
	#
	# state is an Oware object
	def minimax_move(self, state):
		self.depth = self.get_depth(state)
		print "Expansion depth: ", self.depth
		return self.minimax_search(state, self.depth)[1]

	# Get a move for the indicated state, using an alpha-beta search
	#
	# state is an Oware object
	def alpha_beta_move(self, state):
		self.depth = self.get_depth(state)
		print "Expansion depth: ", self.depth
		return self.alpha_beta_search(state, self.depth, -sys.maxint - 1, sys.maxint)[1]

	# For the first player, use alpha_beta algorithm; for the second one use minimax
	def tournament_move(self, state):
		return self.alpha_beta_move(state)

