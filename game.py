#!/usr/bin/env python

import imp
import getopt
import optparse
import os
import sys
import traceback

import game_state
import game_player
import game_controller

MAX_EXPAND = 15
USAGE_STRING = \
"\nUsage 1: %prog [-m | -a] [-e MAX_EXPAND] GAME PLAYER1 PLAYER2\n"\
"Usage 2: %prog -t [-v] [-e MAX_EXPAND] [-x PLAYER] GAME\n\n"\
"GAME specifies the game to be played (see README)\n"\
"PLAYER1, PLAYER2 specify player modules to use for first and second player\n"\
	"\trespectively"
PLAYER_PATH = './players'
GAME_SUFFIX = "State"
PLAYER_SUFFIX = "Player"

# Loads a module with the indicated name from the indicated path.
# Appends the path to sys.path so any imports from that module will be correctly
# handled.
# wd is the working directory that should be restored after the module loads.
#
# Returns the module object, or None if an exception occurs.
def load_module(mName, path, wd):
	f = p = d = mod = None
	if path != '' and path != None and path not in sys.path:
		sys.path.append(path)
	try:
		f,p,d = imp.find_module(mName, None)
		mod = imp.load_module(mName, f, p, d)
	except ImportError, e:
		print "Could not import module", mName
		print e
		return None
	except:
		print "Could not import module", mName, "(unknown error)"
		traceback.print_exc()
		return None
	finally:
		if f != None:
			f.close()
		os.chdir(wd)
	return mod

# Creates an instance of a class of the indicated name, from the indicated
# module.  Optional arguments are passed to class constructor.
#
# Returns the instantiated object, or None if an exception occurs.
def class_instance(mod, name, *args):
	try:
		cl = getattr(mod, name)
		r = cl(*args)
	except AttributeError, e:
		print "Could not get class named", name
		print e
		return None
	except:
		print "Could not get class named", name, "(unknown error)"
		traceback.print_exc()
		return None
	return r
	

# "gameName" is the properly-capitalized name of the GameState subclass
# excluding the trailing ...State (e.g., if we're playing with the
# TicTacToeState, the first arg is TicTacToe)
#
# This class resides in a module file with the same name, only lowercase
# (e.g., tictactoe.py), in this directory or on the path
#
#
# "p1Name" is the name of the first player's module, which is in
# the "players" subdirectory.  This module must contain a player class
# derived from GamePlayer with the name (gameName)Player.
#
# e.g., the simple TicTacToe agent lives in the players/tictactoe_simple.py
# file, which contains the TicTacToePlayer class defining the agent.
# The value of this argument is "tictactoe_simple"
#
#
# "p2Name" is the name of the second player's module, which works exactly
# the same as the first player's (and can in fact be the same module)
#
# "maxExpansions" is the maximum number of game-tree expansions to allow each
# player as they search during one turn.
#
# "alphabeta" is a boolean indicating whether alpha-beta is used or not.
def play_game(gameName, p1Name, p2Name, maxExpansions, alphabeta):
	wd = os.getcwd()
	# Load game, player modules
	gameMod = load_module(gameName.lower(), None, wd)
	p1Mod = load_module(p1Name, os.path.join(PLAYER_PATH, gameName.lower()), wd)
	p2Mod = load_module(p2Name, os.path.join(PLAYER_PATH, gameName.lower()), wd)
	if gameMod == None or p1Mod == None or p2Mod == None:
		sys.exit(2)
	
	# Load game, player classes
	state = class_instance(gameMod, gameName+GAME_SUFFIX)
	if state == None:
		sys.exit(2)
	gameIDs = state.get_players()
	p1 = class_instance(p1Mod, gameName+PLAYER_SUFFIX, p1Name, gameIDs[0])
	p2 = class_instance(p2Mod, gameName+PLAYER_SUFFIX, p2Name, gameIDs[1])
	if p1 == None or p2 == None:
		sys.exit(2)
	
	# Create a game controller
	try:
		gm = game_controller.GameController(state, [p1,p2], maxExpansions, wd)
	except game_controller.PlayerException, e:
		print "Player ID not covered!"
		print e
		sys.exit(3)
		
	# keep playing til user wants to stop
	playOn = True	
	while playOn:
		# Reset the game
		gm.reset()
		# Play the game
		fn = game_controller.GameController.ALPHA_BETA if alphabeta \
				else game_controller.GameController.MINIMAX
		winner = gm.play_game(fn)
		if winner == None:
			print "Game is a draw!"
		else:
			winnerName = None
			if p1.get_game_id() == winner:
				winnerName = p1.get_name()
			else:
				winnerName = p2.get_name()
			print winnerName, "wins!"
		
		# get valid input
		while True:
			p = raw_input("Play again (y/n)? ")
			if p == 'y':
				break
			elif p == 'n':
				playOn = False
				break
			else:
				print "Please input 'y' or 'n'"


