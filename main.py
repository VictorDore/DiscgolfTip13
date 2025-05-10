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

        self.level_maps = ["Maps/map1.tmx", "Maps/map1.tmx"] #"Maps/map2.tmx", "Maps/map3.tmx"]
        self.level_options = [["100", "1000", "10000"], ["100", "1000", "10000"]]
        self.level_options_points = [[0, -1, 1], [0, -1, 1]]
        self.level_choice_text = [["Kom igen, det var tæt på!", "Helt rigtigt", "Argh, du må hellere tage dig sammen"], ["Kom igen, det var tæt på!", "Helt rigtigt", "Argh, du må hellere tage dig sammen"]]
        self.level_completion_heights = [[300, 390, 200], [300, 390, 200]]
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
        disc_x = WIDTH // 2  # Center of the screen horizontally
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
                        release_angle = ReleaseAngle.HYZER
                    elif 66 < mouse[0] <= 132:
                        release_angle = ReleaseAngle.FLAT
                    elif 132 < mouse[0] <= 200:
                        release_angle = ReleaseAngle.ANHYZER
                    


            # Draw the map to the screen
            self.displayWindow.blit(self.map_img, (0, 0))
            mouse = pygame.mouse.get_pos() 

            if disc_thrown:
                match release_angle:
                    case ReleaseAngle.HYZER:
                        disc_y += disc_speed
                        disc_x -= curve_amount * curve_counter  # curve to the left
                        completion_height = self.level_completion_heights[self.current_level][0]
                        curve_counter += 1
                        choice_result_text = self.level_choice_text[self.current_level][0]
                        choice_score = self.level_options_points[self.current_level][0]

                    case ReleaseAngle.FLAT:
                        disc_y += disc_speed
                        completion_height = self.level_completion_heights[self.current_level][1]
                        choice_result_text = self.level_choice_text[self.current_level][1]
                        choice_score = self.level_options_points[self.current_level][1]

                    case ReleaseAngle.ANHYZER:
                        disc_y += disc_speed
                        disc_x += curve_amount * curve_counter  # curve to the right
                        completion_height = self.level_completion_heights[self.current_level][2]
                        curve_counter += 1
                        choice_result_text = self.level_choice_text[self.current_level][2]
                        choice_score = self.level_options_points[self.current_level][2]

                # Check if the disc has reached the bottom
                if disc_y - disc_radius > completion_height:
                    Tk().wm_withdraw()
                    messagebox.showinfo(f'Bane {self.current_level + 1}', choice_result_text)
                    self.current_score += choice_score
                    self.nextLevel()
                    disc_thrown = False
                    disc_y = 0  # Reset disc position for next level
                    disc_x = WIDTH // 2  # Center of the screen horizontally

                # Draw the disc        
                pygame.draw.circle(self.displayWindow, RED, (disc_x, disc_y), disc_radius)


            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(hyzer_text, (10,554))

            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(flat_text, (80,554))

            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(anhyzer_text, (140,554))

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