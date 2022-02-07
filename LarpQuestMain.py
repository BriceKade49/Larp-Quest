import pygame
import random
import math
import vector
import tileMapModule
import Pickups
import gui_elements
import os
import shutil

# fetch all files
for file_name in os.listdir(r"Rooms\\"):
    # construct full file path
    source = r"Rooms\\" + file_name
    destination = r"NewRooms\\" + file_name
    # copy only files
    if os.path.isfile(source):
        shutil.copy(source, destination)
        #print('copied', file_name)

     
pygame.init()
ds_width = 670
ds_height = 670
ds = pygame.display.set_mode((ds_width, ds_height))
Skeliton = pygame.image.load("Sprites\\SkeletonBow1.png")
Projectial = pygame.image.load("Sprites\\Arrow.png")
Hero_Pistol = pygame.image.load("Sprites\\Hero_Pistol.png")
Hero_Shotgun = pygame.image.load("Sprites\\Hero_Shotgun.png")
Hero_Minigun = pygame.image.load("Sprites\\Hero_Mini.png")
Hero_Sword = pygame.image.load("Sprites\\Hero_Sowrd.png")
Hero_Bare = pygame.image.load("Sprites\\Hero_Bare.png")
Bullet = pygame.image.load("Sprites\\Bullet.png")
UIShell = pygame.image.load("Sprites\\UIShell.png")
UIMini = pygame.image.load("Sprites\\UIMini.png")
Heart_6 = pygame.image.load("Sprites\\Heart_6.png")
Heart_5 = pygame.image.load("Sprites\\Heart_5.png")
Heart_4 = pygame.image.load("Sprites\\Heart_4.png")
Heart_3 = pygame.image.load("Sprites\\Heart_3.png")
Heart_2 = pygame.image.load("Sprites\\Heart_2.png")
Heart_1 = pygame.image.load("Sprites\\Heart_1.png")
UIBullets = pygame.image.load("Sprites\\UIBullet.png")
UIPistol = pygame.image.load("Sprites\\Pistol.png")
UIShotgun = pygame.image.load("Sprites\\shotgun.png")
UIMinigun = pygame.image.load("Sprites\\MiniGun.png")
TalkingScroll = pygame.image.load("Sprites\\Scroll2.0.png")
FireBall1 = pygame.image.load("Sprites\\FireBall.png")
DarkWizard1 = pygame.image.load("Sprites\\DarkWizard.png")
Controls = pygame.image.load("Sprites\\controls.png")
Logo = pygame.image.load("Sprites\\Logo.png")
Main_Menu = pygame.image.load("Sprites\\Menu.png")
menu_font = pygame.font.Font("Fonts\\retro_computer_personal_use.ttf", 16)
EnemyList = []
ArrowList = []
RemoveArrowList = []
BulletList = []
RemoveBulletList = []
EnemyRemoveList = []
DropRemoveList = []
#isRunning = True
px = 300
py = 300
SwordTimer = 0
bulletCount = 6
sys_font = pygame.font.SysFont("Fonts\\Cardinal.ttf", 100)
StoryText = pygame.font.SysFont("Fonts\\Cardinal.ttf", 100)
reloadFont = pygame.font.SysFont("Fonts\\Cardinal.ttf", 40)
loot_dropper = Pickups.Pickup()
fps_clock=pygame.time.Clock()
time = 0
miniGunTimer = 0
TitleScreen = True
play = False
controls = False
minigunshotting = False
SwordInstructions = True
PistalInstructions = True
Instructions = True
ShotgunInstructions1 = True
ShotgunInstructions2 = True

map1=tileMapModule.Tilemap(renderSurface=ds)
map1.fromFile("R1C1")
RoomCol= 1
RoomRow= 1


   
class StoryText(object):
    def __init__(self,FirstText,SecondText,ThirdText):
        self.x = ds_height/19
        self.y = 13*(ds_height/20)
        self.firstText = FirstText
        self.secondText = SecondText
        self.thirdText = ThirdText
    def render(self):
        ds.blit(TalkingScroll,(self.x,self.y))
        Text2 = reloadFont.render(self.firstText, 0, (56, 55, 53))
        Text = reloadFont.render(self.secondText, 0, (56, 55, 53))
        Text3 = reloadFont.render(self.thirdText, 0, (56, 55, 53))
        ds.blit(Text,(ds_height-13*(ds_width/15),ds_height-5*(ds_height/20)))
        ds.blit(Text2,(ds_height-13*(ds_width/15),ds_height-5*(ds_height/17)))
        ds.blit(Text3,(ds_height-13*(ds_width/15),ds_height-5*(ds_height/25)))
