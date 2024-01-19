import pygame.font

from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption('Monster Killer')
        pygame.display.set_icon(pygame.image.load('images/icon.png'))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('better-vcr-5.2.ttf', fontsize)

        self.character_spritesheet = Spritesheet('images/character.png')
        self.terrain_spritesheet = Spritesheet('images/terrain.png')
        self.enemy_spritesheet = Spritesheet('images/enemy.png')
        self.attack_spritesheet = Spritesheet('images/attack.png')
        self.intro_background = pygame.image.load('images/background.jpg')
        self.game_over_background = pygame.image.load('images/gameover.png')
        self.win_background = pygame.image.load('images/win_background.jpg')

    def create_tilemap(self):
        self.player_pos = [0, 0]
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'E':
                    Enemy(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)

    def new(self):
        self.playing = True
        self.score = 0

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.timer = Timer(self)
        self.spawn = Spawn_Enemy(self)
        self.create_tilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        text = self.font.render(f'Score {self.score}', True, WHITE)
        text_rect = text.get_rect(center=(win_width - win_width / 8, win_height / 15))
        self.screen.blit(text, text_rect)
        self.timer.update()
        self.spawn.update()
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        text1 = self.font.render('Game Over', True, WHITE)
        text_rect1 = text1.get_rect(center=(win_width / 2, win_height / 2.5))
        text2 = self.font.render(f'Your score: {self.score}', True, WHITE)
        text_rect2 = text2.get_rect(center=(win_width / 2, win_height / 2))
        restart_button = Button(self, win_width / 2 - button_width / 2, win_height / 1.5 - button_height / 2,
                                'Restart', 'images/game_over_button.png')
        quit_button = Button(self, win_width / 2 - button_width / 2, win_height / 2 - 60 + win_height / 3,
                             'Quit', 'images/game_over_button.png')
        for sprite in self.all_sprites:
            sprite.kill()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro_screen()

            self.screen.blit(pygame.transform.scale(self.game_over_background, (win_width, win_height)), (0, 0))
            restart_button.draw()
            quit_button.draw()
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.clock.tick(FPS)
            pygame.display.update()

    def win_screen(self):
        if self.score > max_kills:
            change_config(win_width, win_height, button_width, button_height, size, self.score, fontsize)
        text1 = self.font.render('You won!', True, WHITE)
        text_rect1 = text1.get_rect(center=(win_width / 2, win_height / 2.5))
        text2 = self.font.render(f'Your score: {self.score}', True, WHITE)
        text_rect2 = text2.get_rect(center=(win_width / 2, win_height / 2))
        quit_button = Button(self, win_width / 2 - button_width / 2, win_height / 2 - 60 + win_height / 3,
                             'Quit', 'images/button_background.png')
        for sprite in self.all_sprites:
            sprite.kill()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro_screen()

            self.screen.blit(pygame.transform.scale(self.win_background, (win_width, win_height)), (0, 0))
            quit_button.draw()
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        title = self.font.render('Monster Killer', True, GRAY)
        title_rect = title.get_rect(x=int(25 * size), y=int(40 * size))
        play_button = Button(self, 30 * size, 140 * size,
                             'Play', 'images/button_background.png')
        option_button = Button(self, 30 * size, (140 + 30 + button_height / size) * size,
                               'Options', 'images/button_background.png')
        quit_button = Button(self, 30 * size, (140 + 60 + button_height * 2 / size) * size,
                             'Quit', 'images/button_background.png')
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if option_button.is_pressed(mouse_pos, mouse_pressed):
                self.settings_menu()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(pygame.transform.scale(self.intro_background, (win_width, win_height)), (0, 0))
            self.screen.blit(title, title_rect)
            play_button.draw()
            option_button.draw()
            quit_button.draw()
            self.clock.tick(FPS)
            pygame.display.update()

    def settings_menu(self):
        back_button = Button(self, win_width / 2 - button_width / 2, win_height / 2 - (45 / 2) + win_height / 3,
                             'Back', 'images/button_background.png')
        window_size_button3 = Button(self, win_width / 2 - button_width / 2, win_height / 1.5 - button_height,
                                     'Fullscreen', 'images/button_background.png', text_size=32 * size)
        window_size_button2 = Button(self, win_width / 2 - button_width / 2, win_height / 2 - button_height / 2,
                                     '1280*800', 'images/button_background.png')
        window_size_button1 = Button(self, win_width / 2 - button_width / 2, win_height / 3,
                                     '960*600', 'images/button_background.png')
        text = self.font.render('Resolution settings', True, GRAY)
        text_rect = text.get_rect(center=(win_width / 2, win_height / 3 - 40))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if back_button.is_pressed(mouse_pos, mouse_pressed):
                self.intro_screen()
            if window_size_button1.is_pressed(mouse_pos, mouse_pressed):
                change_config(960, 600, 215, 65, 1, max_kills, 40)
                read_config()
                self.screen = pygame.display.set_mode((win_width, win_height))
                self.font = pygame.font.Font('better-vcr-5.2.ttf', fontsize)
                self.settings_menu()
            if window_size_button2.is_pressed(mouse_pos, mouse_pressed):
                change_config(1280, 800, 250, 80, 1.4, max_kills, 55)
                read_config()
                self.screen = pygame.display.set_mode((win_width, win_height))
                self.font = pygame.font.Font('better-vcr-5.2.ttf', fontsize)
                self.settings_menu()
            if window_size_button3.is_pressed(mouse_pos, mouse_pressed):
                change_config(1920, 1080, 300, 100, 1.9, max_kills, 70)
                read_config()
                self.screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
                self.font = pygame.font.Font('better-vcr-5.2.ttf', fontsize)
                self.settings_menu()

            self.screen.blit(pygame.transform.scale(self.intro_background, (win_width, win_height)), (0, 0))
            self.screen.blit(text, text_rect)
            back_button.draw()
            window_size_button1.draw()
            window_size_button2.draw()
            window_size_button3.draw()
            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    Game.intro_screen(Game())
