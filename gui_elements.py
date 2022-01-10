import pygame

class Element:
    """ The base class for all gui type. """

    def __init__(self, x, y, width, height, color, text, font, text_color):
        self.mArea = pygame.Rect(x, y, width, height)
        self.mActive = False
        self.mColor = color
        self.mFillColor = (color[0] // 4,
                           color[1] // 4,
                           color[2] // 4)
        self.text = font.render(text, False, text_color)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.textw = self.text.get_width()
        self.texth = self.text.get_height()

    def update(self, mx, my):
        self.mActive = self.mArea.collidepoint(mx, my)

    def draw(self, surf):
        surf.blit(self.text, (self.x + (self.width / 2) - (self.textw /2), self.y + (self.height / 2) - (self.texth / 2)))
        if self.mActive:
            pygame.draw.rect(surf, self.mFillColor, self.mArea)
        pygame.draw.rect(surf, self.mColor, self.mArea, 2)


