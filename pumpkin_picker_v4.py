#Version 4.0: the end of sprint 2

# Fully working timere functionality with pumpkin falling and scoring


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
RESPAWN_MARGIN = 50
# Game timer (milliseconds)
GAME_DURATION_MS = 20 * 1000  # 30 seconds

# Fonts for timer and end-screen
FONT_SMALL = pygame.font.SysFont(None, 36)
FONT_LARGE = pygame.font.SysFont(None, 72)

#Adds a background with image "background.jpg"
background_image = pygame.image.load(os.path.join("background.jpg"))
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

pumpkin_colors = ["orange", "darkorange"]

#Cite: https://stackoverflow.com/questions/16060899/alphabet-range-in-python
new_pumpkin_letters = list(string.ascii_uppercase)

#List used to keep track of letters that have already been assigned to pumpkins. This helps avoid duplicates until all letters are used. At this point, the used letters are recycled back into the new letters list.
used_pumpkin_letters = []
score = 0   

class Pumpkin:
    """Class to represent and draw a pumpkin."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        if not new_pumpkin_letters:
            new_pumpkin_letters.extend(used_pumpkin_letters)
            used_pumpkin_letters.clear()
        self.letter = random.choice(new_pumpkin_letters)

        try:
            new_pumpkin_letters.remove(self.letter)
            used_pumpkin_letters.append(self.letter)
        except ValueError:
            pass
            
        self.is_falling = False
        self.fall_speed = 10
        # Whether selecting this pumpkin (making it fall) should award a point when it completes falling
        self.award_on_fall = False

    def draw(self, surface):
        """Draws the pumpkin given its attributes."""
        pygame.draw.circle(surface, pygame.Color(self.color), (int(self.x), int(self.y)), int(self.radius))
    
    def add_letter(self):
        """Draw the pumpkin's stored letter on the pumpkin."""
        font = pygame.font.SysFont(None, int(self.radius))
        text = font.render(self.letter, True, pygame.Color("black"))
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)
    
    def update(self):
        """Updates the pumpkin's position if it is falling."""
        if self.is_falling:
            self.y += self.fall_speed
            # pumpkin_letters.append(self.letter)
        if new_pumpkin_letters == []:
            new_pumpkin_letters.extend(used_pumpkin_letters)
            used_pumpkin_letters.clear()
    
    # def assign_new_letter(self):



