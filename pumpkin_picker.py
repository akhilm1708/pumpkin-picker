<<<<<<< Updated upstream
import pygame
import sys
import os
=======
import turtle
# import os
>>>>>>> Stashed changes
import random
import string

# Initialize pygame and window
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin Picker")
clock = pygame.time.Clock()

#Adds a background with image "background.jpg"
background_image = pygame.image.load(os.path.join("background.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


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
    
    def add_letter(self, letter):
        """Adds a letter on the pumpkin."""
        font = pygame.font.SysFont(None, int(self.radius))
        text = font.render(letter, True, pygame.Color("black"))
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)


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

#Cite: https://stackoverflow.com/questions/16060899/alphabet-range-in-python
pumpkin_letters = list(string.ascii_uppercase)

<<<<<<< Updated upstream
=======
    # Draw pumpkin
    pumpkin_body = Pumpkin(x, y, size, color)
    pumpkin_body.draw()

    pumpkin_stem = Stem(x, y + size, size * 0.28, size * 0.36)
    pumpkin_stem.draw()
>>>>>>> Stashed changes

def make_scene():
    """Creates pumpkins and stems for the scene."""
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

    #keeps the background image
    screen.blit(background_image, (0, 0))


    # draw stems then pumpkins 
    for stem in stems:
        stem.draw(screen)
    for p in pumpkins:
        p.draw(screen)
        Letter = random.choice(pumpkin_letters)
        p.add_letter(Letter)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()