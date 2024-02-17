import os
import pygame
import requests


class MapParams(object):
    def __init__(self):
        self.lat = 60.035131
        self.lon = 30.381382
        self.zoom = 16
        self.type = "map"

    def l_l(self):
        return str(self.lon) + "," + str(self.lat)


def load_map(map_):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=map_.l_l(), z=map_.zoom, type=map_.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса")

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    map_ = MapParams()
    map_file = load_map(map_)
    pygame.display.set_caption("Карта")
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if map_.zoom < 19:
                        map_.zoom += 1

                elif event.key == pygame.K_PAGEDOWN:
                    if map_.zoom > 0:
                        map_.zoom -= 1

                elif event.key == pygame.K_UP:
                    if 19 >= map_.zoom >= 10:
                        map_.lat += 0.0015
                    elif 9 >= map_.zoom >= 0:
                        map_.lat += 1.0015

                    if map_.lat > 90:
                        map_.lat = 90

                elif event.key == pygame.K_DOWN:
                    if 19 >= map_.zoom >= 10:
                        map_.lat -= 0.0015
                    elif 9 >= map_.zoom >= 0:
                        map_.lat -= 1.0015

                    if map_.lat < -90:
                        map_.lat = -90

                elif event.key == pygame.K_RIGHT:
                    if 19 >= map_.zoom >= 10:
                        map_.lon += 0.0015
                    elif 9 >= map_.zoom >= 0:
                        map_.lon += 1.0015

                    if map_.lon > 180:
                        map_.lon = -180

                elif event.key == pygame.K_LEFT:
                    if 19 >= map_.zoom >= 10:
                        map_.lon -= 0.0015
                    elif 9 >= map_.zoom >= 0:
                        map_.lon -= 1.0015

                    if map_.lon < -180:
                        map_.lon = 180

        map_file = load_map(map_)
        screen.blit(pygame.image.load(map_file), (0, 0))
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
