from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, direction = None):
        super().__init__()
        self.player_image = transform.scale(image.load(player_image), (65,65))
        self.rect = self.player_image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = direction

    def reset(self):
        window.blit(self.player_image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self,speed):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= speed
        if keys_pressed[K_DOWN] and self.rect.y < 595:
            self.rect.y += speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= speed 
        if keys_pressed[K_RIGHT] and self.rect.x < 795:
            self.rect.x += speed
    
class Enemy(GameSprite):
    def update(self,speed):
        if self.rect.x > 800:
            self.direction = 'left'
        if self.rect.x < 600:
            self.direction = 'right'
        if self.direction == 'left':
            self.rect.x -= speed
        else:
            self.rect.x += speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, height, width, x, y):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.height = height
        self.width = width
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

font.init()
font = font.Font(None, 70)
win = font.render('YOU WON', True, (0, 0, 0))
lose = font.render('YOU LOST', True, (0, 0, 0))

hero_sprite = Player('hero.png', 100, 100)
enemy_sprite = Enemy('cyborg.png', 600, 400)
treasure = GameSprite('treasure.png', 800,400)
wall_1 = Wall(120, 98, 38, 60, 120, 100, 300)
wall_2 = Wall(120, 98, 38, 200, 60, 500, 200)
wall_3 = Wall(120, 98, 38, 80, 150, 400, 0)

window = display.set_mode((900,700))
display.set_caption('Maze')
background = transform.scale(image.load('background.jpg'), (900,700))
game = True
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')
finish = False

while game:
    if not finish:
        hero_sprite.update(8)
        enemy_sprite.update(2)
        window.blit(background, (0,0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        treasure.reset()
        hero_sprite.reset()
        enemy_sprite.reset()
        if sprite.collide_rect(hero_sprite, treasure):
            window.blit(win, (350,350))
            finish = True
            money.play()
        elif sprite.collide_rect(hero_sprite, enemy_sprite) or sprite.collide_rect(hero_sprite, wall_1) or sprite.collide_rect(hero_sprite, wall_2) or sprite.collide_rect(hero_sprite, wall_3):
            window.blit(lose, (350,350))
            finish = True
            kick.play()
    events = event.get()
    for i in events:
        if i.type == QUIT:
            game = False
    clock.tick(FPS)
    display.update()