import pygame

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, FONT_STYLE, GAMEOVER

from game.components.spaceship import Spaceship
from game.components.enemies.enemy_manager  import Enemy_manager 
from game.components.bullets.bullet_manager import Bullet_manager
from game.components.menu import Menu
from game.components.power_ups.power_up_manager import Power_up_manager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.playing = False
        self.game_speed = 10

        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = Enemy_manager()
        self.bullet_manager = Bullet_manager()
        self.running = False
        self.score = 0
        ## se creo una nueva variable que es el puntaje mas alto 
        self.score_total = 0
        self.death_count = 0
        self.menu = Menu('Press any key to start...', self.screen)
        self.power_up_manager = Power_up_manager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.enemy_manager.reset()
        self.score = 0

        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset(self):
        self.power_up_manager.reset()
     

                 
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False


    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input, self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        ## Se hace el llamado del metodo actualizar jugador
        self.bullet_manager.update_player(self)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))

        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        ## Se hace el llamado del metodo dibujar jugador
        self.bullet_manager.draw_player(self.screen)
        self.draw_score()
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg-image_height))

        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg = self.y_pos_bg + self.game_speed

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/ 10000, 2)
            if time_to_show >=0:
                self.menu.draw(self.screen, f'{self.player.power_up_type.capitalize()}is enabled for{time_to_show} in seconds', 500,50,(255,255,255))
            else:
                self.player.has_power_up = False
                self.player.power_time_up = DEFAULT_TYPE
                self.player.set_image()

    def show_menu(self):
        self.menu.reset_screen_color(self.screen)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        ## se valida si el numero de muertes es igual a 0
        if self.death_count == 0:
            ## se pinta el menu de inicio
            self.menu.draw(self.screen)
            icon = pygame.transform.scale(ICON, (80,120))
            self.screen.blit(icon, (half_screen_width - 50, half_screen_height - 150))
        else:
            ## si el numero de muertes es diferente de 0
            ## se pinta el menu de game over
            ##actualiza el mensaje

            ##si score total es  menor o igual al score obtenido en partida 
            if self.score_total <= self.score:
                ##El score total ahora es score que obtuvo en la partida 
                ## ej : score total es 0 y el score obtenido es 3 score total ahora es 3 
                self.score_total = self.score

            self.menu.update_message('Score = {}  -  total deaths = {}  -  highest score = {}'.format(self.score, self.death_count,  self.score_total))
            ## se pinta le mensaje
            self.menu.draw(self.screen)
            ## se crea una variable icon con la imagen y tamaños 
            icon = pygame.transform.scale(GAMEOVER, (386,40))
            ## se pinta la imagen de Game Over
            self.screen.blit(icon, (half_screen_width - 190, half_screen_height - 150))
        
        self.menu.update(self)

    def update_score(self):
        self.score +=1

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE,30)
        text = font.render(f'Score: {self.score}',True,(255,255,255) )
        text_rect = text.get_rect()
        text_rect.center = (1000,50)
        self.screen.blit(text, text_rect)



