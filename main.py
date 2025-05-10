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
        self.loadMap()

    def update(self):
        pygame.display.set_caption("Sebastians konfirmation")
        pygame.display.update()

    def loadMap(self):
        self.map = TiledMap("Maps/map1.tmx")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

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
        smallfont = pygame.font.SysFont('Corbel',20) 
        hyzer_text = smallfont.render('Hyzer' , True , (255,255,255)) 
        flat_text = smallfont.render('Flat' , True , (255,255,255)) 
        anhyzer_text = smallfont.render('Anhyzer' , True , (255,255,255))         
        while self.displayRunning:
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
                        continue
                    case ReleaseAngle.FLAT:                                                                # Update disc position
                        disc_y += disc_speed  # Move the disc downward
                        completion_height = 390
                    case ReleaseAngle.ANHYZER:
                        continue

                # Check if the disc has reached the bottom
                if disc_y - disc_radius > completion_height:
                    Tk().wm_withdraw() #to hide the main window
                    messagebox.showinfo('Bane 1','ACE')

                # Draw the disc        
                pygame.draw.circle(self.displayWindow, RED, (disc_x, disc_y), disc_radius)


            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(hyzer_text, (10,554))

            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(flat_text, (80,554))

            pygame.draw.rect(self.displayWindow, RED,[0,584,66,40]) 
            self.displayWindow.blit(anhyzer_text, (140,554))
        
            self.update()
            self.clock.tick(60)  # Limit to 60 FPS

# Main driver
if __name__ == "__main__":
    runDisplay = Display()
    runDisplay.displayLoop()
    pygame.quit()