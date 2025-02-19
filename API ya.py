import io
import pygame
import enum

from ya_map_library import *


class MapApp:
    DELTA_LON = 200
    DELTA_LAT = 90
    THEMES = 'light', 'dark'


    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)
        self.z = 1
        self.coord = [0, 0]
        self.theme = 0
        self.update_map()

    def update_map(self):
        bytes_img = get_static_map(ll=','.join(map(str, self.coord)), z=self.z, thema=MapApp.THEMES[self.theme])
        img = pygame.image.load(io.BytesIO(bytes_img))
        self.screen.blit(img, (0, 0))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        self.z = min(21, self.z + 1)
                    if event.key == pygame.K_PAGEDOWN:
                        self.z = max(0, self.z - 1)
                    if event.key == pygame.K_LEFT:
                        self.coord[0] = (self.coord[0] - MapApp.DELTA_LON * 2 ** -self.z + 180) % 360 - 180
                    if event.key == pygame.K_RIGHT:
                        self.coord[0] = (self.coord[0] + MapApp.DELTA_LON * 2 ** -self.z + 180) % 360 - 180
                    if event.key == pygame.K_UP:
                        self.coord[1] = min((self.coord[1] + MapApp.DELTA_LAT * 2 ** -self.z), 85)
                    if event.key == pygame.K_DOWN:
                        self.coord[1] = max((self.coord[1] - MapApp.DELTA_LAT * 2 ** -self.z), -85)
                    if event.key == pygame.K_t:
                        self.theme = 1 - self.theme
                    self.update_map()



            pygame.display.flip()


if __name__ == '__main__':
    app = MapApp((600, 450))
    app.run()