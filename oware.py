import game_state
import game_player


# Subclass of GameMove describing a single move in a game of Oware
class OwareMove(game_state.GameMove):
	# Sets the player making the move, the pit being emptied,
	#  and whether the move is a forfeit on creation
	#
	# "player" is a valid player ID for an OwareState
	# "pit" is an integer indicating which of the player's pits to empty (i.e.,
	#   0-5 -- see comments on OwareState)
	# "forfeit" is a boolean, True only if the player wishes to concede
	def __init__(self, player, pit, forfeit=False):
		self.player = player
		self.pit = pit
		self.forfeit = forfeit
		
	# Returns an informal string representation for printing
	def __str__(self):
		# Tell us which player moves where
		return "Player %s moves pit %s" \
			% (self.player, \
				str(self.pit+1) if self.pit != None else "None")
	
	# Returns the player who's making the move
	def get_player(self):
		return self.player
	
	# Returns the pit being moved
	def get_move(self):
		return self.pit
	
	# Returns True if the player gives up, False else
	def is_forfeit(self):
		return self.forfeit
		
		
# Subclass of GameState describing a single game state in a game of Oware
#
# Player IDs are 1,2 -- for any method requiring a valid player ID, use one
#  of the two values returned in a list from get_players()
# Each player has a keep containing captured stones (call get_keep_count()
#  to find out how many)
# Each player has pits, numbered 0-5, containing stones which are in play (call
#  get_pit_count() to find out how many stones in a pit).  Pits are numbered
#  left-to-right from the PLAYER'S point of view -- i.e., the board prints
#  with the following positions, and each player's #5 pit is the one immediately
#  before his/her opponent's #0 pit in the counterclockwise distribution cycle.
#   K 5 4 3 2 1 0		(Player 1)
#     0 1 2 3 4 5 K		(Player 2)
class OwareState(game_state.GameState):
	# On initialization, just clear the board to a starting state
	def __init__(self):
		game_state.GameState.__init__(self)
		self.clear()
	
	# Return an informal string representation for printing the board
	def __str__(self):
		return "%2d  %2d %2d %2d %2d %2d %2d\n"\
				"    %2d %2d %2d %2d %2d %2d  %2d" \
				% (self.keeps[0], self.pits[5], self.pits[4], self.pits[3], \
						self.pits[2], self.pits[1], self.pits[0], \
					self.pits[6], self.pits[7], self.pits[8], self.pits[9], \
						self.pits[10], self.pits[11], self.keeps[1])
	
	# Oware has cycles, so let the GameController know that
	#  repeated-state detection is in effect
	def repeats(self):
		return True
	
	# Returns a hashable representation of the state for repeated-state
	#  detection
	def repeated_rep(self):
		return (self.player, tuple(self.pits))
	
	# Clears the board to a starting state
	def clear(self):
		# The pits are all initially filled with 4 stones
		self.pits = [4] * 12
		# The players' keeps are initially empty
		self.keeps = [0] * 2
		# Player 1 goes first
		self.player = 1
		# If the controller has been initialized, restart its repeated-state
		#  detection
		if self.controller != None:
			self.controller.clear_repeat()
	
	# Copies this board into another OwareState
	def copy_into(self, other):
		# Do the superclass copying
		game_state.GameState.copy_into(self, other)
		# Copy over the pit, keep, next-player values
		other.pits = [x for x in self.pits]
		other.keeps = [x for x in self.keeps]
		other.player = self.player
	
	# Returns an OwareState, containing this state's properties, which can 
	#  safely be modified without modifying this one
	def make_copy(self):
		r = OwareState()
		self.copy_into(r)
		return r
	
	# Returns a list containing valid player ID values for this game
	def get_players(self):
		return [1,2]
	
	# Returns the player ID of the player who should move next
	def get_next_player(self):
	 	return self.player
	
	# Returns the number of stones in the indicated pit
	#
	# "player" is a valid player ID
	# "pit" is a number, 0-5, indicating the desired pit
	def get_pit_count(self, player, pit):
		return self.pits[ (player-1)*6 + pit ]
	
	# Returns the number of stones in the indicated player's keep
	#
	# "player" is a valid player ID
	def get_keep_count(self, player):
		return self.keeps[player-1]
	
	# Returns the pit on which the indicated move will end -- that is,
	# if I move from the indicated pit, which pit will receive the last stone.
	# Ending pit is indicated as a (player, pit) pair as in get_pit_count()
	#
	# player, pit arguments are as in get_pit_count()
	def get_pit_target(self, player, pit):
		pit = pit + (player-1)*6
		# Count the stones in the indicated pit
		stones = self.pits[pit]
		# Get the number of times we'll actually circle the board
		cycles = stones // 12
		# Get the final pit we'll land in
		# NB: Add # of cycles to this, since we have to skip the original pit
		dest = (pit + stones + cycles) % 12
		destPlayer = 1 if dest < 6 else 2
		return (destPlayer, dest % 6)
	
	# Returns a state representation specific to a given player
	#
	# Since the game is fully observable, just returns a copy of this state.
	def get_player_state(self, player):
		return self.make_copy()
	
	# Returns True if the indicated player's pits are all empty
	# False else
	#
	# "player" is a valid player ID
	def is_empty(self, player):
		# Count from the player's lowest pit to his/her highest
		lowerBound = (player-1)*6
		upperBound = player*6
		# If any one contains stones, the player is not empty
		for i in range(12)[lowerBound:upperBound]:
			if self.pits[i] > 0:
				return False
		return True
	
	# Returns True if the board is a win for the indicated player, False else
	#
	# "player" is a valid player ID
	def is_win(self, player):
		if self.keeps[player-1] > 24:
			return True
		if player != self.player or not self.is_empty(player):
			return False
		otherPlayer = (player%2)+1
		return self.is_empty(otherPlayer)
	
	# Returns True if the indicated move would leave the opposing player
	#  with no stones, False else
	#
	# "move" is an OwareMove object
	def kills_opponent(self, move):
		# Get the internal pit number and the opposing player's bounds
		pit = move.get_move() + (move.get_player()-1)*6
		otherPlayer = (move.get_player() % 2) + 1
		lowerBound = (otherPlayer-1)*6
		upperBound = otherPlayer*6
		
		# Count the stones in the indicated pit
		stones = self.pits[pit]
		# Get the number of times we'll actually circle the board
		cycles = stones // 12
		# Get the final pit we'll land in
		# NB: Add # of cycles to this, since we have to skip the original pit
		dest = (pit + stones + cycles) % 12
		
		# If we're landing in our own territory (i.e., outside the opponent's
		#  bounds)
		if dest < lowerBound or dest >= upperBound:
			# If we never made it to opponent's territory (i.e., distance
			#  between starting location and our own upper bound is greater
			#  than the number of stones we have) AND the opponent's pits are
			#  all empty, then the opponent will have no stones
			# Otherwise, the opponent will have stones.
			return stones < move.get_player()*6 - pit \
					and self.is_empty(otherPlayer)
					
		# The number of stones in the target pit will increase by the number
		#  of times we cycle the board + 1
		destCount = self.pits[dest] + cycles + 1
		
		# If that number is 2 or 3, we will capture the opponent's pits
		if destCount == 2 or destCount == 3:
			# If we cycled the board at least once, then all the opponent's pits
			#  above the target pit will have at least one stone
			if cycles > 0 and dest % 6 != 5:
				return False
			# If any of the opponent's pits above the target had stones to
			#  begin with, they're safe and so is the opponent
			for i in range(12)[dest+1:upperBound]:
				if self.pits[i] > 0:
					return False
			# Otherwise, check the opponent's pits below the target
			for i in range(12)[lowerBound:dest]:
				# Each of them will also increase by the number of cycles + 1
				pCount = self.pits[i] + cycles + 1
				# If any of them equals neither 2 nor 3, it's safe and so
				#  is the opponent
				if pCount != 2 and pCount != 3:
					return False
			# If we're capturing and all the above tests fail, the move
			#  deprives the opponent of all his/her stones
			return True
		
		# If we're not capturing, the opponent is safe
		return False
	
	
	# Returns True if the indicated move is valid on this state, False else.
	#
	# "move" is an OwareMove object.
	def is_valid_move(self, move):
		# if it's not the correct player, invalid
		if move.get_player() != self.player:
			return False
		# if it's not a valid pit, invalid
		if move.get_move() < 0 or move.get_move() > 5:
			return False
		pit = move.get_move() + (move.get_player()-1)*6
		# if the indicated pit contains no stones, invalid
		if self.pits[pit] == 0:
			return False
		# if this move would deprive the other player of all stones
		#  and there are moves available which would not, invalid
		if self.kills_opponent(move):
			for i in range(6):
				if i == move.get_move():
					continue
				pit = i + (move.get_player()-1)*6
				if self.pits[pit] > 0 and \
						not self.kills_opponent(OwareMove(move.get_player(),i)):
					return False
		# otherwise, it's a valid move.
		return True
	
	# Deals with a signal from the GameController that this state repeats
	#  one that has been played previously.
	#
	# Our rules for this situation dictate that remaining stones are split
	#  evenly between the players (fractionally if the remaining # of stones is
	#  odd).  This will leave the game in a finalized state.
	def handle_cycle(self):
		sum = 0
		# Count remaining stones
		for i in range(12):
			sum += self.pits[i]
			self.pits[i] = 0
		# Divide remaining stones between players
		self.keeps[0] += float(sum) / 2
		self.keeps[1] += float(sum) / 2
	
	# Performs the indicated move destructively on this state, replacing its
	#  previous values with the new values resulting from the move.
	#
	# "move" is an OwareMove object
	def move(self, move, clearRepeats=False):
		if not self.is_valid_move(move):
			return None
		
		# get stones out of pit
		pit = move.get_move() + (move.get_player()-1)*6
		stones = self.pits[pit]
		self.pits[pit] = 0
		
		# distribute stones
		pitIter = pit
		while stones > 0:
			# increment iterator with wrapping
			pitIter = (pitIter + 1) % 12
			# Skip the original pit
			if pitIter == pit:
				continue
			# increase pit value and decrement stones in hand
			self.pits[pitIter] += 1
			stones -= 1
			
		# if we landed in an opponent's pit and == 2 or == 3, capture
		lowerBound = (self.player-1)*6
		upperBound = self.player*6 - 1
		if (pitIter < lowerBound or pitIter > upperBound) \
				and (self.pits[pitIter] == 2 or self.pits[pitIter] == 3) \
				and self.controller != None:
			# We can wipe the controller's memory of repeated states if we're
			#  capturing
			if clearRepeats:
				self.controller.clear_repeat()
			
		while (pitIter < lowerBound or pitIter > upperBound) \
				and (self.pits[pitIter] == 2 or self.pits[pitIter] == 3):
			# Increase keep count, remove stones from pit, and decrement
			#  iterator with wrapping
			self.keeps[self.player-1] += self.pits[pitIter]
			self.pits[pitIter] = 0
			pitIter = (pitIter - 1) % 12
			
		# switch players
		self.player = (self.player % 2) + 1
		return self.player
		
	# Returns the list of valid successor moves from this state
	#  or None if the controller refuses to allow any more expansions
	#
	# If the list is empty, then there are no valid moves on this state.
	#
	# Each element in the list is an OwareMove object.
	def successor_moves(self):
		moves = game_state.GameState.successor_moves(self)
		if(moves == None):
			return None
		for i in range(6):
			move = OwareMove(self.player, i)
			# first condition saves us looping over all other moves
			#  (in is_valid_move()) to find out if there are non-killing
			#  moves when not necessary
			if (self.get_pit_count(self.player, i) > 0 \
						and not self.kills_opponent(move)) \
					or self.is_valid_move(move):
				moves.append(move)
		return moves