# Runs a tournament between all the game players it can find for the indicated
# game.
#
# "gameName" is as for play_game() above.
#
# "exclusions" is a list of strings indicating player modules to leave out
# of the tournament (useful for excluding human-interaction modules)
#
# "maxExpansions" is as for play_game() above.
#
# "quiet" indicates that the program should refrain from outputting each and
# every game state as games are played, if True.
def play_tournament(gameName, exclusions, maxExpansions, quiet):
	wd = os.getcwd()
	
	# Load game module
	gameMod = load_module(gameName.lower(), None, wd)
	if gameMod == None:
		sys.exit(2)
	
	# Instantiate game class & get player IDs
	state = class_instance(gameMod, gameName+GAME_SUFFIX)
	if state == None:
		sys.exit(2)
	playerIDs = state.get_players()
	
	# Get a list of player modules and try to load them
	playerNames = os.listdir(os.path.join(PLAYER_PATH, gameName.lower()))
	playerNames = [x[:-3] for x in playerNames if x.endswith('.py')]
	playerNames = [x for x in playerNames if x not in exclusions]
	playerMods = [load_module(x, \
						os.path.join(PLAYER_PATH, gameName.lower()), wd) \
					for x in playerNames]
	if None in playerMods:
		sys.exit(2)
	
	# Instantiate a player-1 instance and a player-2 instance of every player
	players = [(class_instance(x, gameName+PLAYER_SUFFIX, playerNames[i], \
					playerIDs[0]), \
				class_instance(x, gameName+PLAYER_SUFFIX, playerNames[i], \
					playerIDs[1])) \
				for i,x in enumerate(playerMods)]
				
	# Cut down the name, module lists to successfully-instantiated players
	playerNames = [x for i,x in enumerate(playerNames) \
					if players[i][0] != None and players[i][1] != None]
	playerMods = [x for i,x in enumerate(playerMods) \
					if players[i][0] != None and players[i][1] != None]
	players = [x for x in players if x[0] != None and x[1] != None]
	
	# Player scores are all 0 to begin
	playerScores = [0 for x in players]
	
	# Create a game controller
	try:
		gm = game_controller.GameController(state, \
					[players[0][0],players[1][1]], maxExpansions, wd)
	except game_controller.PlayerException, e:
		print "Player ID not covered!"
		print e
		sys.exit(3)
	
	# Play every player as player 1
	for i, p1 in enumerate(players):
		# Against every other player as player 2
		for j, p2 in enumerate(players):
			if i == j:
				continue
			
			# Reset the game
			gm.reset()
			gm.set_players([p1[0], p2[1]])
			# Play the game using tournament functions
			winner = gm.play_game(game_controller.GameController.TOURN, quiet)
			
			# Output results
			if winner == None:
				print p1[0].get_name(), "vs.", p2[1].get_name(), "is a draw"
				continue
			winnerName = p1[0].get_name() if p1[0].get_game_id() == winner \
							else p2[1].get_name()
			print p1[0].get_name(), "vs.", p2[1].get_name(), "won by", \
							winnerName
			
			# Increment winner's score
			if winner == p1[0].get_game_id():
				playerScores[i] += 1
			else:
				playerScores[j] += 1
	
	# Output final scores of all players
	print
	print "-----------------------------------------"
	print "-----------------------------------------"
	print "Final scores:"
	for i,s in enumerate(playerScores):
		print "Player %s: %d" % (players[i][0].get_name(), s)
	


