class Piece:
    """
    Base class for all pieces.

    Attributes:
        _color (int): The color of the piece. (1 or -1)
        _value (int): The value of the piece.

    Methods:
        get_moves(board, x, y): Returns a list of all possible moves for the piece.
    """

    def __init__(self, color: int, value: float):
        self.color = color
        self.value = value

    @property
    def color(self) -> int:
        """Get piece color"""
        return self._color
    
    @color.setter
    def color(self, color: int) -> None:
        if color not in {1, -1}:
            raise TypeError(
                "The 'color' attribute must be either 1 (white) or -1 (black)\n" + 
                f"Got unexpected value: {color}"
                )
        else:
            self._color = color

    @property
    def value(self) -> float:
        """Get piece value"""
        return self._value
    
    @value.setter
    def value(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(
                "The 'value' attribute must be a float\n" + 
                f"Got unexpected type: {type(value)}"
            )
        else:
            self._value = value


class Pawn(Piece):
    """
    Implementation of the Pawn piece
    """

    def __init__(self, color: int):
        super().__init__(color, 1.0)

class Bishop(Piece):
    """
    Implementation of the Bishop piece
    """

    def __init__(self, color: int):
        super().__init__(color, 3.0)

class Knight(Piece):
    """
    Implementation of the Knight piece
    """

    def __init__(self, color: int):
        super().__init__(color, 3.0)

class Queen(Piece):
    """
    Implementation of the Queen piece
    """

    def __init__(self, color: int):
        super().__init__(color, 9.0)

class Rook(Piece):
    """
    Implementation of the Rook piece

    Attributes:
        _never_moved (int): Records if the piece has moved before (0 or 1)
    """

    def __init__(self, color: int, never_moved: int):
        super().__init__(color, 5.0)
        self.never_moved = never_moved

    @property
    def never_moved(self) -> int:
        """Returns 0 or 1 depending on whether or not piece has moved"""
        return self._never_moved
    
    @never_moved.setter
    def never_moved(self, never_moved: int) -> None:
        if never_moved not in {0, 1}:
            raise TypeError(
                "The 'never_moved' attribute must be either 0 (moved) or 1 (never moved)\n" + 
                f"Got unexpected value: {never_moved}"
            )
        else:
            self._never_moved = never_moved

class King(Piece):
    """
    Implementation of the King piece

    Attributes:
        _never_moved (int): Records if the piece has moved before (0 or 1)
    """

    def __init__(self, color: int, never_moved: int):
        super().__init__(color, 0.0)
        self.never_moved = never_moved

    @property
    def never_moved(self) -> int:
        """Returns 0 or 1 depending on whether or not piece has moved"""
        return self._never_moved
    
    @never_moved.setter
    def never_moved(self, never_moved: int) -> None:
        if never_moved not in {0, 1}:
            raise TypeError(
                "The 'never_moved' attribute must be either 0 (moved) or 1 (never moved)\n" + 
                f"Got unexpected value: {never_moved}"
            )
        else:
            self._never_moved = never_moved
