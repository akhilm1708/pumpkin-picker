import pygame
import random
import string
import sys
import os

# Initialize pygame and window
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pumpkin Picker")
clock = pygame.time.Clock()

#Adds a background with image "background.jpg"
background_image = pygame.image.load(os.path.join("background.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pumpkin_colors = ["orange", "darkorange"]
#Cite: https://stackoverflow.com/questions/16060899/alphabet-range-in-python
pumpkin_letters = list(string.ascii_uppercase)


class Pumpkin:
    """Class to represent and draw a pumpkin."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.letter = random.choice(pumpkin_letters)

    def draw(self, surface):
        """Draws the pumpkin given its attributes."""
        pygame.draw.circle(surface, pygame.Color(self.color), (int(self.x), int(self.y)), int(self.radius))
    
    def add_letter(self):
        """Draw the pumpkin's stored letter on the pumpkin."""
        font = pygame.font.SysFont(None, int(self.radius))
        text = font.render(self.letter, True, pygame.Color("black"))
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


 
def make_scene():
    """Creates pumpkins and stems for the scene."""
    pumpkins = []
    stems = []
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    for n in range(5):
        # Pumpkin parameters (dimensions, position, color, etc.)
        x = center_x + (n - 2) * 200
        y = center_y
        size = random.randint(40, 60)
        color = random.choice(pumpkin_colors)

        #Stem parameters
        stem_height = 30
        stem_width = 15
        # place stem above pumpkin (top y of stem)
        stem_top = y - size - stem_height

        #Add each stem and pumpkin to their respective lists for drawing later
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
        # draw the already-chosen letter for each pumpkin (remains same)
        p.add_letter()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()