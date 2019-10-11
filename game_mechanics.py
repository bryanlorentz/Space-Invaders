from bullet import Bullet
from aliens import *
from barrier import *
from ship import *
from time import sleep
import pygame
import sys


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_q:
        sys.exit()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

        if len(aliens) == 0:
            bullets.empty()
            create_fleet(ai_settings, screen, ship, aliens)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien1_points
        for aliens in collisions.values():
            stats.score += ai_settings.alien1_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        sb.prep_level()
        stats.level += 1
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        laser = pygame.mixer.Sound("Sounds/laser.wav")
        laser.play()
        bullets.add(new_bullet)


def create_barriers(ai_settings, screen):
    barrier1 = Barrier(ai_settings, screen)
    barrier1_width = barrier1.rect.width
    barrier1.x = barrier1_width + 1.95 * barrier1_width
    barrier1.rect.x = barrier1.x
    barrier1.rect.y = barrier1.rect.height + 1.5 * barrier1.rect.height
    barrier1.blitme()

    barrier2 = Barrier(ai_settings, screen)
    barrier2.rect.x = 500
    barrier2.rect.y = 650
    barrier2.blitme()

    barrier3 = Barrier(ai_settings, screen)
    barrier3.rect.x = 750
    barrier3.rect.y = 650
    barrier3.blitme()


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            if row_number == 0:
                create_alien3(ai_settings, screen, aliens, alien_number, row_number)
            elif row_number == 1:
                create_alien2(ai_settings, screen, aliens, alien_number, row_number)
            else:
                create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_alien2(ai_settings, screen, aliens, alien_number, row_number):
    alien2 = Alien2(ai_settings, screen)
    alien_width = alien2.rect.width
    alien2.x = alien_width + 1.95 * alien_width * alien_number
    alien2.rect.x = alien2.x
    alien2.rect.y = alien2.rect.height + 1.5 * alien2.rect.height * row_number
    aliens.add(alien2)


def create_alien3(ai_settings, screen, aliens, alien_number, row_number):
    alien3 = Alien3(ai_settings, screen)
    alien_width = alien3.rect.width
    alien3.x = alien_width + 2.05 * alien_width * alien_number
    alien3.rect.x = alien3.x
    alien3.rect.y = alien3.rect.height + 6 * alien3.rect.height * row_number
    aliens.add(alien3)


def display_alien_start_screen(ai_settings, start_scr):
    alien = Alien(ai_settings, start_scr)
    alien.rect.x = 425
    alien.rect.y = 275
    alien.blitme()

    alien2 = Alien2(ai_settings, start_scr)
    alien2.rect.x = 400
    alien2.rect.y = 170
    alien2.blitme()

    alien3 = Alien3(ai_settings, start_scr)
    alien3.rect.x = 400
    alien3.rect.y = 100
    alien3.blitme()


def score_font(points, font):
    sf = font.render(points, True, (255, 255, 255))
    return sf, sf.get_rect()


def score1(start_scr):
    f_size = pygame.font.Font(None, 50)

    f, p1 = score_font('50    Points', f_size)
    p1.center = (600, 300)
    start_scr.blit(f, p1)

    f, p2 = score_font('150   Points', f_size)
    p2.center = (600, 220)
    start_scr.blit(f, p2)

    f, p3 = score_font('350   Points', f_size)
    p3.center = (600, 140)
    start_scr.blit(f, p3)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_fleet_edges(ai_settings, aliens)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    aliens.update()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 1:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        boom = Explosion(ai_settings, screen)
        boom.blitme()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        if not stats.game_active:
            sys.exit()


def store_score(stats, score_scr):
    a = []
    with open("highscore_file.txt", "r+") as file:
        file.write(str(stats.score) + "\n")
        for i in file:
            a.append(int(i))
        while len(a) > 10:
            del a[-1]
    a.sort(reverse=True)
    print(a)
    y = 100
    for i in a:
        print(i)
        display_scores(str(i), score_scr, y)
        y += 50


def display_scores(i, score_scr, y):
    f_size = pygame.font.Font(None, 50)
    f, p = score_font(i, f_size)
    p.center = (600, y)
    score_scr.blit(f, p)
    y += 50


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_button_press(play_button, ai_settings, stats, sb):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked and not stats.game_active:
                stats.game_active = True

                ai_settings.initialize_dynamic_settings()

                stats.reset_stats()

                sb.prep_score()
                sb.prep_high_score()
                sb.prep_level()
                sb.prep_ships()


def score_menu(score_button, ai_settings, stats, sb):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = score_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked and not stats.game_active:
                return True


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    pygame.display.flip()
