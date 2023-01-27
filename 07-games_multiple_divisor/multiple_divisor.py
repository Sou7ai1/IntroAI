def can_take(a, b):
    """
        Return True if a player can take a when b was played before
        Note that can_take(a, b) == can_take(b, a)
    """
    return a % b == 0 if a >= b else b % a == 0

def player(stones, last):
    """
        Return one move of the current player
        stones: A list of remaining numbers which have not been taken.
        last: A number taken in the last move.
        The function is expected to return one number which can be taken to win if the position is winning, and False if the position is loosing.

        TODO: Implement this function.
    """
    return False
