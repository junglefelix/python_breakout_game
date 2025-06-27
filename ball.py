import pygame
import random

class Ball:
    def __init__(self, x, y, dx, dy, size, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.color = color

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.size, self.size))

    def bounce_horizontal(self):
        self.dx = -self.dx

    def bounce_vertical(self):
        self.dy = -self.dy

    def randomize_color(self, color_map):
        self.color = random.choice([color for name, color in color_map.items() if name != "BLACK"])