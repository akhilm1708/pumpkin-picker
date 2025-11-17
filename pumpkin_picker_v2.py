#Version 2.0

# Started with turtle but switched to pygame for better graphics and event handling.
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
pumpkin_letters = list(string.ascii_uppercase)

class Pumpkin:
    """Class to represent and draw a pumpkin."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        #Cite: https://stackoverflow.com/questions/16060899/alphabet-range-in-python
        self.letter = random.choice(pumpkin_letters)
        #
        self.is_falling = False
        self.fall_speed = 5


    def draw(self, surface):
        """Draws the pumpkin given its attributes."""
        pygame.draw.circle(surface, pygame.Color(self.color), (int(self.x), int(self.y)), int(self.radius))
    
    def add_letter(self):
        """Draw the pumpkin's stored letter on the pumpkin."""
        font = pygame.font.SysFont(None, int(self.radius))
        text = font.render(self.letter, True, pygame.Color("black"))
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)
        # pumpkin_letters.remove(self.letter)
    
    def update(self):
        """Updates the pumpkin's position if it is falling."""
        if self.is_falling:
            self.y += self.fall_speed
            # pumpkin_letters.append(self.letter)


class Stem:
    """Class to represent and draw a pumpkin stem."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_falling = False
        self.fall_speed = 5

    def draw(self, surface):
        """Draws the stem given its attributes."""
        rect = pygame.Rect(0, 0, int(self.width), int(self.height))
        rect.centerx = int(self.x)
        rect.top = int(self.y)
        pygame.draw.rect(surface, pygame.Color("brown"), rect)
    
    def update(self):
        """Updates the stem's position if it is falling."""
        if self.is_falling:
            self.y += self.fall_speed


 
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
        elif event.type == pygame.KEYDOWN:
            pressed_char = event.unicode.upper()
            # Check each pumpkin to see if its letter matches the pressed key
            for i, p in enumerate(pumpkins):
                if p.letter == pressed_char and not p.is_falling:
                    p.is_falling = True
                    stems[i].is_falling = True
                    break
        
    for p in pumpkins:
        p.update()
    for stem in stems:
        stem.update()

    #keeps the background image
    screen.blit(background_image, (0, 0))


    # draw stems then pumpkins 
    for stem in stems:
        stem.draw(screen)
    for p in pumpkins:
        p.draw(screen)
        # draw the already-chosen letter for each pumpkin (remains same)
        p.add_letter()

    #Cite: https://www.google.com/search?aep=48&cud=0&ie=UTF-8&q=can+you+show+me+an+example+solution+of+how+to+make+five+pumpkins+appear+on+the+screen%2C+and+making+them+able+to+fall+when+the+corresponding+letter+is+clicked%2C+referencing+the+list+of+pumpkins%3A&qsubts=1763053330009&safe=active&sourceid=chrome&udm=50&mtid=aQ8WaePtHIz40PEPl8Oo6Q4&mstk=AUtExfCZfKv8Moiqmz3M8oCFB4xTC6aKNbwBJbVhnsTlwTcn5nyXzR7eKqVFOnegLbJ0PbrOytmkO56MSFBZmJR4uW9pWFqlW4-87j0q-ADUHPH_jcpw3bJfRfFzTAsBqlqU0aHKApM1Ks0hfWm9hM8JwG-goT57YyT_HNg&csuir=1&sei=rRAWafrHK-fC0PEPq-rxCQ
    pumpkins = [p for p in pumpkins if p.y - p.radius < HEIGHT]
    stems = [s for s in stems if s.y < HEIGHT]
    #

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()