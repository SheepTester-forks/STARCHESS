# /* Square.py
from typing import Literal
import pygame

from data.classes.Piece import Piece


# Tile creator
class Square:
    x: int
    y: int
    width: int
    height: int
    abs_x: int
    abs_y: int
    abs_pos: tuple[int, int]
    pos: tuple[int, int]
    color: Literal["light", "dark"]
    draw_color: tuple[int, int, int]
    highlight_color: tuple[int, int, int]
    occupying_piece: Piece | None
    coord: str
    highlight: bool
    rect: pygame.Rect

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (x, y)
        self.color = "light" if (x + y) % 2 == 0 else "dark"
        self.draw_color = (220, 208, 194) if self.color == "light" else (53, 53, 53)
        self.highlight_color = (100, 249, 83) if self.color == "light" else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)

    # get the formal notation of the tile
    def get_coord(self):
        columns = "abcdef"
        return columns[self.x] + str(self.y + 1)

    def draw(self, display):
        # configures if tile should be light or dark or highlighted tile
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)
        # adds the chess piece icons
        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)
