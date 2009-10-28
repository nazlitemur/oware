import copy
import os
import sys
import traceback

# An exception which is raised if the player objects provided to the 
# GameController constructor don't line up with the GameState subclass's
# player IDs.
class PlayerException(Exception):
	# "player" is a representation of the missing player
	def __init__(self, player):
		self.player = player
	def __str__(self):
		return "Player not found %s" % repr(self.player)

# The central controller for a single game of (whatever).
class GameController:
	# The game function to be used - minimax, alpha-beta, or tournament?
	MINIMAX = 0
	ALPHA_BETA = 1
	TOURN = 2

	# does initial setup of a game
	#
	# "state" is an object whose type is a game-specific subclass of GameState
	# "players" is a list of objects whose type is a game-specific subclass
	#   of GamePlayer
	# Each of the players should return a valid game ID when get_game_id() is
	#   is called, and all game IDs should have a corresponding player.
	# "maxExpansions" is the maximum number of expansions each player is allowed
	#   per turn.
	# "wd" is the working directory that should be restored after each player
	#   takes a turn.  (In case some player changes the wd and doesn't restore)
	#
	# Raises PlayerException if there's a mismatch between players and gameIDs
	def __init__(self, state, players, fns, max_expansions, wd):
		# Reference and ready the game state
		self.state = state
		self.state.clear()
		self.state.setController(self)
		
		# If game cycles, need state repetition detection
		self.visitedStates = set()
		
		# Maps players' game IDs to player objects
		self.players = {}
		
		# Grab the ID of the next player
		self.nextPlayer = state.get_next_player()
		
		# Make a note of number of remaining expansions
		self.max_expansions = max_expansions
		self.expansions = self.max_expansions
		
		# Note the wd in case players open files
		self.wd = wd
		
		# Insert players into map
		self.set_players(players, fns)
	
	# only called by self.state
	# lets the state know how many more expansions it has
	def expansions_count(self):
		return self.expansions
		
	# only called by self.state
	# decreases the available expansions on this turn by 1
	def successor_generated(self):
		if self.expansions <= 0:
			return False
		self.expansions -= 1
		return True
	
	# only called by self and self.state
	#
	# "state" is a game-specific subclass of GameState
	#
	# Returns True if game cycles and state has been visited before
	# Returns False else
	def is_repeat(self, state):
		if not self.state.repeats():
			return False
		return state.repeated_rep() in self.visitedStates
	
	# only called by self and self.state
	#
	# If game cycles, clears our repeated-state history.
	def clear_repeat(self):
		self.visitedStates.clear()
	
	# Sets up player objects corresponding to game IDs
	# 
	# "players" is a list of objects whose type is a game-specific subclass
	#   of GamePlayer
	#
	# Raises PlayerException if there's a mismatch between players and gameIDs
	def set_players(self, players, fns):
		self.players.clear()
		playersFns = zip(players,fns)
		# Insert player IDs, objects into map
		for p in self.state.get_players():
			for v,m in playersFns:
				if v.get_game_id() == p:
					self.players[p] = (v,m)
					break
			if p not in self.players:
				raise PlayerException(p)
	
	# Reset the game
	def reset(self):
		self.clear_repeat()
		self.state.clear()
		self.nextPlayer = self.state.get_next_player()
	
	# Make one move (actually one ply) within the game
	# Returns a tuple (move, winner)
	# move is an object whose type is a subclass of GameMove
	# winner is the game ID of the winning player
	#
	# if move is None, there was no move made
	# if winner is None, nobody has won yet
	# if both are None, the game is over and is a draw.
	#
	# fn is an integer, one of MINIMAX, ALPHA_BETA, or TOURN,
	# indicating which of the players' move functions we should use.
	def game_move(self):
		# make a note of the player who isn't playing
		for x in self.players.keys():
			if x != self.nextPlayer:
				otherPlayer = x
				break
		
		
		# If there are no remaining moves for this player, either the other
		# player has won or it's a draw
		self.expansions = 1
		if len(self.state.successors()) == 0:
			if self.state.is_win(otherPlayer):
				return (None, otherPlayer)
			else:
				# None, None for a draw
				return (None, None)
			
		# allow the player max_expansions for this turn
		self.expansions = self.max_expansions
		
		# are we using alpha-beta, minimax, or tournament?
		fn = self.players[self.nextPlayer][1]
		if fn == GameController.MINIMAX:
			move_fun = self.players[self.nextPlayer][0].minimax_move
		elif fn == GameController.ALPHA_BETA:
			move_fun = self.players[self.nextPlayer][0].alpha_beta_move
		elif fn == GameController.TOURN:
			move_fun = self.players[self.nextPlayer][0].tournament_move
		else:
			move_fun = None
		move = None
		lastPlayer = None
		
		# player may throw an exception
		try:
			# get player's move, make sure we don't modify the current state
			move = move_fun(self.state.get_player_state(self.nextPlayer))
			# player may give up
			if move.is_forfeit():
				print "Player", self.nextPlayer, "forfeits."
				return (move, otherPlayer)
			# player may return illegal move
			if not self.state.is_valid_move(move):
				print "Illegal move returned by player", self.nextPlayer, \
						"(", self.players[self.nextPlayer][0].get_name(), ")"
				return (move, otherPlayer)
			# this player is now last player
			lastPlayer = self.nextPlayer
			# get the new next player and make the indicated move
			self.nextPlayer = self.state.move(move, True)
		except:
			print "Exception thrown by player", self.nextPlayer, \
						"(", self.players[self.nextPlayer][0].get_name(), ")"
			print
			traceback.print_exc()
			print
			return (None, otherPlayer)
		
		os.chdir(self.wd)
		
		# may be a repeated state IF the game cycles
		if self.is_repeat(self.state):
			self.state.handle_cycle()
		# otherwise, if the game cycles, note that we've been here
		elif self.state.repeats():
			self.visitedStates.add(self.state.repeated_rep())
		
		# player may have won
		if self.state.is_win(lastPlayer):
			return (move, lastPlayer)
		
		# nobody's won or lost yet
		return (move, None)
	
	# returns a winner, or None if a draw
	def play_game(self, quiet=False):
		# Just loop until everything's done
		winner = None
		while(winner == None):
			if not quiet:
				print self.state
			move, winner = self.game_move()
			if move == None and winner == None:
				return None
			if move != None and not quiet:
				print "%s:" % self.players[move.get_player()][0].get_name(), \
									move
				print 
		if not quiet:
			print self.state
		return winner
		
