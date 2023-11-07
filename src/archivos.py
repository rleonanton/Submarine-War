import pygame, os
from config import*


def save_high_score(score):
    with open("src\high_scores.txt", "a") as file:
        file.write(str(score) + "\n")


def update_high_scores(score):
    high_scores = []

    with open("src\high_scores.txt", "r") as file:
        for line in file:
            high_scores.append(int(line.strip()))

    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]

    with open("src\high_scores.txt", "w") as file:
        for score in high_scores:
            file.write(f"{score}\n")


def show_high_scores():
    show_high_score = True
    high_scores = []

    if os.path.isfile("src\high_scores.txt"):
        with open("src\high_scores.txt", "r") as file:
            high_scores = [int(line.strip()) for line in file]

    font = pygame.font.Font(None, 36)
    y = 10  # Coordenada Y inicial para mostrar los puntajes
    for i, score in enumerate(high_scores, start=1):
        text_surface = font.render(f"Puntaje {i}: {score}", True, WHITE)
        screen.blit(text_surface, (10, y))
        y += text_surface.get_height() + 5 