class Stem:
    """Class to represent and draw a pumpkin stem."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_falling = False
        self.fall_speed = 10

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



def make_scene(num_pumpkins=5, center_x=None, center_y=None, spacing=200):
    """Creates pumpkins and stems for the scene.

    Parameters:
      num_pumpkins -- number of pumpkins/stems to create (default 5)
      center_x, center_y -- optional center position; defaults to screen center
      spacing -- horizontal spacing between pumpkins (default 200)

    Returns (pumpkins, stems)
    """
    pumpkins = []
    stems = []

    if center_x is None:
        center_x = WIDTH // 2
    if center_y is None:
        center_y = HEIGHT // 2

    mid_offset = (num_pumpkins - 1) / 2
    for n in range(num_pumpkins):
        # Pumpkin parameters (dimensions, position, color, etc.)
        x = center_x + int((n - mid_offset) * spacing)
        y = center_y
        size = random.randint(40, 60)
        color = random.choice(pumpkin_colors)

        # Stem parameters
        stem_height = 30
        stem_width = 15
        stem_top = y - size - stem_height

        stems.append(Stem(x, stem_top, stem_width, stem_height))
        pumpkins.append(Pumpkin(x, y, size, color))

    return pumpkins, stems

pumpkins, stems = make_scene()

# Start the game timer (deferred until first correct keypress)
start_ticks = None
timer_started = False
game_over = False

# Title to display before the first letter is clicked (as requested)
TITLE_TEXT = "pumpkin picke"
title_shown = True


running = True
while running:
    # Calculate elapsed time and whether the game is over
    if timer_started and start_ticks is not None:
        elapsed_ms = pygame.time.get_ticks() - start_ticks
        if not game_over and elapsed_ms >= GAME_DURATION_MS:
            game_over = True
    else:
        elapsed_ms = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        # The input is based around the user, who presses a key corresponding to a pumpkin letter on one of the five pumpkins that appear on the screen:
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                pressed_char = event.unicode.upper()
                for i, p in enumerate(pumpkins):
                    if p.letter == pressed_char and not p.is_falling:
                        # Start the timer on the first valid selection and hide the title
                        if not timer_started:
                            start_ticks = pygame.time.get_ticks()
                            timer_started = True
                            title_shown = False

                        # The output is that the pumpkin with the matching letter falls down the screen, so we set its is_falling attribute to True.
                        radii = [pp.radius for pp in pumpkins]
                        max_radius = max(radii) if radii else p.radius
                        max_count = radii.count(max_radius)
                        # attribute that sets only to true if the pumpkin is the largest and unique, you will see the score increase by 1 when it falls off the screen
                        p.award_on_fall = (p.radius == max_radius and max_count == 1)
                        p.is_falling = True
                        stems[i].is_falling = True
                        break




    # Update positions of falling pumpkins and stems (only while game running)
    if not game_over:
        for p in pumpkins:
            p.update()
        for stem in stems:
            stem.update()

    #keeps the background image
    screen.blit(background_image, (0, 0))

    
    #draw stems and pumpkins
    for stem in stems:
        stem.draw(screen)
    for p in pumpkins:
        p.draw(screen)
        # draw the already-chosen letter for each pumpkin (remains same)
        p.add_letter()

    # Draw the timer (remaining seconds) in the top-left. If timer hasn't started, show full time.
    if timer_started and start_ticks is not None:
        remaining_ms = max(0, GAME_DURATION_MS - (pygame.time.get_ticks() - start_ticks))
    else:
        remaining_ms = GAME_DURATION_MS
    remaining_seconds = remaining_ms // 1000
    timer_text = FONT_SMALL.render(f"Time: {remaining_seconds}s", True, pygame.Color("white"))
    screen.blit(timer_text, (10, 10))

    # Draw pre-start title above the game while the title is shown
    if title_shown:
        title_surface = FONT_SMALL.render(TITLE_TEXT, True, pygame.Color("white"))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 40))
        screen.blit(title_surface, title_rect)


    
    new_pumpkins = []
    new_stems = []
    
    #Cite: https://www.google.com/search?aep=48&cud=0&ie=UTF-8&q=can+you+show+me+an+example+solution+of+how+to+make+five+pumpkins+appear+on+the+screen%2C+and+making+them+able+to+fall+when+the+corresponding+letter+is+clicked%2C+referencing+the+list+of+pumpkins%3A&qsubts=1763053330009&safe=active&sourceid=chrome&udm=50&mtid=aQ8WaePtHIz40PEPl8Oo6Q4&mstk=AUtExfCZfKv8Moiqmz3M8oCFB4xTC6aKNbwBJbVhnsTlwTcn5nyXzR7eKqVFOnegLbJ0PbrOytmkO56MSFBZmJR4uW9pWFqlW4-87j0q-ADUHPH_jcpw3bJfRfFzTAsBqlqU0aHKApM1Ks0hfWm9hM8JwG-goT57YyT_HNg&csuir=1&sei=rRAWafrHK-fC0PEPq-rxCQ
    # NEW CODE (THE FIX)
    for i in range(len(pumpkins)):
        pumpkin = pumpkins[i]
        stem = stems[i]

        # If pumpkin hasn't fallen past the visible bottom (with margin), keep it
        if pumpkin.y - pumpkin.radius < HEIGHT - RESPAWN_MARGIN:
            new_pumpkins.append(pumpkin)
            new_stems.append(stem)
    #######################################

        else:
            # Pumpkin has fallen past the threshold. Count it and spawn a fresh one
            # Only award a point if this pumpkin was marked to award on fall
            if getattr(pumpkin, 'award_on_fall', False):
                score += 1
                print(f"Score: {score}")

            # Spawn a new pumpkin in the same column (same x) and reset it near the center
            spawn_x = pumpkin.x
            spawn_y = HEIGHT // 2
            size = random.randint(40, 60)
            color = random.choice(pumpkin_colors)

            # Create matching stem positioned above the new pumpkin
            stem_height = 30
            stem_width = 15
            stem_top = spawn_y - size - stem_height

            new_p = Pumpkin(spawn_x, spawn_y, size, color)
            new_s = Stem(spawn_x, stem_top, stem_width, stem_height)

            new_pumpkins.append(new_p)
            new_stems.append(new_s)

    pumpkins = new_pumpkins
    stems = new_stems

    if game_over:

        #Cite: https://www.google.com/search?q=what+does+pygame.SRCALPHA+do&rlz=1C5CHFA_enUS910US911&gs_lcrp=EgZjaHJvbWUyCggAEEUYFhgeGDkyCAgBEAAYFhgeMg0IAhAAGIYDGIAEGIoFMg0IAxAAGIYDGIAEGIoFMg0IBBAAGIYDGIAEGIoFMg0IBRAAGIYDGIAEGIoF0gEINjA0MmowajeoAgCwAgA&sourceid=chrome&ie=UTF-8&udm=50&fbs=AIIjpHxU7SXXniUZfeShr2fp4giZ1Y6MJ25_tmWITc7uy4KIeiAkWG4OlBE2zyCTMjPbGmMU8EWskMk2JSE__efdUJ3x-dd8PyEzi5Y9BtPQcYyUv-qqGBKcZRAt6t3qPZ3-iSYj4NFTLo_PkVeRaPNr8Tt4VoiX2M8mh9n-sT5J21n9U2PyFXKatPNXBOlz7UuuHiqhCxVYFODW2lnaf74YkzQdFBoLbg&ved=2ahUKEwirv725voSRAxVBMDQIHScBL1EQ0NsOegQIHxAA&aep=10&ntc=1&safe=active&ssui=on
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # 
        
        overlay.fill((0, 0, 0, 180))  # translucent dark overlay
        screen.blit(overlay, (0, 0))
        final_text = FONT_LARGE.render(f"Time's up! Score: {score}", True, pygame.Color("white"))
        ft_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(final_text, ft_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()