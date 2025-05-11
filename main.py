import pygame
import pytmx
from tkinter import *
from tkinter import messagebox
from enum import Enum


class TiledMap:
    def __init__(self, filename, scale=1.0):
        self.scale = scale
        self.gameMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.mapwidth = self.gameMap.tilewidth * self.gameMap.width
        self.mapheight = self.gameMap.tileheight * self.gameMap.height

    def render(self, surface):
        for layer in self.gameMap.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if tile:
                        tile = pygame.transform.scale(
                            tile,
                            (
                                int(tile.get_width() * self.scale),
                                int(tile.get_height() * self.scale),
                            ),
                        )
                        surface.blit(
                            tile,
                            (
                                x * self.gameMap.tilewidth * self.scale,
                                y * self.gameMap.tileheight * self.scale,
                            ),
                        )

    def make_map(self):
        scaled_width = int(self.mapwidth * self.scale)
        scaled_height = int(self.mapheight * self.scale)
        mapSurface = pygame.Surface((scaled_width, scaled_height))
        self.render(mapSurface)
        return mapSurface


class ReleaseAngle(Enum):
    HYZER = 0
    FLAT = 1
    ANHYZER = 2


class Display:
    def __init__(self):
        self.root = Tk()
        self.root.withdraw()
        pygame.init()

        self.scale = 2.0  # Set your desired scale factor here

        self.WIDTH = int(200 * self.scale)
        self.HEIGHT = int(584 * self.scale)
        self.displayWindow = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.displayRunning = True

        self.level_maps = ["Maps/map1.tmx", "Maps/map2.tmx", "Maps/map3.tmx", "Maps/map4.tmx", "Maps/map5.tmx", "Maps/map6.tmx", "Maps/map7.tmx"]
        self.level_start_positions = [80, 32, 80, 80, 0, 0, 0]
        self.level_options = [["x", "y", "z"], ["100", "1000", "10000"], ["100", "1000", "10000"], ["100", "1000", "10000"], ["100", "1000", "10000"], ["100", "1000", "10000"], ["100", "1000", "10000"]]
        self.level_options_points = [[0, -1, 1], [0, 1, -1], [-1, 1, 0], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
        self.level_choice_text = [
            ["Kom igen, det var tæt på!", "Helt rigtigt", "Argh, du må hellere tage dig sammen"],
            ["Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen", "Helt rigtigt"],
            ["Argh, du må hellere tage dig sammen", "Helt rigtigt", "Kom igen, det var tæt på!"],
            ["Helt rigtigt", "Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen"],
            ["Helt rigtigt", "Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen"],
            ["Helt rigtigt", "Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen"],
            ["Helt rigtigt", "Kom igen, det var tæt på!", "Argh, du må hellere tage dig sammen"]
        ]
        self.level_movement_functions = [
            [lambda x, y, c: (x + 0.05 * c, y + 5, c + 1),
             lambda x, y, c: (x, y + 5, c),
             lambda x, y, c: (x - 0.05 * c, y + 5, c + 1)],
            [lambda x, y, c: (x - 0.001 * c, y + 4, c + 1),
             lambda x, y, c: (x, y + 6, c),
             lambda x, y, c: (x + 0.015 * c, y + 4, c + 1)],
            [lambda x, y, c: (x + 0.05 * c, y + 5, c + 1),
             lambda x, y, c: (x, y + 5, c),
             lambda x, y, c: (x, y + 5, c)],
            [lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
             lambda x, y, c: (x, y + 4, c),
             lambda x, y, c: (x + 0.01 * c, y + 3, c + 1)],
            [lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
             lambda x, y, c: (x, y + 4, c),
             lambda x, y, c: (x + 0.01 * c, y + 3, c + 1)],
             [lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
             lambda x, y, c: (x, y + 4, c),
             lambda x, y, c: (x + 0.01 * c, y + 3, c + 1)],
            [lambda x, y, c: (x + 0.015 * c, y + 4, c + 1),
             lambda x, y, c: (x, y + 4, c),
             lambda x, y, c: (x + 0.01 * c, y + 3, c + 1)],
        ]
        self.level_completion_heights = [[300, 390, 200], [400, 200, 500], [250, 424, 370], [450, 270, 350], [450, 270, 350], [450, 270, 350], [450, 270, 350]]

        self.current_level = 0
        self.current_score = 0

        self.loadMap()

    def update(self):
        pygame.display.set_caption("Sebastians konfirmation")
        pygame.display.update()

    def loadMap(self):
        current_map_file = self.level_maps[self.current_level]
        self.map = TiledMap(current_map_file, self.scale)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def nextLevel(self):
        self.current_level += 1
        if self.current_level < len(self.level_maps):
            self.loadMap()
        else:
            messagebox.showinfo("Game Over", f"Du slutter med en score på {self.current_score}")
            self.root.update()
            self.displayRunning = False

    def displayLoop(self):
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)

        disc_thrown = False
        disc_radius = 8
        disc_x = self.level_start_positions[0]
        disc_y = 0
        curve_counter = 0

        smallfont = pygame.font.SysFont("Corbel", int(20 * self.scale))

        while self.displayRunning:
            mouse = pygame.mouse.get_pos()
            hyzer_text = smallfont.render(self.level_options[self.current_level][0], True, WHITE)
            flat_text = smallfont.render(self.level_options[self.current_level][1], True, WHITE)
            anhyzer_text = smallfont.render(self.level_options[self.current_level][2], True, WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.displayRunning = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not (544 * self.scale <= mouse[1] <= 584 * self.scale):
                        continue

                    disc_thrown = True
                    if 0 <= mouse[0] <= 66 * self.scale:
                        release_angle = 0
                    elif 66 * self.scale < mouse[0] <= 132 * self.scale:
                        release_angle = 1
                    elif 132 * self.scale < mouse[0] <= 200 * self.scale:
                        release_angle = 2

            self.displayWindow.blit(self.map_img, (0, 0))

            if disc_thrown:
                move_func = self.level_movement_functions[self.current_level][release_angle]
                disc_x, disc_y, curve_counter = move_func(disc_x, disc_y, curve_counter)

                completion_height = self.level_completion_heights[self.current_level][release_angle]
                choice_result_text = self.level_choice_text[self.current_level][release_angle]
                choice_score = self.level_options_points[self.current_level][release_angle]

                if disc_y - disc_radius > completion_height:
                    messagebox.showinfo(f"Bane {self.current_level + 1}", choice_result_text)
                    self.root.update()
                    self.current_score += choice_score
                    self.nextLevel()

                    if self.displayRunning:
                        disc_thrown = False
                        disc_y = 0
                        disc_x = self.level_start_positions[self.current_level]
                        curve_counter = 0

                # Draw the disc
                pygame.draw.circle(
                    self.displayWindow,
                    RED,
                    (int(disc_x * self.scale), int(disc_y * self.scale)),
                    int(disc_radius * self.scale),
                )

            # Draw UI buttons
            pygame.draw.rect(self.displayWindow, BLACK, [0, 544 * self.scale, 66 * self.scale, 40 * self.scale])
            pygame.draw.rect(self.displayWindow, BLACK, [66 * self.scale, 544 * self.scale, 66 * self.scale, 40 * self.scale])
            pygame.draw.rect(self.displayWindow, BLACK, [132 * self.scale, 544 * self.scale, 66 * self.scale, 40 * self.scale])

            self.displayWindow.blit(hyzer_text, (10 * self.scale, 554 * self.scale))
            self.displayWindow.blit(flat_text, (76 * self.scale, 554 * self.scale))
            self.displayWindow.blit(anhyzer_text, (142 * self.scale, 554 * self.scale))

            score_text = smallfont.render(f"Score: {self.current_score}", True, WHITE)
            score_rect = score_text.get_rect(topright=(self.WIDTH - 10, 10 * self.scale))
            self.displayWindow.blit(score_text, score_rect)

            self.update()
            self.clock.tick(60)


if __name__ == "__main__":
    runDisplay = Display()
    runDisplay.displayLoop()
    pygame.quit()
