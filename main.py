from settings import Settings
from ship import Ship
from aliens import *
from stats import GameStats
from menu import Button
from scoreboard import Scoreboard
import game_mechanics as gm
from pygame.sprite import Group
from barrier import Barrier


# Start screen showing the different aliens and their points.
# Also shows a menu where you can press play or look at high scores
def start_screen():
    pygame.init()
    ai_settings = Settings()
    start_scr = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, start_scr, stats)

    music = pygame.mixer.Sound("Sounds/space_music.wav")

    play_button = Button(ai_settings, start_scr, "Start", (600, 50))
    score_button = Button(ai_settings, start_scr, "Highscore", (600, 750))
    score_button.msg_image_rect.center = 600, 750

    a = gm.display_alien_start_screen(ai_settings, start_scr)
    gm.score1(start_scr)

    while True:
        music.play()
        gm.check_button_press(play_button, ai_settings, stats, sb)
        if stats.game_active:
            run_game()
        elif not stats.game_active:
            play_button.draw_button()
            score_button.draw_button()

        a = gm.score_menu(score_button, ai_settings, stats, sb)
        if a is True:
            score_screen()

        pygame.display.flip()


# Screen for running the actual game
def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    music = pygame.mixer.Sound("Sounds/space_music.wav")

    play_button = Button(ai_settings, screen, "Play", (600, 50))
    barrier = Barrier(ai_settings, screen)
    ship = Ship(ai_settings, screen)

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    bullets = Group()
    aliens = Group()

    gm.create_fleet(ai_settings, screen, ship, aliens)
    gm.create_barriers(ai_settings, screen)

    while True:
        music.play()
        gm.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        bullets.update()
        ship.update()
        barrier.update()
        gm.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gm.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gm.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets)

        pygame.display.flip()

#High score screen
def score_screen():
    pygame.init()
    ai_settings = Settings()
    score_scr = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Space Invaders")

    music = pygame.mixer.Sound("Sounds/space_music.wav")

    play_button = Button(ai_settings, score_scr, "Start", (600, 50))

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, score_scr, stats)
    a = gm.store_score(stats, score_scr)

    y = 0

    gm.display_scores(a, score_scr, y)

    while True:
        music.play()
        gm.check_button_press(play_button, ai_settings, stats, sb)

        if stats.game_active:
            run_game()
        elif not stats.game_active:
            play_button.draw_button()
        pygame.display.flip()


start_screen()

