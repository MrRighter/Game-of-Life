import pygame
import base64
from io import BytesIO


class PicGoLButton:
    def __init__(self, x, y, width, height, image_encoded, hover_image_encoded, pushing_hover_image_encoded):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = self.decode_image(image_encoded)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.decode_image(hover_image_encoded)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        self.pushing_hover_image = self.decode_image(pushing_hover_image_encoded)
        self.pushing_hover_image = pygame.transform.scale(self.pushing_hover_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False
        self.is_pushed = False

    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def decode_image(self, encoded_image):
        decoded_image = base64.b64decode(encoded_image)
        image_stream = BytesIO(decoded_image)
        return pygame.image.load(image_stream)

    def draw(self, screen):
        if self.is_pushed:
            current_image = self.pushing_hover_image
        elif self.is_hovered:
            current_image = self.hover_image
        else:
            current_image = self.image
        screen.blit(current_image, self.rect.topleft)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_pushed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_pushed:
            self.is_pushed = False
            if self.is_hovered:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
