from collections import Counter
from django.urls import reverse
from django.db import models


class Game(models.Model):
    """
    This defines the board state (and metadata) for a tic-tac-toe game.

    The board is modeled a 9 character string:
        'X' or 'O' means the space is played.
        ' ' (space) means the space is empty.

    We also keep track of the time the game was created and last updated,
    just in case we want to add "recent games" or a game list of some form.
 
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    board = models.CharField(max_length=9, default=" " * 9)

    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)

    def __unicode__(self):
        return '{0} vs {1}, state="{2}"'.format(self.player_x, self.player_o, self.board)

    def get_absolute_url(self):
        return reverse('play:detail', kwargs={'pk': self.pk})

    @property
    def next_player(self):
        """
        Returns 'X' if the next play is player X, otherwise 'O'.
        This is easy to calculate based on how many plays have taken place:
        if X has played more than O, it's O's turn; otherwise, X plays.
        """
        # Counter is a useful class that counts objects.
        count = Counter(self.board)
        if count.get('X', 0) > count.get('O', 0):
            return 'O'
        return 'X'
 

    WINNING = [
        [0, 1, 2],  # Across top
        [3, 4, 5],  # Across middle
        [6, 7, 8],  # Across bottom
        [0, 3, 6],  # Down left
        [1, 4, 7],  # Down middle
        [2, 5, 8],  # Down right
        [0, 4, 8],  # Diagonal ltr
        [2, 4, 6],  # Diagonal rtl
    ]

    @property
    def is_game_over(self):
        """
        If the game is over and there is a winner, returns 'X' or 'O'.
        If the game is a stalemate, it returns ' ' (space)
        If the game isn't over, it returns None. 
        """
        board = list(self.board)
        for wins in self.WINNING:
            # Create a tuple
            w = (board[wins[0]], board[wins[1]], board[wins[2]])
            if w == ('X', 'X', 'X'):
                return 'X'
            if w == ('O', 'O', 'O'):
                return 'O'
        # Check for stalemate
        if ' ' in board:
            return None
        return ' '

    def play(self, index):
        """
        Plays a square specified by ``index``.
        The player to play is implied by the board state.

        If the play is invalid, it raises a ValueError.
        """
        if index < 0 or index >= 9:
            raise IndexError("Invalid board index")

        if self.board[index] != ' ':
            raise ValueError("Square already played")

        # One downside of storing the board state as a string
        # is that you can't mutate it in place.
        board = list(self.board)
        board[index] = self.next_player
        self.board = u''.join(board)