class UIClass(object):
    def __init__(self, pistol_bullet_count=100, pistol_mag_size=6, shotgun_shell_count = 100, shotgun_mag_size = 2, minigun_mag_size = 16, minigun_bullet_count = 50, reload_time=200, Health=6, GunPicked=1):
        self.PBCount = pistol_bullet_count
        self.PMSize = pistol_mag_size
        self.PSLeft = pistol_mag_size
        self.SSCount = shotgun_shell_count
        self.SMSize = shotgun_mag_size
        self.SSLeft = shotgun_mag_size
        self.MBCount = minigun_bullet_count
        self.MMSize = minigun_mag_size
        self.MBLeft = minigun_mag_size
        self.reload_time = reload_time
        self.wait_time = reload_time
        self.pistol_remaining = 0
        self.shotgun_remaining = 0
        self.minigun_remaining = 0
        self.health = Health
        self.GunPicked = GunPicked
        self.ShotGun = False
        self.MiniGun = False
        self.pistel = False
    def ShootGun(self):
        if self.GunPicked == 1:
            self.PSLeft -= 1
        elif self.GunPicked == 2:
            self.SSLeft -= 1
        elif self.GunPicked == 3:
            self.MBLeft -= 1
    def auto_pistol_reload(self):
        if self.PBCount >= self.PMSize - self.pistol_remaining:
            self.PBCount -= self.PMSize - self.pistol_remaining
            self.PSLeft += self.PMSize
            self.reload_time = self.wait_time
            self.pistol_remaining = 0
        elif self.PBCount == 0:
            self.PSLeft = 0
            self.reload_time = self.wait_time
        elif self.PBCount < self.PMSize - self.pistol_remaining:
            self.PSLeft += self.PBCount
            self.PBCount = 0
            self.reload_time = self.wait_time
            self.pistol_remaining = 0
    def auto_shotgun_reload(self):
        if self.SSCount >= self.SMSize - self.shotgun_remaining:
            self.SSCount -= self.SMSize - self.shotgun_remaining
            self.SSLeft += self.SMSize
            self.reload_time = self.wait_time
            self.shotgun_remaining = 0
        elif self.SSCount == 0:
            self.SSLeft = 0
            self.reload_time = self.wait_time
        elif self.SSCount < self.SMSize - self.shotgun_remaining:
            self.SSLeft += self.SBCount
            self.SBCount = 0
            self.reload_time = self.wait_time
            self.shotgun_remaining = 0
    def auto_minigun_reload(self): 
        if self.MBCount >= self.MMSize - self.pistol_remaining:
            self.MBCount -= self.MMSize - self.pistol_remaining
            self.MBLeft += self.MMSize
            self.reload_time = self.wait_time
            self.pistol_remaining = 0
        elif self.MBCount == 0:
            self.MBLeft = 0
            self.reload_time = self.wait_time
        elif self.MBCount < self.MMSize - self.minigun_remaining:
            self.MBLeft += self.MBCount
            self.MBCount = 0
            self.reload_time = self.wait_time
            self.pistol_remaining = 0
            
    def self_reload(self):
        if self.GunPicked == 1:
            self.pistol_remaining = self.PSLeft
            self.PSLeft = 0
        if self.GunPicked == 2:
            self.shotgun_remaining = self.SSLeft
            self.SSLeft = 0
        if self.GunPicked == 3:
            self.minigun_remaining = self.MBLeft
            self.MBLeft = 0


    def pistol_wait(self):
        if self.pistol_remaining == 0:
            self.reload_time -= 1
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
        else:
            self.reload_time -= 1 + self.pistol_remaining
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
    def shotgun_wait(self):
        if self.shotgun_remaining == 0:
            self.reload_time -= 1
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
        else:
            self.reload_time -= 1 + self.shotgun_remaining
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
    def minigun_wait(self):
        if self.minigun_remaining == 0:
            self.reload_time -= 1
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
        else:
            self.reload_time -= 1 + self.shotgun_remaining
            reloadingText = reloadFont.render("reloading...", 0, (169, 177, 188))
            ds.blit(reloadingText,(ds_height-13*(ds_width/20),ds_height-3*(ds_height/20)))
    def add_pistol_ammo(self):
        self.PBCount += 6
    def add_shotgun_ammo(self):
        self.SSCount += 2
    def add_minigun_ammo(self):
        self.MBCount += 16
    def SwitchGun(self):
        if self.GunPicked == 1 and self.ShotGun == True:
            self.GunPicked = 2
        elif self.GunPicked == 2:
            if(self.MiniGun==True):
                self.GunPicked = 3
            else:
                self.GunPicked = 1
        elif self.GunPicked == 3:
            self.GunPicked = 1
    def TakeDamage(self):
        self.health -= 1
        if self.health < 0:
            self.health == 0
    def render(self):
        if self.pistel == True:
            if self.GunPicked == 1:
                ds.blit(UIBullets,(ds_width -8*(ds_width/20),ds_height-2*(ds_height/20)-10))
                font_render = sys_font.render(str(self.PSLeft) + ":" + str(self.PBCount), 0, (169, 177, 188))
                ds.blit(UIPistol, (ds_width / 30, ds_height-2*(ds_height/20)-10))
            elif self.GunPicked == 2:
                ds.blit(UIShell, (ds_width - 8 * (ds_width / 20), ds_height - 2 * (ds_height / 20) - 20))
                font_render = sys_font.render(str(self.SSLeft) + ":" + str(self.SSCount), 0, (169, 177, 188))
                ds.blit(UIShotgun, (ds_width / 30, ds_height - 2 * (ds_height / 20) - 10))
            elif self.GunPicked == 3:
                ds.blit(UIMini, (ds_width - 8 * (ds_width / 20), ds_height - 2 * (ds_height / 20) - 10))
                font_render = sys_font.render(str(self.MBLeft) + ":" + str(self.MBCount), 0, (169, 177, 188))
                ds.blit(UIMinigun, (ds_width / 30, ds_height - 2 * (ds_height / 20) - 10))

            ds.blit(font_render, (ds_width - 5 * (ds_width / 20)-10, ds_height - 2 * (ds_height / 20)))
                                
        if self.health == 6:
            ds.blit(Heart_6,(0,0))
        if self.health == 5:
            ds.blit(Heart_5,(0,0))
        if self.health == 4:
            ds.blit(Heart_4,(0,0))
        if self.health == 3:
            ds.blit(Heart_3,(0,0))
        if self.health == 2:
            ds.blit(Heart_2,(0,0))
        if self.health == 1:
            ds.blit(Heart_1,(0,0))
        if self.health == 0:
            #quit game
            #pygame.display.quit()
            pass

