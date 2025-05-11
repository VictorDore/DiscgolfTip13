import pygame
import pytmx                    
from tkinter import *
from tkinter import messagebox
from enum import Enum


class TiledMap:
    def __init__(self, filename):
        self.gameMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.mapwidth = self.gameMap.tilewidth * self.gameMap.width
        self.mapheight = self.gameMap.tileheight * self.gameMap.height

    def render(self, surface):
        for layer in self.gameMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    def make_map(self):
        mapSurface = pygame.Surface((self.mapwidth, self.mapheight))
        self.render(mapSurface)
        return mapSurface
    
class ReleaseAngle(Enum):
    HYZER = 0,
    FLAT = 1,
    ANHYZER = 2

class Display:
    def __init__(self):
        pygame.init()
        self.displayRunning = True
        self.displayWindow = pygame.display.set_mode((200, 584))
        self.clock = pygame.time.Clock()

        self.level_maps = ["Maps/map1.tmx", "Maps/map2.tmx", "Maps/map3.tmx", "Maps/map4.tmx"]
        self.level_start_positions = [80, 32, 80, 80]
        self.level_options = [["x", "y", "z"], ["100", "1000", "10000"], ["100", "1000", "10000"], ["100", "1000", "10000"]]
        self.level_options_points = [[0, -1, 1], [0, 1, -1], [-1, 1, 0], [-1, 0, 1]]
        self.level_choice_text = [
            ["Kom igen, det var tæt på!", "Helt rigtigt", "Argh, du må hellere tage dig sammen"], 
            ["Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen", "Helt rigtigt"], 
            ["Argh, du må hellere tage dig sammen", "Helt rigtigt", "Kom igen, det var tæt på!"], 
            ["Helt rigtigt", "Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen"]]
        
        # Movement functions for [HYZER, FLAT, ANHYZER] for each level
        # Each function takes (x, y, counter) and returns new (x, y, counter)
        self.level_movement_functions = [
            [  # Level 0
                lambda x, y, c: (x + 0.05 * c, y + 5, c + 1),  # HYZER
                lambda x, y, c: (x, y + 5, c),                 # FLAT
                lambda x, y, c: (x - 0.05 * c, y + 5, c + 1),  # ANHYZER
            ],
            [  # Level 1
                lambda x, y, c: (x - 0.001 * c, y + 4, c + 1),
                lambda x, y, c: (x, y + 6, c),
                lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
            ],
            [  # Level 2
                lambda x, y, c: (x + 0.05 * c, y + 5, c + 1),
                lambda x, y, c: (x, y + 5, c),
                lambda x, y, c: (x, y + 5, c),
            ],
            [  # Level 3
                lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
                lambda x, y, c: (x, y + 4, c),
                lambda x, y, c: (x + 0.01 * c, y + 3, c + 1),
            ],
        ]

        self.level_completion_heights = [[300, 390, 200], [400, 200, 500], [250, 424, 370], [450, 270, 350]]
        self.current_level = 0
        self.current_score = 0
        
        self.loadMap()

    def update(self):
        pygame.display.set_caption("Sebastians konfirmation")
        pygame.display.update()

    def loadMap(self):
        current_map_file = self.level_maps[self.current_level]
        self.map = TiledMap(current_map_file)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def nextLevel(self):
        self.current_level += 1
        if self.current_level < len(self.level_maps):
            self.loadMap()
        else:
            Tk().wm_withdraw()
            messagebox.showinfo("Game Over", f"Du slutter med en score på {self.current_score}")
            self.displayRunning = False


    def displayLoop(self):
        # Screen dimensions
        WIDTH, HEIGHT = 200, 584

        # Colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)


        # Disc properties
        disc_thrown = False
        disc_radius = 8
        disc_x = self.level_start_positions[0]
        disc_y = 0  # Start at the top of the screen
        disc_speed = 5  # Pixels per frame
        curve_amount = 0.05  # adjust this for how much it curves
        curve_counter = 0    # simulate time or distance
        
        smallfont = pygame.font.SysFont('Corbel',20) 
      
        while self.displayRunning:
            hyzer_text = smallfont.render(self.level_options[self.current_level][0] , True , (255,255,255)) 
            flat_text = smallfont.render(self.level_options[self.current_level][1] , True , (255,255,255)) 
            anhyzer_text = smallfont.render(self.level_options[self.current_level][2]  , True , (255,255,255)) 
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.displayRunning = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Cursor is not in the bottom of screen where buttons are placed
                    if  not 544 <= mouse[1] <= 584:
                        continue

                    disc_thrown = True
                    if 0 <= mouse[0] <= 66: 
                        release_angle = 0
                    elif 66 < mouse[0] <= 132:
                        release_angle = 1
                    elif 132 < mouse[0] <= 200:
                        release_angle = 2
                    


            # Draw the map to the screen
            self.displayWindow.blit(self.map_img, (0, 0))
            mouse = pygame.mouse.get_pos() 

            if disc_thrown:
                move_func = self.level_movement_functions[self.current_level][release_angle]
                disc_x, disc_y, curve_counter = move_func(disc_x, disc_y, curve_counter)
                
                completion_height = self.level_completion_heights[self.current_level][release_angle]
                choice_result_text = self.level_choice_text[self.current_level][release_angle]
                choice_score = self.level_options_points[self.current_level][release_angle]

                # Check if the disc has reached the bottom
                if disc_y - disc_radius > completion_height:
                    Tk().wm_withdraw()
                    messagebox.showinfo(f'Bane {self.current_level + 1}', choice_result_text)
                    self.current_score += choice_score
                    self.nextLevel()

                    if self.displayRunning:
                        disc_thrown = False
                        disc_y = 0  # Reset disc position for next level
                        disc_x = self.level_start_positions[self.current_level]
                        curve_counter = 0    # simulate time or distance

                # Draw the disc        
                pygame.draw.circle(self.displayWindow, RED, (disc_x, disc_y), disc_radius)

            # Clear button area first
            pygame.draw.rect(self.displayWindow, BLACK, [0, 544, 66, 40])  # Hyzer button background
            pygame.draw.rect(self.displayWindow, BLACK, [66, 544, 66, 40]) # Flat button background
            pygame.draw.rect(self.displayWindow, BLACK, [132, 544, 66, 40]) # Anhyzer button background

            # Draw updated text
            self.displayWindow.blit(hyzer_text, (10, 554))
            self.displayWindow.blit(flat_text, (76, 554))
            self.displayWindow.blit(anhyzer_text, (142, 554))

            score_text = smallfont.render(f"Score: {self.current_score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
            self.displayWindow.blit(score_text, score_rect)
        
            self.update()
            self.clock.tick(60)  # Limit to 60 FPS

# Main driver
if __name__ == "__main__":
    runDisplay = Display()
    runDisplay.displayLoop()
    pygame.quit()