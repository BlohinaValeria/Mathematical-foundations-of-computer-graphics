import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from pygame.sprite import Group

def check_events(settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                fire_bullet(settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(bullets, aliens, stats):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens_hit in collisions.values():
            stats['score'] += len(aliens_hit)
    return collisions

def create_fleet(settings, screen, aliens):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height

    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)

    available_space_y = settings.screen_height - 3 * alien_height - 100
    number_rows = available_space_y // (2 * alien_height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = Alien(settings, screen)
            alien.rect.x = alien_width + 2 * alien_width * alien_number
            alien.rect.y = alien_height + 2 * alien_height * row_number
            alien.x = float(alien.rect.x)
            aliens.add(alien)

def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def update_aliens(settings, aliens, ship, stats, screen):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        stats['ships_left'] -= 1
        aliens.empty()
        if stats['ships_left'] > 0:
            create_fleet(settings, screen, aliens)
        else:
            sys.exit()
    for alien in aliens.sprites():
        if alien.rect.bottom >= settings.screen_height:
            stats['ships_left'] -= 1
            aliens.empty()
            if stats['ships_left'] > 0:
                create_fleet(settings, screen, aliens)
            else:
                sys.exit()

def update_screen(settings, screen, ship, aliens, bullets, stats, background):
    screen.blit(background, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    font = pygame.font.SysFont(None, 48)
    score_str = f"Жизни: {stats['ships_left']}  Очки: {stats['score']}"
    score_image = font.render(score_str, True, (255, 255, 255))
    screen.blit(score_image, (20, 20))
    pygame.display.flip()

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Инопланетное вторжение")

    background = pygame.image.load('assets/background.jpg')
    background = pygame.transform.scale(background, (settings.screen_width, settings.screen_height))

    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()

    stats = {'ships_left': settings.ship_limit, 'score': 0}

    create_fleet(settings, screen, aliens)

    while True:
        check_events(settings, screen, ship, bullets)
        ship.update()
        update_bullets(bullets, aliens, stats)
        update_aliens(settings, aliens, ship, stats, screen)
        update_screen(settings, screen, ship, aliens, bullets, stats, background)

if __name__ == "__main__":
    run_game()