class Arrow(object):
    def __init__(self,x,y,offset = 0,speed = 8, sprite = Projectial):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.angle = (math.atan2((player.y - y),(player.x - x))+ offset)
        self.angleArrow = pygame.transform.rotate(self.sprite,-math.degrees(self.angle))
        self.speed = speed
        self.height = 0 
        self.width = 0
    def move(self):
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x += self.dx
        self.y += self.dy
    def render(self):
        self.width = self.angleArrow.get_width()
        self.height = self.angleArrow.get_height()
        ds.blit(self.angleArrow,(self.x,self.y))
        #pygame.draw.circle(ds,(255,255,255),(int(self.x+self.width/2),int(self.y+self.height/2)),15)
class SkelingtonSpawner(object):
    def __init__(self,x = random.randint(100,500),y = random.randint(100,500) ,speed = 10, shotDist = 200, shotTime = 100,sprite = Skeliton,health = 3):
        self.x = random.randint(0,ds_width)
        self.y = random.randint(0,ds_height)
        self.speed = speed
        self.EV = vector.Vector2(self.x,self.y)
        self.VP = vector.Vector2(px,py)
        self.VA = self.EV - self.VP
        self.collide = None
        self.ox = self.x
        self.oy = self.y
        self.shotDist = shotDist
        self.shotTime = shotTime
        self.sprite = sprite
        self.flipE = True
        self.health = health
    def move(self,px,py):
        if self.health<= 0:
            EnemyRemoveList.append(self)
        self.EV = vector.Vector(self.x,self.y)
        self.VP = vector.Vector2(px+50,py+50)
        self.VA = self.VP - self.EV
        dx = self.x - px
        dy = self.y - py
        distance = (dx**2 + dy**2)**.5
        if self.x < px and  distance > self.shotDist:
            self.x = self.x + self.speed
        if self.y < py and distance > self.shotDist:
            self.y = self.y + self.speed
        if self.x > px and distance > self.shotDist:
            self.x = self.x - self.speed
        if self.y > py and distance > self.shotDist:
            self.y = self.y - self.speed
        if px < self.x and self.flipE == True:
            self.flipE = False
            self.sprite = pygame.transform.flip(self.sprite,True,False)
        elif px >= self.x and self.flipE == False:
                self.flipE = True
                self.sprite = pygame.transform.flip(self.sprite,True,False)
        if distance <= self.shotDist and time % self.shotTime == 0:
            self.shot()
        if isinstance(self, DarkWizard):
            if distance <= self.shotDist and time % 800 == 0:
                self.spawn()
    def render(self,px,py):
            self.collide = ds.blit(self.sprite,(self.x,self.y))

    def shot(self):
        ArrowList.append(Arrow(self.x,self.y,0))
        
