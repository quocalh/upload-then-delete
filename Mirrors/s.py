import pygame
import time


class World(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # init here constant deffenitions
        self.proprieties()

    def proprieties(self):
        self.rect = pygame.Rect(0, 0, 3200, 3200)
        self.tiles = pygame.Rect(0, 0, 64, 64)

    def get_surface(self):
        self.surf = pygame.Surface(self.rect[2:])
        return self.surf

    def draw(self, camera_rect):
        # Draw world grid
        for x in range(self.rect[0], self.rect[2], self.tiles[2]):
            pygame.draw.line(self.surf, 'green', (x, 0), (x, self.rect.w))
        for y in range(self.rect[1], self.rect[3], self.tiles[3]):
            pygame.draw.line(self.surf, 'green', (0, y), (self.rect.h, y))

        pygame.draw.rect(self.surf, 'red', camera_rect, 5)

    def update(self, camera_rect):
        self.get_surface()
        self.draw(camera_rect)


class Camera(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.world = World()
        self.screen = pygame.display.get_surface()
        self.last_time = time.time()

        # init here constant deffenitions
        self.proprieties()

    def proprieties(self):
        self.rect = pygame.Rect(0, 0, 3200, 3200)
        self.SPEED = 250
        self.MIN_ZOOM, self.MAX_ZOOM = 800, min(self.world.rect.width, self.world.rect.height)
        self.SCROLL_UP, self.SCROLL_DOWN = 0, 0
    def get_surface(self):
        self.surf = pygame.Surface(self.rect[2:])
        return self.surf

    def zoom(self):
        zoom_factor = (self.SCROLL_DOWN - self.SCROLL_UP) * self.SPEED
        self.new_width, self.new_height = self.rect.w + zoom_factor, self.rect.h + zoom_factor

        # Clamp the zoom size
        self.new_width = max(self.MIN_ZOOM, min(self.MAX_ZOOM, self.new_width))
        self.new_height = max(self.MIN_ZOOM, min(self.MAX_ZOOM, self.new_height))

        # Center-based zoom adjustment
        camera_center = self.rect.center  # Get the current center of the camera
        self.rect.width = self.new_width
        self.rect.height = self.new_height
        self.rect.center = camera_center  # Recenter the camera around the same point
    def move(self):
        self.current_time = time.time()
        dt = (self.current_time - self.last_time)
        self.last_time = self.current_time

        key = pygame.key.get_pressed()

        horizontal_movement = (key[pygame.K_d] - key[pygame.K_a]) * self.SPEED * dt
        vertical_movement = (key[pygame.K_s] - key[pygame.K_w]) * self.SPEED * dt

        self.rect.move_ip(horizontal_movement, vertical_movement)
        self.rect = self.rect.clamp(self.world.rect)
        self.screen.get_rect().clamp(self.world.rect)

    def draw(self):
        pygame.draw.rect(self.world.surf, 'red', self.rect, 5)

    def update(self):
        self.get_surface()
        self.move()


import pygame
import sys



pygame.init()

# Set screen
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Survival')

# Clock
clock = pygame.time.Clock()
FPS = 500000000
# World
world = World()

# Camera
camera = Camera()


# Run loop
running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            camera.SCROLL_UP = event.y > 0
            camera.SCROLL_DOWN = event.y < 0
            camera.zoom()

    camera.update()
    world.update(camera.rect)

    camera.surf.blit(world.surf, [c * -1 for c in camera.rect[:2]])
    screen.blit(pygame.transform.smoothscale(camera.surf, screen.get_size()), (0, 0))

    pygame.display.flip()
    pygame.display.set_caption(f"{clock.get_fps() // 1}")

pygame.quit()
sys.exit()