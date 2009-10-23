import game_state
import game_player
import oware

class OwarePlayer(game_player.GamePlayer):
	def __init__(self, name, game_id):
		game_player.GamePlayer.__init__(self, name, game_id)
		
	def minimax_move(self, state):
		# see what the valid moves are so we can check the human's answer
		successors = state.successor_moves()
		successors = [x.get_move() for x in successors]
		
		# Keep looping until the human gives us valid input
		while True:
			# Ask
			s = raw_input("What pit would you like to move (1-6, q to quit)? ")
			# Human wants to quit
			if s == 'q':
				# so return a forfeit move
				return oware.OwareMove(self.game_id, None, True)
			
			# Human may not have input an integer
			try:
				s = int(s)
			except:
				print "Please input an integer 1-6, or q to quit "
				continue
			
			# Human may not have input a value on the board
			if s >= 1 and s <= 6:
				s -= 1
			else:
				print "Please input an integer 1-6, or q to quit "
				continue
			
			# Human may not have input a valid move
			if s not in successors:
				print "That is not a valid move.  Please choose a pit "\
					"containing stones or which does not deprive the opponent "\
					"of moves."
				continue
			
			# Return the valid move
			return oware.OwareMove(self.game_id, s)
			
	def alpha_beta_move(self, state):
		return self.minimax_move(state)
	
	def tournament_move(self, state):
		return self.minimax_move(state)