class Player(object):
    def __init__(self):
        self.x = 400
        self.y = 300
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.BulletCount = 6
        self.coolDown = 0
        self.canShoot = True
        self.Hero_Pistol = Hero_Pistol
        self.Hero_Shotgun = Hero_Shotgun
        self.Hero_Sword = Hero_Sword
        self.Hero_Minigun = Hero_Minigun
        self.Hero_Bare = Hero_Bare
        self.colliderect = None
        self.flip = None
        self.sAttck = 0
        self.swordOnly = True

    def move(self, keys,dt,mx):
        if mx > self.x:
            self.flip = True
            if(self.swordOnly==True):
                self.Hero_Bare = pygame.transform.flip(Hero_Bare,True,False)
            if(self.sAttck>0):
                self.Hero_Sword = pygame.transform.flip(Hero_Sword,True,False)
            elif UI.GunPicked == 1:
                self.Hero_Pistol = pygame.transform.flip(Hero_Pistol,True,False)
            elif UI.GunPicked == 2:
                self.Hero_Shotgun = pygame.transform.flip(Hero_Shotgun, True, False)
            elif UI.GunPicked == 3:
                self.Hero_Minigun = pygame.transform.flip(Hero_Minigun, True, False)
        else:
            self.flip = False
            if(self.swordOnly==True):
                self.Hero_Bare = pygame.transform.flip(Hero_Bare,False,False)
            if(self.sAttck>0):
                self.Hero_Sword = pygame.transform.flip(Hero_Sword,False,False)
            elif UI.GunPicked == 1:
                self.Hero_Pistol = pygame.transform.flip(Hero_Pistol,False,False)
            elif UI.GunPicked == 2:
                self.Hero_Shotgun = pygame.transform.flip(Hero_Shotgun, False, False)
            elif UI.GunPicked == 3:
                self.Hero_Minigun = pygame.transform.flip(Hero_Minigun, False, False)
        skirt = 1
        if keys[pygame.K_w]:
            self.dy = -skirt
        if keys[pygame.K_s]:
            self.dy = skirt
        if keys[pygame.K_a]:
            self.dx = -skirt
        if keys[pygame.K_d]:
            self.dx = skirt

        self.x += self.dx*(dt//5)
        self.y += self.dy*(dt//5)

        self.dx = 0
        self.dy = 0

    def render(self, ds):
        if self.swordOnly == True:
            if(self.sAttck>0):
                self.swordAttack(ds)
            else:
                self.colliderect = ds.blit(self.Hero_Bare,(self.x,self.y))
        else:
            if(self.sAttck>0):
                self.swordAttack(ds)
            else:
                if UI.GunPicked == 1:
                    self.colliderect = ds.blit(self.Hero_Pistol,(self.x,self.y))
                elif UI.GunPicked == 2:
                    self.colliderect = ds.blit(self.Hero_Shotgun, (self.x, self.y))
                elif UI.GunPicked == 3:
                    self.colliderect = ds.blit(self.Hero_Minigun, (self.x, self.y))
            

            
    def swordAttack(self, ds):
        self.colliderect = ds.blit(self.Hero_Sword,(self.x,self.y))
        self.sAttck -= 1

class Shoot(object):
    def __init__(self,x,y,angle,speed = 5):
        if player.flip == True:
            self.x = x + 75
        else:
            self.x = x - 5
        self.y = y + 30
        self.speed = 10
        self.angle = angle
        self. Bullet = pygame.transform.rotate(Bullet,-math.degrees(angle))
    def move (self,mx,my):
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.x += self.dx
        self.y += self.dy
    def render(self):
        ds.blit(self.Bullet,(self.x,self.y))
class ShotGunShoot(Shoot):
    def render(self):
        pygame.draw.circle(ds,(150,150,150),(int(self.x),int(self.y)),5,0)
class FireBall(Arrow):
    def render(self):
        self.width = self.angleArrow.get_width()
        self.height = self.angleArrow.get_height()
        ds.blit(self.angleArrow,(self.x,self.y))
        #pygame.draw.circle(ds,(255,0,0),(int(self.x),int(self.y)),10)
class DarkWizard(SkelingtonSpawner):
    def shot(self):
        ArrowList.append(FireBall(self.x,self.y,0,4,sprite = FireBall1))
        ArrowList.append(FireBall(self.x,self.y,0.75, 4,sprite = FireBall1))
        ArrowList.append(FireBall(self.x,self.y,1.5,4,sprite = FireBall1))
        ArrowList.append(FireBall(self.x,self.y,-0.75,4,sprite = FireBall1))
    def spawn(self):
        EnemyList.append(SkelingtonSpawner())
    def render(self,px,py):
        pygame.draw.rect(ds,(255,0,0),(250,10,self.health*10,20))
        self.collide = ds.blit(self.sprite,(self.x,self.y))
class Menu(object):
    def __init__(self, screen, logo, font):
        self.screen = screen
        self.logo = logo
        self.font = font
        self.color = (0, 0, 255)
        tempplay = self.font.render("PLAY", False, (255, 255, 255))
        tempcontrols = self.font.render("CONTROLS", False, (255, 255, 255))
        tempquit = self.font.render("QUIT", False, (255, 255, 255))
        self.menulist = [tempplay, tempcontrols, tempquit]
        self.boxwidth = 0
        self.boxheight = 0
        for option in self.menulist:
            if self.boxwidth < option.get_width():
                self.boxwidth = option.get_width() + 20
            if self.boxheight < option.get_height():
                self.boxheight = option.get_height() + 10
        self.boxlist = []
        x = (self.screen.get_width() / 2) - (self.boxwidth / 2)
        y = 350
        text = "play"
        for i in range(len(self.menulist)):
            self.boxlist.append(gui_elements.Element(x, y, self.boxwidth, self.boxheight, self.color, text, self.font, (255, 255, 255)))
            y += 75
            if text == "play":
                text = "controls"
            elif text == "controls":
                text = "quit"


    def update(self, mx, my):
        for box in self.boxlist:
            box.update(mx, my)


    def render(self, surface):
        win_width = surface.get_width()
        surface.blit(self.screen, (0, 0))
        logo_width = self.logo.get_width()
        surface.blit(self.logo, (((win_width / 2) - (logo_width / 2)), 10))
        for box in self.boxlist:
            box.draw(surface)

screen = Menu(Main_Menu, Logo, menu_font)
while TitleScreen == True:
    cur_event = pygame.event.poll()
    # event-handling
    if cur_event.type == pygame.QUIT:
        break
    elif cur_event.type == pygame.KEYDOWN:
        if cur_event.key == pygame.K_ESCAPE:
            break

    mx, my = pygame.mouse.get_pos()
    box1, box2, box3 = screen.boxlist
    if cur_event.type == pygame.MOUSEBUTTONDOWN:
        if box1.mArea.collidepoint(mx, my):
            play = True
            TitleScreen = False
        if box2.mArea.collidepoint(mx, my):
            controls = True
            TitleScreen = False
        if box3.mArea.collidepoint(mx, my):
            break

    screen.update(mx, my)
    screen.render(ds)

    pygame.display.update()

while controls == True:
    ds.blit(Controls, (25, 0))
    tempback = gui_elements.Element(500, 10, 100, 30, (0, 0, 0), "Back", menu_font, (0, 0, 0))
    cur_event = pygame.event.poll()
    if cur_event.type == pygame.QUIT:
        break
    elif cur_event.type == pygame.KEYDOWN:
        if cur_event.key == pygame.K_ESCAPE:
            break

    mx, my = pygame.mouse.get_pos()
    if cur_event.type == pygame.MOUSEBUTTONDOWN:
        if tempback.mArea.collidepoint(mx, my):
            TitleScreen = True
            controls = False
    tempback.update(mx, my)
    tempback.draw(ds)

    pygame.display.update()

player = Player()
UI = UIClass()
Message3 = StoryText("Old Lady: Oh its you from the trailer.","If you want to get out of here you","are going to need to get")
Message4 = StoryText("the key to the Dark Wizards catsle.","Its deep in the undead grave yard","enter to continue")
Message2 = StoryText("Instructions: Use W,A,S,D key to","move around","Who said that??? enter to continue")
Message = StoryText("Screw this sword I'm from Texas and","we always packing *pulls out revolver*"," enter to continue")
Message1 = StoryText("Instructions: right click to attack"," enemies with your sword","enter to continue")
textOn = False
for num in range(map1.PickupDic["pAmmo"]):
    loot_dropper.dropped_list.append(["pAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
for num in range(map1.PickupDic["sAmmo"]):
    loot_dropper.dropped_list.append(["sAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
for num in range(map1.PickupDic["mAmmo"]):
    loot_dropper.dropped_list.append(["mAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
for num in range(map1.PickupDic["miniGun"]):
    loot_dropper.dropped_list.append(["miniGun",ds_width - 150,ds_height - 150,128,128])
for num in range(map1.PickupDic["key"]):
    loot_dropper.dropped_list.append(["key",ds_width - 50,ds_height - 50,128,128])
for num in range(map1.PickupDic["HP"]):
    loot_dropper.dropped_list.append(["HP",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
for num in range(map1.EnemyDic["Skeleton"]):
    EnemyList.append(SkelingtonSpawner())
for num in range(map1.EnemyDic["WizBoss"]):
    EnemyList.append(DarkWizard(shotDist = 350,shotTime = 300,sprite = DarkWizard1, health = 30))
while play == True:
    SwordAttack = False
    dt = fps_clock.tick(60)
    if(SwordTimer > 0):
        SwordTimer-=dt
    time += 1
    mx, my = pygame.mouse.get_pos()
    #ds.blit(BackgroundImage,(0,0))  
    map1.render()
    loot_dropper.render(ds)
    player.render(ds)
    pygame.event.pump()
    keys=pygame.key.get_pressed()
    player.move(keys, dt,mx)

    # Wall Collisions

    # For Player
    if "FT" in map1.checkTileMapCollision(player.x + 50, player.y, 32, 64):
        player.x = old_x
        player.y = old_y

    if "FL" in map1.checkTileMapCollision(player.x, player.y + 50, 64, 64):
        player.x = old_x
        player.y = old_y

    if "FR" in map1.checkTileMapCollision(player.x + 50, player.y + 50, 10, 32):
        player.x = old_x
        player.y = old_y

    if "FB" in map1.checkTileMapCollision(player.x + 50, player.y + 50, 32, 32):
        player.x = old_x
        player.y = old_y

    if "TS" in map1.checkTileMapCollision(player.x + 50, player.y + 50, 10, 32):
        player.x = old_x
        player.y = old_y
        
    if "WW" in map1.checkTileMapCollision(player.x + 50, player.y + 50, 10, 32):
        player.x = old_x
        player.y = old_y
        
    if "WW" in map1.checkTileMapCollision(player.x, player.y + 50, 10, 32):
        player.x = old_x
        player.y = old_y

    old_x = player.x
    old_y = player.y

    # For Enemy

    for enemy in EnemyList:
        if "FT" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 32, 64):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        if "FL" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 64, 64):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        if "FR" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 10, 32):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        if "FB" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 32, 32):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        if "TS" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 10, 32):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        if "WW" in map1.checkTileMapCollision(enemy.x + 50, enemy.y + 50, 10, 32):
            enemy.x = enemy.ox
            enemy.y = enemy.oy
        
        if "WW" in map1.checkTileMapCollision(enemy.x, enemy.y + 50, 10, 32):
            enemy.x = enemy.ox
            enemy.y = enemy.oy

        enemy.ox = enemy.x
        enemy.oy = enemy.y

    if player.x <= 0:
        oldRoom = ("R"+str(RoomRow)+"C"+str(RoomCol))
        newRoom = ("R"+str(RoomRow+1)+"C"+str(RoomCol))

        # Builds dictionary
        s=0
        w=0
        sa=0
        ma=0
        pa=0
        hpd=0
        kd=0
        mini=0
        for enemy in EnemyList:
            if enemy.__class__ == SkelingtonSpawner:
                s+=1
                print("Skeletons:", s)
            if enemy.__class__ == DarkWizard:
                w+=1

        for item in loot_dropper.dropped_list:
            if item[0] == "sAmmo":
                sa+=1
            if item[0] == "pAmmo":
                pa+=1
            if item[0] == "mAmmo":
                ma+=1
            if item[0] == "HP":
                hpd+=1
            if item[0] == "key":
                kd+=1
            if item[0] == "miniGun":
                mini+=1
        map1.PickupDic["sAmmo"] = sa
        map1.PickupDic["pAmmo"] = pa
        map1.PickupDic["mAmmo"] = ma
        map1.PickupDic["HP"] = hpd
        map1.PickupDic["key"] = kd
        map1.PickupDic["miniGun"] = mini
        
        map1.EnemyDic["Skeleton"] = s
        map1.EnemyDic["WizBoss"] = w

        map1.toFile("NewRooms//"+oldRoom+".map")
        ArrowList = []
        #Pickup saving
        #for item in loot_dropper.dropped_list:
          #  DropRemoveList.append(item)
        loot_dropper.dropped_list = []
        map1.fromFile(newRoom)
        
        for num in range(map1.PickupDic["pAmmo"]):
            loot_dropper.dropped_list.append(["pAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["sAmmo"]):
            loot_dropper.dropped_list.append(["sAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["mAmmo"]):
            loot_dropper.dropped_list.append(["mAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["miniGun"]):
            loot_dropper.dropped_list.append(["miniGun",ds_width - 150,ds_height - 150,128,128])
        for num in range(map1.PickupDic["key"]):
            loot_dropper.dropped_list.append(["key",ds_width - 50,ds_height - 50,128,128])
        for num in range(map1.PickupDic["HP"]):
            loot_dropper.dropped_list.append(["HP",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        
        
        #Enemy Spawning
        EnemyList=[] 
        for num in range(map1.EnemyDic["Skeleton"]):
            EnemyList.append(SkelingtonSpawner())
        for num in range(map1.EnemyDic["WizBoss"]):
            EnemyList.append(DarkWizard())
        
        player.x = 4*(ds_width/6)
        player.y = ds_height/2-50
        RoomRow += 1
    if player.x >= ds_width:
        oldRoom = ("R"+str(RoomRow)+"C"+str(RoomCol))
        newRoom = ("R"+str(RoomRow-1)+"C"+str(RoomCol))
        # Builds dictionary
        s=0
        w=0
        sa=0
        ma=0
        pa=0
        hpd=0
        kd=0
        mini=0
        for enemy in EnemyList:
            if enemy.__class__ == SkelingtonSpawner:
                s+=1
                print("Skeletons:", s)
            if enemy.__class__ == DarkWizard:
                w+=1
        for item in loot_dropper.dropped_list:
            if item[0] == "sAmmo":
                sa+=1
            if item[0] == "pAmmo":
                pa+=1
            if item[0] == "mAmmo":
                ma+=1
            if item[0] == "HP":
                hpd+=1
            if item[0] == "key":
                kd+=1
            if item[0] == "miniGun":
                mini+=1
        map1.PickupDic["sAmmo"] = sa
        map1.PickupDic["pAmmo"] = pa
        map1.PickupDic["mAmmo"] = ma
        map1.PickupDic["HP"] = hpd
        map1.PickupDic["key"] = kd
        map1.PickupDic["miniGun"] = mini


        map1.EnemyDic["Skeleton"] = s
        map1.EnemyDic["WizBoss"] = w

        map1.toFile("NewRooms//"+oldRoom+".map")
        ArrowList = []
        #for item in loot_dropper.dropped_list:
          #  DropRemoveList.append(item)
        loot_dropper.dropped_list = []
        map1.fromFile(newRoom)

        for num in range(map1.PickupDic["pAmmo"]):
            loot_dropper.dropped_list.append(["pAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["sAmmo"]):
            loot_dropper.dropped_list.append(["sAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["mAmmo"]):
            loot_dropper.dropped_list.append(["mAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["miniGun"]):
            loot_dropper.dropped_list.append(["miniGun",ds_width - 150,ds_height - 150,128,128])
        for num in range(map1.PickupDic["key"]):
            loot_dropper.dropped_list.append(["key",ds_width - 50,ds_height - 50,128,128])
        for num in range(map1.PickupDic["HP"]):
            loot_dropper.dropped_list.append(["HP",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        

        #Enemy Spawning
        EnemyList=[] 
        for num in range(map1.EnemyDic["Skeleton"]):
            EnemyList.append(SkelingtonSpawner())
        for num in range(map1.EnemyDic["WizBoss"]):
            EnemyList.append(DarkWizard(shotDist = 350,shotTime = 300,sprite = DarkWizard1, health = 30))
            
        player.x = ds_width/6
        player.y = ds_height/2-50
        RoomRow -= 1
    if player.y <= 0:
        oldRoom = ("R"+str(RoomRow)+"C"+str(RoomCol))
        newRoom = ("R"+str(RoomRow)+"C"+str(RoomCol+1))
        # Builds dictionary
        s=0
        w=0
        sa=0
        ma=0
        pa=0
        hpd=0
        kd=0
        mini=0
        for enemy in EnemyList:
            if enemy.__class__ == SkelingtonSpawner:
                s+=1
                print("Skeletons:", s)
            if enemy.__class__ == DarkWizard:
                w+=1

        for item in loot_dropper.dropped_list:
            if item[0] == "sAmmo":
                sa+=1
            if item[0] == "pAmmo":
                pa+=1
            if item[0] == "mAmmo":
                ma+=1
            if item[0] == "HP":
                hpd+=1
            if item[0] == "key":
                kd+=1
            if item[0] == "miniGun":
                mini+=1
        map1.PickupDic["sAmmo"] = sa
        map1.PickupDic["pAmmo"] = pa
        map1.PickupDic["mAmmo"] = ma
        map1.PickupDic["HP"] = hpd
        map1.PickupDic["key"] = kd
        map1.PickupDic["miniGun"] = mini
        
        map1.EnemyDic["Skeleton"] = s
        map1.EnemyDic["WizBoss"] = w

        map1.toFile("NewRooms//"+oldRoom+".map")
        ArrowList = []
           #for item in loot_dropper.dropped_list:
          #  DropRemoveList.append(item)
        loot_dropper.dropped_list = []
        map1.fromFile(newRoom)

        for num in range(map1.PickupDic["pAmmo"]):
            loot_dropper.dropped_list.append(["pAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["sAmmo"]):
            loot_dropper.dropped_list.append(["sAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["mAmmo"]):
            loot_dropper.dropped_list.append(["mAmmo",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        for num in range(map1.PickupDic["miniGun"]):
            loot_dropper.dropped_list.append(["miniGun",ds_width - 150,ds_height - 150,128,128])
        for num in range(map1.PickupDic["key"]):
            loot_dropper.dropped_list.append(["key",ds_width - 50,ds_height - 50,128,128])
        for num in range(map1.PickupDic["HP"]):
            loot_dropper.dropped_list.append(["HP",random.randint(0,ds_width-64),random.randint(0,ds_height-64),128,128])
        


        #Enemy Spawning
        EnemyList=[] 
        for num in range(map1.EnemyDic["Skeleton"]):
            EnemyList.append(SkelingtonSpawner())
        for num in range(map1.EnemyDic["WizBoss"]):
            EnemyList.append(DarkWizard(shotDist = 350,shotTime = 300,sprite = DarkWizard1, health = 30))
            
        player.x = ds_width/2-50
        player.y = (ds_height/10)*9
        RoomCol += 1
    if player.y >= ds_height:
        oldRoom = ("R"+str(RoomRow)+"C"+str(RoomCol))
        newRoom = ("R"+str(RoomRow)+"C"+str(RoomCol-1))
        # Builds dictionary
        s=0
        w=0
        sa=0
        ma=0
        pa=0
        hpd=0
        kd=0
        mini=0
        for enemy in EnemyList:
            if enemy.__class__ == SkelingtonSpawner:
                s+=1
                print("Skeletons:", s)
            if enemy.__class__ == DarkWizard:
                w+=1

        for item in loot_dropper.dropped_list:
            if item[0] == "sAmmo":
                sa+=1
            if item[0] == "pAmmo":
                pa+=1
            if item[0] == "mAmmo":
                ma+=1
            if item[0] == "HP":
                hpd+=1
            if item[0] == "key":
                kd+=1
            if item[0] == "miniGun":
                mini+=1
        map1.PickupDic["sAmmo"] = sa
        map1.PickupDic["pAmmo"] = pa
        map1.PickupDic["mAmmo"] = ma
        map1.PickupDic["HP"] = hpd
        map1.PickupDic["key"] = kd
        map1.PickupDic["miniGun"] = mini
        
        map1.EnemyDic["Skeleton"] = s
        map1.EnemyDic["WizBoss"] = w

        map1.toFile("NewRooms//"+oldRoom+".map")
        ArrowList = []
        #for item in loot_dropper.dropped_list:
          #  DropRemoveList.append(item)
        loot_dropper.dropped_list = []
        map1.fromFile(newRoom)

        for num in range(map1.PickupDic["pAmmo"]):
            loot_dropper.dropped_list.append(["pAmmo",random.randint(0,ds_width),random.randint(0,ds_height),128,128])
        for num in range(map1.PickupDic["sAmmo"]):
            loot_dropper.dropped_list.append(["sAmmo",random.randint(0,ds_width),random.randint(0,ds_height),128,128])
        for num in range(map1.PickupDic["mAmmo"]):
            loot_dropper.dropped_list.append(["mAmmo",random.randint(0,ds_width),random.randint(0,ds_height),128,128])
        for num in range(map1.PickupDic["miniGun"]):
            loot_dropper.dropped_list.append(["miniGun",ds_width - 150,ds_height - 150,128,128])
        for num in range(map1.PickupDic["key"]):
            loot_dropper.dropped_list.append(["key",ds_width - 50,ds_height - 50,128,128])
        for num in range(map1.PickupDic["HP"]):
            loot_dropper.dropped_list.append(["HP",random.randint(0,ds_width),random.randint(0,ds_height),128,128])
        



        #Enemy Spawning
        EnemyList=[] 
        for num in range(map1.EnemyDic["Skeleton"]):
            EnemyList.append(SkelingtonSpawner())
        for num in range(map1.EnemyDic["WizBoss"]):
            EnemyList.append(DarkWizard(shotDist = 350,shotTime = 300,sprite = DarkWizard1, health = 30))
            
        player.x = ds_width/2 - 50
        player.y = (ds_height/10)
        RoomCol -= 1
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            play = False
        if events.type == pygame.KEYDOWN: 
            if keys[pygame.K_ESCAPE]:
                play = False
            if keys[pygame.K_m]:
                if textOn:
                    textOn = False
                elif textOn == False:
                    textOn = True
                Message.render()
            if keys[pygame.K_k]:
                EnemyList.append(SkelingtonSpawner())
            if keys[pygame.K_t]:
                 EnemyList.append(DarkWizard(shotDist = 350,shotTime = 300,sprite = DarkWizard1, health = 30))
            if keys[pygame.K_r]:
                if UI.reload_time == UI.wait_time:
                    UI.self_reload()
            if keys[pygame.K_i]:
                UI.add_pistol_ammo()
            if keys[pygame.K_o]:
                UI.add_shotgun_ammo()
        if events.type == pygame.MOUSEBUTTONUP:
            minigunshotting = False
        if events.type == pygame.MOUSEBUTTONDOWN:
            m1,m2,m3 = pygame.mouse.get_pressed(3)
            #mm1,mm2,mm3 = pygame
            if m1:
                angle = math.atan2((my - player.y),(mx - player.x))
                if player.swordOnly == False:
                    if UI.PSLeft > 0 and UI.GunPicked == 1:
                        UI.ShootGun()
                        #if player.canShoot and player.BulletCount > 0:
                        BulletList.append(Shoot(player.x, player.y, angle))
                        #player.gunUpdate()
                    if UI.SSLeft > 0 and UI.GunPicked == 2:
                        UI.ShootGun()
                        BulletList.append(ShotGunShoot(player.x, player.y,angle))
                        BulletList.append(ShotGunShoot(player.x, player.y,angle+0.2))
                        BulletList.append(ShotGunShoot(player.x, player.y, angle-0.2))
                    if UI.MBLeft > 0 and UI.GunPicked == 3:
                        minigunshotting = True
                    

            if m2:
                UI.SwitchGun()
            if m3:
                #sword attack here
                if(SwordTimer<=0):
                     SwordAttack = True
                     player.swordAttack(ds)
                     SwordTimer = 1000
                     player.sAttck = 10
    if(miniGunTimer>0):
        miniGunTimer-=dt
    if(minigunshotting == True and UI.MBLeft > 0 and UI.GunPicked == 3 and miniGunTimer<=0):
        angle = math.atan2((my - player.y),(mx - player.x))
        UI.ShootGun()
        BulletList.append(Shoot(player.x, player.y, angle))
        miniGunTimer = 100
    for Enemy in EnemyList:
        Enemy.move(player.x, player.y)
        Enemy.render(player.x, player.y)
        if(SwordAttack):
            if (abs((Enemy.x - player.x)+(Enemy.y - player.y))<=100):
                print("sword attack hit")
                Enemy.health-=1
                
                
        #for otherSkelington in EnemyList:
            #if Skelington.collide.colliderect(otherSkelington.collide):
                #print("touching")
    for arrow in ArrowList:
        arrow.move()
        arrow.render()
        if ds_width< arrow.x or arrow.x <0:
            RemoveArrowList.append(arrow)
        if ds_height < arrow.y or arrow.y < 0:
            RemoveArrowList.append(arrow)
        if player.colliderect.collidepoint(arrow.x+arrow.width/2,arrow.y+arrow.height/2):
            #for Arrows in ArrowList:
            RemoveArrowList.append(arrow)
            UI.TakeDamage()

    for bullet in BulletList:
        bullet.move(mx,my)
        bullet.render()
        if ds_width< bullet.x or bullet.x <0:
            RemoveBulletList.append(bullet)
        if ds_height < bullet.y or bullet.y < 0:
            RemoveBulletList.append(bullet)
        for enemy in EnemyList:
            if enemy.collide.collidepoint(bullet.x,bullet.y):
                RemoveBulletList.append(bullet)
                enemy.health-= 1
                #EnemyRemoveList.append(enemy)
                for Bullets in BulletList:
                    RemoveArrowList.append(Bullets)

    for item in loot_dropper.dropped_list:
        temp_rect = pygame.Rect(item[1], item[2], item[3], item[4])
        if temp_rect.colliderect(player.colliderect):
            if item[0] == "HP":
                if UI.health < 6:
                    UI.health += 1
                    if UI.health < 6:
                        UI.health += 1
                DropRemoveList.append(item)
            elif item[0] == "pAmmo":
                UI.add_pistol_ammo()
                DropRemoveList.append(item)
            elif item[0] == "sAmmo":
                UI.add_shotgun_ammo()
                DropRemoveList.append(item)
            elif item[0] == "mAmmo":
                #TODO: add UI.add_minigun_ammo()
                DropRemoveList.append(item)
            elif item[0] == "miniGun":
                #TODO: add mini gun to wepons list
                UI.MiniGun = True
                loot_dropper.items.append("mAmmo")
                DropRemoveList.append(item)
            elif item[0] == "key":
                #TODO: add key to invitory
                DropRemoveList.append(item)

                
   
    for Bullets in RemoveBulletList:
        if Bullets in BulletList:
            BulletList.remove(Bullets)
        
    for Arrows in RemoveArrowList:
        if Arrows in ArrowList:
            ArrowList.remove(Arrows)
    RemoveArrowList = []

    for enemy in EnemyRemoveList:
        if enemy in EnemyList:
            drop = random.randint(1, 2)
            if drop == 1:
                loot_dropper.drop(enemy.x, enemy.y)
            EnemyList.remove(enemy)

    for item in DropRemoveList:
        if item in loot_dropper.dropped_list:
            loot_dropper.dropped_list.remove(item)

    if UI.PSLeft == 0:
        if UI.GunPicked == 1:
            if UI.PBCount > 0:
                UI.pistol_wait()
                if UI.reload_time < 0:
                    UI.auto_pistol_reload()
    if UI.SSLeft == 0:
        if UI.GunPicked == 2:
            if UI.SSCount > 0:
                UI.shotgun_wait()
                if UI.reload_time < 0:
                    UI.auto_shotgun_reload()
    if UI.MBLeft == 0:
        if UI.GunPicked == 3:
            if UI.MBCount > 0:
                UI.minigun_wait()
                if UI.reload_time < 0:
                    UI.auto_minigun_reload()

    if(RoomCol == 1 and RoomRow == 1):
        while(Instructions == True):
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            map1.render()
            player.render(ds)
            UI.render()
            Message2.render()
            pygame.display.update()
            if(keys[pygame.K_RETURN]):
                Instructions = False
    elif(RoomCol == 2 and RoomRow == 1):
        while(SwordInstructions == True):
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            map1.render()
            player.render(ds)
            UI.render()
            Message1.render()
            pygame.display.update()
            if(keys[pygame.K_RETURN]):
                SwordInstructions = False
    elif(RoomCol == 2 and RoomRow == 2 and player.swordOnly == True):
        while(PistalInstructions == True):
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            map1.render()
            player.render(ds)
            UI.render()
            Message.render()
            pygame.display.update()
            if(keys[pygame.K_RETURN]):
                PistalInstructions = False
        loot_dropper.items.append("pAmmo")
        UI.pistel = True
        player.swordOnly = False
    elif(RoomCol == 5 and RoomRow == 5 and UI.ShotGun == False):
        while(ShotgunInstructions1 == True):
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            map1.render()
            loot_dropper.render(ds)
            player.render(ds)
            UI.render()
            Message3.render()
            pygame.display.update()
            if(keys[pygame.K_RETURN]):
                ShotgunInstructions1 = False
        while(ShotgunInstructions2 == True):
            pygame.event.pump()
            keys=pygame.key.get_pressed()
            map1.render()
            loot_dropper.render(ds)
            player.render(ds)
            UI.render()
            Message4.render()
            pygame.display.update()
            if(keys[pygame.K_RETURN]):
                ShotgunInstructions2 = False
        loot_dropper.items.append("sAmmo")
        UI.ShotGun = True
    if textOn:
        Message.render()
    UI.render()
    #pygame.draw.rect(ds,(255,0,0),player.colliderect)
    pygame.display.update()
pygame.display.quit()

for file_name in os.listdir(r"NewRooms\\"):
    # construct full file path
    source = r"NewRooms\\" + file_name
    # copy only files
    if os.path.isfile(source):
        os.remove(source)
        #print('removed', file_name)
