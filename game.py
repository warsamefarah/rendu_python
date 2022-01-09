# PYGAME
import pygame
import time
import ptext
from player import Player
from ball import Ball
from brick import Brick

pygame.init()

# Variables couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (36, 90, 190)
BLEU_CLAIR = (0, 176, 240)
ROUGE = (255, 0, 0)
ORANGE = (255, 100, 0)
JAUNE = (255, 255, 0)

# Variables interface
score = 0
vies = 3

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Casse-Brique")

defeat = pygame.Surface(size)
defeat.set_alpha(128)
defeat.fill(ROUGE)

victory = pygame.Surface(size)
victory.set_alpha(128)
victory.fill(NOIR)

pause_screen = pygame.Surface(size)
pause_screen.set_alpha(50)
pause_screen.fill(BLEU)

all_sprites_list = pygame.sprite.Group()

# Setting the player
player = Player(BLEU_CLAIR, 100, 10)
player.rect.x = 350
player.rect.y = 560

# Setting the ball
ball = Ball(BLANC, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# Setting the bricks
all_bricks = pygame.sprite.Group()
for i in range(7):
    brick = Brick(ROUGE, 80, 30)
    brick.rect.x = 60 + i*100
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE, 80, 30)
    brick.rect.x = 60 + i*100
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(JAUNE, 80, 30)
    brick.rect.x = 60 + i*100
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

all_sprites_list.add(player)
all_sprites_list.add(ball)

loop = True
clock = pygame.time.Clock()


def pause():
    paused = True
    while paused:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    paused = False
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()

        screen.blit(pause_screen, (0, 0))
        ptext.draw('PAUSE', (300, 100), color=BLANC, fontsize=74)
        ptext.draw('Continuer [P]', (300, 300), color=BLANC, fontsize=34)
        ptext.draw('Quitter [echap]', (300, 350), color=BLANC, fontsize=34)
        pygame.display.flip()
        clock.tick(60)


# GAME LOOP
while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loop = False
            elif event.key == pygame.K_p:
                pause()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(5)
        # if len(all_bricks) <= 10:
        #     player.move_left(10)
    if keys[pygame.K_RIGHT]:
        player.move_right(5)
        # if len(all_bricks) <= 10:
        #     player.move_right(10)
    if keys[pygame.K_UP]:
        player.move_up(5)
    if keys[pygame.K_DOWN]:
        player.move_down(5)
    if keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
        player.dash_right(7)
    if keys[pygame.K_SPACE] and keys[pygame.K_LEFT]:
        player.dash_left(7)

    all_sprites_list.update()

    # On wall bounce
    # HORIZONTAL
    if ball.rect.x >= 790:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    # VERTICAL
    # If it touches the bottom
    if ball.rect.y >= 590:
        ball.velocity[1] = -ball.velocity[1]
        vies -= 1
        # LOSE STATE
        if vies == 0:
            screen.blit(defeat, (0, 0))
            pygame.display.flip()
            time.sleep(1)
            # font = pygame.font.Font(None, 74)
            # text = font.render("GAME OVER", 1, BLANC)
            # screen.blit(text, (250, 300))
            ptext.draw('GAME OVER', (250, 300), color=BLANC, fontsize=74, alpha=150 / 255)
            pygame.display.flip()
            pygame.time.wait(2000)

            loop = False

    if ball.rect.y <= 40:
        ball.velocity[1] = -ball.velocity[1]

    # Ball and player paddle collision
    if pygame.sprite.collide_mask(ball, player):
        ball.velocity[1] = -ball.velocity[1]
        # ball.rect.x -= ball.velocity[0]
        # ball.rect.y -= ball.velocity[1]
        # ball.bounce()

    # Brick collision
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 100
        brick.kill()
        # WIN STATE
        if len(all_bricks) == 0:
            screen.blit(victory, (0, 0))
            pygame.display.flip()
            time.sleep(1)
            # font = pygame.font.Font(None, 74)
            # text = font.render("NIVEAU TERMINÉ", 1, BLANC)
            # screen.blit(text, (200, 300))
            ptext.draw('TERMINÉ !', (250, 300), color=BLANC, fontsize=74, alpha=150 / 255)
            pygame.display.flip()
            pygame.time.wait(3000)

            loop = False

    screen.fill(NOIR)
    pygame.draw.line(screen, BLANC, [0, 38], [800, 38], 2)

    # font = pygame.font.Font(None, 34)
    # text = font.render("Score: " + str(score), 1, BLANC)
    # screen.blit(text, (20, 10))
    # text = font.render("Niveau 1", 1, BLANC)
    # screen.blit(text, (350, 10))
    # text = font.render("Vies: " + str(vies), 1, BLANC)
    # screen.blit(text, (700, 10))
    ptext.draw('Score: ' + str(score), (20, 10), color=BLANC, fontsize=34, alpha=250 / 255)
    ptext.draw('Niveau 1', (350, 10), color=BLANC, fontsize=34, alpha=250 / 255)
    ptext.draw('Vies: ' + str(vies), (700, 10), color=BLANC, fontsize=34, alpha=250 / 255)

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
