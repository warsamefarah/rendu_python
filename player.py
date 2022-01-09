import pygame

NOIR = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(NOIR)
        self.image.set_colorkey(NOIR)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        self.rect.x += pixels
        if self.rect.x > 700:
            self.rect.x = 700

    def dash_left(self, pixels):
        self.rect.x -= pixels

    def dash_right(self, pixels):
        self.rect.x += pixels

    def move_up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 540:
            self.rect.y = 540

    def move_down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > 580:
            self.rect.y = 580