def main():
	parser = optparse.OptionParser()
	gameName = None
	gameMod = None
	p1Name = None
	p1Mod = None
	p2Name = None
	p2Mod = None
	alphabeta = False
	
	# Set up our option parser
	parser.set_usage(USAGE_STRING)
	parser.add_option("-m", "--minimax", action="store_true", dest="minimax",
		help="Have players use minimax tree search (default).")
	parser.add_option("-a", "--alpha-beta", action="store_true", dest="alphabeta",
		help="Have players use alpha-beta tree search.")
	parser.add_option("-t", "--tournament", action="store_true", dest="tournament",
		help="Run a tournament with all compatible players.")
	parser.add_option("-e", "--max-expand", type="int", dest="maxExpand",
		help="Set the maximum number of expansions per ply (default=%d)" \
			% MAX_EXPAND, metavar="MAX_EXPAND")
	parser.add_option("-x", "--exclude", action="append", dest="exclusions",
		help="Exclude a player from the tournament.  Use multiple --exclude " \
		"to exclude many players.", metavar="PLAYER")
	parser.add_option("-v", "--verbose", action="store_false", dest="quiet",
		help="Print out all the game states in tournament mode.")
	parser.set_defaults(alphabeta=False, minimax=False, tournament=False,
		maxExpand=MAX_EXPAND, exclusions=[], quiet=True)
	
	# Parse the arguments
	opts, args = parser.parse_args()
	
	# Using alpha-beta?
	alphabeta = False
	# Why on earth doesn't optparse handle store_false and store_true to
	#  the same option as mutually exclusive?
	if opts.minimax and opts.alphabeta:
		print "Error: --alpha-beta and --minimax are mutually exclusive."
		sys.exit(1)
	if opts.alphabeta:
		alphabeta = True
	
	# Playing a tournament
	if opts.tournament:
		if len(args) != 1:
			print "Error: Tournament requires 1 argument.  "\
					"Use '-h' for more information."
			sys.exit(1)
		
		# Minimax, alpha-beta options meaningless to tournament play
		if opts.minimax or opts.alphabeta:
			print "Error: Minimax and alpha-beta specifications are "\
					"compatible only with non-tournament play.  Use '-h' "\
					"for more information."
			sys.exit(1)
		
		# Get the game name
		gameName = args[0]
		
		# Run the tournament
		play_tournament(gameName, opts.exclusions, opts.maxExpand, opts.quiet)
		
	# Just playing one player against another
	else:
		# There shouldn't be exclusions
		if len(opts.exclusions) > 0:
			print "Error: Player exclusions are compatible only with "\
					"tournament play.  Use '-h' for more information."
			sys.exit(1)
		
		# There should be three args which are not options
		if len(args) != 3:
			print "Error: Game requires 3 arguments.  "\
					"Use '-h' for more information."
			sys.exit(1)
		
		# Get the game and player names (see comemnts for play_game())
		gameName = args[0]
		p1Name = args[1]
		p2Name = args[2]
		
		print "\nBeginning", gameName, "with players", p1Name, "and", p2Name, \
			"using", "alpha-beta" if alphabeta else "minimax", "planning.\n"
		
		# Go ahead and play
		play_game(gameName, p1Name, p2Name, opts.maxExpand, alphabeta)

if __name__ == "__main__":
	main()
