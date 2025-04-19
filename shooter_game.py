from random import randint

from pygame import *

from time import *

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font2=font.Font(None,36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

score = 0
goal = 10
lost = 0
max_lost = 3



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_w-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(80, win_w - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption('Space Shooter')
bg = transform.scale(image.load(img_back), (win_w, win_h))

ship = Player(img_hero, 5, win_h-100,80,100,10)

monsters=sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80,win_w-80),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids=sprite.Group()
for i in range(3):
    asteroid = Enemy(img_enemy, randint(80,win_w-80),-40,80,50,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
finish = False
game = True
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and red_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(bg,(0,0))
        text=font2.render('Score: '+str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose=font2.render('Missed: '+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        bullets.draw(window)
        monsters.draw(window)

        if rel_time == True:
            now_time = last_time < 3
            reload = font2.render('Reloading', 1, (150,0,0))
            window.blit(reload,(260,460))

        collides = sprite.groupcollide(monsters,bullets,True,True)
        for d in collides:
            score+=1
            monster = Enemy(img_enemy, randint(80, win_w - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life-=1
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        
        if life == 3:
            life_color = (0,150,0)
        
        if life == 2:
            life_color = (150, 150, 0)
        
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))
        display.update()
    else:
        finish = False
        score = 0
        lose = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, randint(80,win_w-80),-40,80,50,randint(1,5))
            monsters.add(monster)
    time.delay(50)

      