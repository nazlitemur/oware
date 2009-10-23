------------------------------------------------------------------
SHORT VERSION

There's a lot of information in this README.  You should read all of it.
However, here's the quick version so you can keep track of it all.

-Game framework is defined in files named game*.py in the top directory.
-Invoke the program with "./game.py" or "python game.py".  Use the -h switch for
	help.
-Game names you can give the program are "TicTacToe" and "Oware" (NB: case-
	sensitive!).  "TicTacToe" is an example, "Oware" is what you're working on.
-Game logic definitions are in tictactoe.py and oware.py in the top directory.
-Game players are in players/GAME_NAME/ subdirectories.
-WHAT YOU HAVE TO DO:
	-Rename players/oware/username.py to have your username instead of
		"username" (e.g., Mark's is "mw54.py").
	-Implement the minimax_move() method in the OwarePlayer class in the file
		with your username.  See "hw4.txt" for details.
	-Implement the alpha_beta_move() method in the OwarePlayer class in the
		file with your username.  See "hw4.txt" for details.
	-Implement the tournament_move() method in the OwarePlayer class in the
		file with your username.  See "hw4.txt" for details.
	-Answer the written questions from "hw4.txt" and put your answers in a
		text file with your username (e.g., "mw54.txt").
	-Upload the Python file and the text file with your username to OnCourse.
-WHAT YOU MAY DO:
	-You may wish to define additional modules.  These files MUST go in the
		players/oware/ subdirectory and MUST have names starting with your
		username (e.g., "mw54_aux.py").  Make sure you upload these files to
		OnCourse.
	-Clever stuff in your tournament_move() might require external files
		(e.g., to contain databases of endgame moves).  These files MUST go
		in the players/oware/ subdirectory (see players/oware/username.py for
		an example of how to load a file in that location) and MUST have names
		starting with your username (e.g., "mw54_endgame_db.txt").  Do not
		give files which are not Python files the .py extension, please.  Make
		sure you upload these files to OnCourse.
-WHAT YOU MAY NOT DO:
	-Modify the game*.py framework files or the oware.py game definition file.
		When grading we will use the canonical versions of these files and any
		changes you make will not be in effect.

------------------------------------------------------------------
INVOKING THE GAME SYSTEM

On UNIX systems, the file "game.py" is executable, meaning you can do:
./game.py
at the command line.  I will use this convention for invocation as it is
shorter.

On Windows systems, this will likely need to be:
python game.py
at the command line.

At any time, you can do:
./game.py -h
for help.

There are two modes for the game system:  Regular play, and tournament.  In
regular-play mode, you provide the program with the name of a game and two
player modules, and the system will run a single game between them, showing
each move, and at the end display the results and ask if you would like to play
again.  The game name must be capitalized correctly and depends on the specific
implementation, so consult the programmer or look in the game-specific scripts.
Player modules are specified by the names of their files, without extensions.
See below in this README for information about invoking specific games included
in the package.
Regular play is invoked with:
./game.py [options] GAME PLAYER1 PLAYER2

In tournament mode, you provide the program with the name of a game, and the
system will find as many compatible player modules as it can.  Then it will
play every player against every other player, once as the first player in the
game and once as the second.  It will print the outcomes of each game as
the tournament progresses, and at the end it will display the number of games
won by each player.  Tournament play is invoked with:
./game.py -t [options] GAME

In regular-play mode, you have a number of options:
-m or --minimax calls the players' minimax search functions, which is the
	default behavior.
-a or --alpha-beta calls the players' alpha-beta pruning search functions.
	-m and -a are incompatible, for obvious reasons.
-e or --max-expand MAX_EXPAND allows each player MAX_EXPAND expansions of the
	game state during each turn's search.  Obviously, MAX_EXPAND should be
	an integer value.

In tournament mode, you also have some options:
-e or --max-expand MAX EXPAND works exactly as for regular play.
-v or --verbose causes the system to output every game state as play progresses,
	just like it does in regular play.
-x or --exclude PLAYER excludes a specific player module from tournament play.
	This is useful if we wish to leave out a human-interactive player or a
	malfunctioning module from a computer tournament.

------------------------------------------------------------------
GENERIC REMARKS ABOUT THE FRAMEWORK AND ITS STRUCTURE

Students:  This section contains information which may be of interest to you
as well as to anyone who uses this framework to implement other games in the
future.  However, you should read the next section of this file for specific
instructions about this assignment, including where to write code and how to
name your files.

The Python files contained with this README provide a generic game-playing
template program for two-player games, as well as the definitions for the
specific game for this semester.

The following four files define pieces of the basic game-playing framework.
STUDENTS SHOULD NOT MODIFY THESE FILES and this overview is presented merely
for your understanding of the framework.

-game_state.py -- This file defines two base classes.  Both of these classes
	are intended to be subclassed for specific games, as we shall see shortly.
	Files containing subclasses for game_state.py should be kept in the same
	directory and follow strict naming conventions which will be described
	later.
	-GameMove -- an object of this type represents one move to be made in a game
	-GameState -- an object of this type represents one state (i.e., board
		position) in a game.  The logic of game rules is also implicitly coded
		into this class via methods such as move(), is_valid_move(),
		successors(), etc.
		
-game_player.py -- This file defines one base class, GamePlayer.  An object of
	this type represents one player in a game and defines that player's logic
	for gameplay.  This class is intended to be subclassed for specific games.
	Files containing subclasses for game_player.py should be kept in the
	players/ subdirectory tree and follow strict naming conventions which will
	be described shortly.

-game_controller.py -- This file defines one class, GameController, and one
	exception which is thrown by it in unusual circumstances.  GameController
	handles the logic of playing ONE game between TWO SPECIFIC player objects.
	GameController is intended to operate generically on superclass instances
	(GameState, GameMove, GamePlayer) and should not need to be subclassed.

-game.py -- This is the "main" file of the program.  It handles command-line
	options, imports and creates the relevant game and player classes, and runs
	games or tournaments using GameController.  This file contains no class
	definitions and should not need to be modified.
	
There are important rules for writing extensions to the framework for specific
games.  Some of these have to do with details of implementation, such as which
methods to override and what they do;  these are covered by the comments in the
above files.  Other rules capture how the extensions should be named and where
their module files should be placed.

RULE 1:  Pick a Python-compatible name (for instance, TicTacToe) for your game.
RULE 2:  Your three subclasses should be named with the name you picked in rule
	1, with the suffixes -Move, -State, and -Player.  For instance,
	TicTacToeMove, TicTacToeState, and TicTacToePlayer, corresponding to
	GameMove, GameState, and GamePlayer.
RULE 3:  Your -Move and -State subclasses should reside in a file in the top-
	level directory of the package, along with game_state.py,
	game_controller.py, game_player.py, and game.py.  This file's name should
	be the name you picked in rule 1, but lowercase.  For instance,
	tictactoe.py.
RULE 4:  Your -Player subclasses should reside in a subdirectory of the
	players/ directory.  This subdirectory's name should be the name you picked
	in rule 1, but lowercase.  You may have as many -Player subclasses as you
	like, but each one should have this name and reside alone in a file with a
	different name (STUDENTS: see rules about naming your submissions at the
	end of this file!).  For instance, tictactoe_simple.py and tictactoe_adv.py
	are both located in the players/tictactoe/ directory.
	
	
In addition to the framework, one simple but complete implementation of an
EXAMPLE game is presented so you can see a simple use of the framework and also
get an idea how to implement your own player agents.  NOTE:  Again, this game
(Tic-tac-toe) is presented as an EXAMPLE and is NOT the game you will be working
on for the assignment.

-tictactoe.py -- This file defines subclasses of GameMove and GameState
	to represent moves and states in a game of tic-tac-toe (aka noughts and
	crosses -- see http://en.wikipedia.org/wiki/Tic-tac-toe).  The complete
	logic of tic-tac-toe is encapsulated in TicTacToeState's methods.
	
-players/tictactoe/tictactoe_simple.py -- This file defines an incredibly simple
	Tic-tac-toe playing agent -- all it does is request a list of successor
	moves from the current state of the game and pick the first one.  Obviously,
	this is not a very good approach to the game.
	
-players/tictactoe/tictactoe_human.py -- This file defines a Tic-tac-toe playing
	agent which asks a human player for input.  This allows you, the human,
	to play against one of the computer opponents.
	
-players/tictactoe/tictactoe_adv.py -- This file defines a smarter computerized
	Tic-tac-toe agent.  It has an evaluation function which treats the player
	using X as MAX and the player using O as min, and it can perform minimax
	and alpha-beta pruning searches through the game tree using the game-logic
	methods of the game-state objects.  Your player agent for the assignment
	game (below) should be loosely modeled on these lines.

Tic-tac-toe is invoked on the command line by passing the game name "TicTacToe"
to the game.py script, along with two of "tictactoe_simple", "tictactoe_adv",
and "tictactoe_human" for the player names.

e.g.:
./game.py TicTacToe tictactoe_simple tictactoe_adv
./game.py -a -e 45 TicTacToe tictactoe_adv tictactoe_human
./game.py -t -v -x tictactoe_human TicTacToe


---------------------------------------------------------------------
ASSIGNMENT-SPECIFIC INSTRUCTIONS FOR STUDENTS

Finally, the package contains an implementation of the game you will be working
on for the assignment.  This semester we are using the Oware variant of the
popular sowing-stones game, Mancala.  The definition of the game --
representation of its states, moves, and logic -- is contained in the file
oware.py, which provides Oware-specific subclasses of GameMove and GameState.
A list of the rules we are using is provided below.

A questionably-intelligent Oware agent, using the same "pick-the-first-
successor" strategy as the simple Tic-tac-toe agent above, is in
players/oware/oware_simple.py.  A human-interactive agent, which will ask a
human player for input, resides in players/oware/oware_human.py.

Finally, and importantly, an incomplete Oware agent resides in
players/oware/username.py.  RENAME THIS FILE TO HAVE YOUR IU USERNAME.  For
instance, Mark's username is "mw54", so his Oware agent would be in the file
players/oware/mw54.py.

Follow the instructions in hw4.txt to complete the Oware agent and answer the
written questions.  When searching the game tree, you may call the OwareState
object's successors() method to get a list of tuples.  Each tuple will consist
of (player, state, move) values, representing the next player in the game (for
Oware, this is always the opposite player to the one who moved), the state the
game will be in after the move is made, and the move which will lead to that
state.  These will all be legal moves.  Of course, you may call the successors()
method of each of the resulting states to get more moves, but eventually the
game will bar you from expanding any more states (when you hit the maximum
number of expansions per turn, specified at the command line).

Writing external modules for your player is discouraged, but can be done.  The
module should be placed in the players/oware/ directory and given a name
which starts with your username (e.g., "mw54_aux.py").  When you are ready to
submit, simply submit the module file along with your agent file and your
written answers.

If you need to load data from an external data file, place the file in the
players/oware/ directory and give it a name starting with your username
(e.g., "mw54_endgame_db.txt").  There is an example in the incomplete Oware
agent of how to load an external file -- please note, particularly, the process
of saving the working directory, changing directory, using the file, and then
restoring the original working directory.  If you do not restore the original
working directory, the game program will cease to function correctly and
the graders will be unhappy!  Remember to upload your data files along with
your submission.  Your data files should never have .py extensions if they
are not valid Python files.


RULES FOR OWARE
- See an overview of Oware at http://en.wikipedia.org/wiki/Oware
- Specific rules we are using:
	- It is legal to capture all an opponent's stones, or leave an opponent
		without stones, but ONLY if there are no alternatives which leave the
		opponent with stones to play.
	- The game is over as soon as one player has captured >24 stones, or when
		the current player has no moves.
	- When a cycle in the game is detected, the remaining stones are split
		evenly between players.  If the remaining stones are of odd number, the
		last stone is split half-and-half between the players.