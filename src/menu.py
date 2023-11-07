import pygame
import sys
from config import width, height, width_button, height_button, GRAY, BLACK, GREEN

def main_menu(screen):
    pygame.init()

    screen = pygame.display.set_mode((width, height))

    background = pygame.transform.scale(pygame.image.load("src\images\wallpaper_menu.jpg"),(width, height))

    #funcion para crear botones y centrar el texto dentro
    def draw_button(screen, text, color_button, bg_color_hoover, text_color, rect_button):
        if rect_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, bg_color_hoover, rect_button, border_radius=25)
        else:
            pygame.draw.rect(screen, color_button, rect_button, border_radius=25)
        font = pygame.font.Font(None, 52)
        label = font.render(text, True, (text_color)) 
        text_rect = label.get_rect(center = rect_button.center)  # Centra el texto en el botón
        screen.blit(label, text_rect.topleft) 

    
    menu_option = None
    
    while menu_option is None:
        # Rellena la pantalla con la imagen de fondo
        screen.blit(background, (0, 0))

        # Definir los rectángulos de los botones
        button_start_rect = pygame.Rect(width // 2 - width_button // 2, height // 2 - 2 * height_button, width_button, height_button)
        button_scores_rect = pygame.Rect(width // 2 - width_button // 2, height // 2 - height_button // 2, width_button, height_button)
        button_exit_rect = pygame.Rect(width // 2 - width_button // 2, height // 2 + height_button, width_button, height_button)

        # Dibuja los botones
        draw_button(screen, "INICIAR JUEGO", GRAY, BLACK, GREEN, button_start_rect)
        draw_button(screen, "VER PUNTUACIONES", GRAY, BLACK, GREEN, button_scores_rect)
        draw_button(screen, "SALIR", GRAY, BLACK, GREEN, button_exit_rect)

        # Procesa los eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_start_rect.collidepoint(x, y):
                    menu_option = "INICIAR JUEGO" 
                elif button_scores_rect.collidepoint(x, y):
                    menu_option = "VER PUNTUACIONES" 
                elif button_exit_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

    return menu_option

