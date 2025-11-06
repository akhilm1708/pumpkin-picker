import pygame
import sys
import os
import random

# Initialize pygame and window
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin Picker")
clock = pygame.time.Clock()

class Pumpkin:
    """Class to represent and draw a pumpkin."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        """Draws the pumpkin given its attributes."""
        pygame.draw.circle(surface, pygame.Color(self.color), (int(self.x), int(self.y)), int(self.radius))


class Stem:
    """Class to represent and draw a pumpkin stem."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface):
        """Draws the stem given its attributes."""
        rect = pygame.Rect(0, 0, int(self.width), int(self.height))
        rect.centerx = int(self.x)
        rect.top = int(self.y)
        pygame.draw.rect(surface, pygame.Color("brown"), rect)


pumpkin_colors = ["orange", "darkorange"]


def make_scene():
    pumpkins = []
    stems = []
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    for n in range(5):
        # Pumpkin parameters
        x = center_x + (n - 2) * 200
        y = center_y
        size = 50
        color = random.choice(pumpkin_colors)

        # Draw pumpkin
        stem_height = 30
        stem_width = 15
        # place stem above pumpkin (top y of stem)
        stem_top = y - size - stem_height
        stems.append(Stem(x, stem_top, stem_width, stem_height))

        pumpkins.append(Pumpkin(x, y, size, color))

    return pumpkins, stems

pumpkins, stems = make_scene()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(pygame.Color("black"))

    # draw stems then pumpkins 
    for stem in stems:
        stem.draw(screen)
    for p in pumpkins:
        p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()