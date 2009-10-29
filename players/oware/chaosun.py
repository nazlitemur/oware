import game_state
import game_player
import oware
import os
import math
import sys

class OwarePlayer(game_player.GamePlayer):
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

  # An evaluation function for Oware
  #
  # Returns the sum of a bunch of feature values time its weight. The weight
  # for a feature may be different for different horizon. Reference:
  # http://users.encs.concordia.ca/~kharma/ResearchWeb/html/research/ayo.html
  #
  # state is a Oware object
  # horizon is the expansion horizon
  def evaluate(self, state):
    # north for north player, south for south player
    north = 1
    south = 2
    pit = state.pits
    # The upper and lower bounds of the north and the south
    n_lowerBound = (north - 1) * 6
    n_upperBound = north * 6
    s_lowerBound = (south - 1) * 6
    s_upperBound = south * 6

    # 1. The number of pits that the south can use to capture 2 seeds
    s_cap_two = 0
    for i in range(12)[s_lowerBound:s_upperBound]:
      target = state.get_pit_target(south, i - 6)
      if target[0] == north and pit[target[1]] == 1:
        s_cap_two += 1

    # 2. The number of pits that the south can use to capture 3 seeds
    s_cap_three = 0
    for i in range(12)[s_lowerBound:s_upperBound]:
      target = state.get_pit_target(south, i - 6)
      if target[0] == north and pit[target[1]] == 2:
        s_cap_three += 1

    # 3. The number of pits that the north can use to capture 2 seeds
    n_cap_two = 0
    for i in range(12)[n_lowerBound:n_upperBound]:
      target = state.get_pit_target(north, i)
      if target[0] == south and pit[target[1] + 6] == 1:
        n_cap_two += 1

    # 4. The number of pits that the north can use to capture 3 seeds
    n_cap_three = 0
    for i in range(12)[n_lowerBound:n_upperBound]:
      target = state.get_pit_target(north, i)
      if target[0] == south and pit[target[1] + 6] == 2:
        n_cap_three += 1

    # 5. The number of pits on the south's side with enough seeds to reach to
    #    the north's side
    s_reach_p = 0
    for i in range(12)[s_lowerBound:s_upperBound]:
      target = state.get_pit_target(south, i - 6)
      if target[0] == north:
        s_reach_p += 1

    # 6. The number of pits on the north's side with enough seeds to reach to
    #    the south's side
    n_reach_o = 0
    for i in range(12)[n_lowerBound:n_upperBound]:
      target = state.get_pit_target(north, i)
      if target[0] == south:
        n_reach_o += 1

    # 7. The number of pits with more than 12 seeds on the south's side
    s_12 = 0
    for i in range(12)[s_lowerBound:s_upperBound]:
      if pit[i] > 12:
        s_12 += 1

    # 8. The number of pits with more than 12 seeds on the north's side
    n_12 = 0
    for i in range(12)[n_lowerBound:n_upperBound]:
      if pit[i] > 12:
        n_12 += 1

    # 9. The current score of the south
    s_keep = state.get_keep_count(south)

    # 10. The current score of the north
    n_keep = state.get_keep_count(north)

    # 11. The number of empty pits on the south's side
    s_empty = 0
    for i in range(12)[s_lowerBound:s_upperBound]:
      if pit[i] == 0:
        s_empty += 1

    # 12. The number of empty pits on the north's side
    n_empty = 0
    for i in range(12)[n_lowerBound:n_upperBound]:
      if pit[i] == 0:
        n_empty += 1

    features = (s_cap_two, s_cap_three, n_cap_two, n_cap_three, s_reach_p, \
                n_reach_o, s_12, n_12, s_keep, n_keep, s_empty, n_empty)

    weights = (-0.50, -1.00, 0.50, 1.00, -0.05, 0.10, -0.20, 0.80, -1.00, 1.00, 0.80, -0.40)

    value = 0
    for i in range(12):
      value += (float)(weights[i]) * features[i]

    return value

  # Does most of the terminal checks for a single step in the search
  #
  # state is a Oware object
  # horizon is steps to the ply horizon
  # players is the list of valid player IDs
  #
  # Returns None if no termination, (value, move) otherwise
  def terminal_checks(self, state, horizon, players):
    # If first player wins, that's a positive
    if state.is_win(players[0]):
      return (sys.maxint, None)
    # If second player wins, that's a negative
    elif state.is_win(players[1]):
      return (-sys.maxint - 1, None)

    # If there are no more expansions allowed, or if
    # we hit the horizon, evaluate
    if state.expansions_count() <= 0 or horizon <= 0:
      return (self.evaluate(state), None)

    # if no termination, return None
    return None

  # minimax_search function. A help function for minimax_move. This one returns
  # a (value, move) tuple that lets us back values up the tree and still return
  # a move at the top.
  #
  # state is an Oware object
  # horizon is an integer representing the distance to the ply horizon
  def minimax_search(self, state, horizon):
    # Get player IDs
    players = state.get_players()

    # Do most of our terminal checks
    term = self.terminal_checks(state, horizon, players)
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
    values = map(lambda x: self.minimax_search(x[1], horizon - 1), successors)
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
  def alpha_beta_search(self, state, horizon, a, b):
    # Get player IDs
    players = state.get_players()
    player = state.get_next_player()

    # Do most of our terminal checks
    term = self.terminal_checks(state, horizon, players)
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
      s_val = self.alpha_beta_search(s[1], horizon - 1, a, b)
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

  # Get the expansion horizon due to current state and the number
  # of nodes for expansion
  #
  # state is an Oware object
  def get_horizon(self, state, strategy):
    # Get the number of nodes for expansion
    exp = state.expansions_count()
    # return int(math.floor(float(exp) / branching_factor))
    if strategy == 1:
      if exp > 3.5:
        return int(math.ceil(math.log(float(exp), 3.5)))
      else:
        return 1
    else:
      if exp >= 6:
        return int(math.ceil(math.log(float(exp), 6.0)))
      else:
        return 1

  # Get a move for the indicated state, using a minimax search
  #
  # state is an Oware object
  def minimax_move(self, state):
    horizon = self.get_horizon(state, 0)
    print "Expansion horizon: ", horizon
    return self.minimax_search(state, horizon)[1]

  # Get a move for the indicated state, using an alpha-beta search
  #
  # state is an Oware object
  def alpha_beta_move(self, state):
    horizon = self.get_horizon(state, 1)
    print "Expansion horizon: ", horizon
    return self.alpha_beta_search(state, horizon, -sys.maxint - 1, sys.maxint)[1]

  # For the first player, use alpha_beta algorithm; for the second one use minimax
  def tournament_move(self, state):
    return self.alpha_beta_move(state)
