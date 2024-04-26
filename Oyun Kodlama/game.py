import pygame
import math
import sys
import random

pygame.init() # for initializing pygame module

screen = pygame.display.set_mode((800, 600)) # width and height
pygame.display.set_caption("TAYYIP")
icon = pygame.image.load("akp_symbol.png")
pygame.display.set_icon(icon)

background_image = pygame.image.load("saray.jpg")
background_image = pygame.transform.scale(background_image , (800 , 600))

ezan_sound = pygame.mixer.Sound("ezan.wav")
bullet_sound = pygame.mixer.Sound("tekbir.mp3")
bullet_sound.set_volume(0.2)



#player ekleme
player_image = pygame.image.load("tayyip.png")
player_image = pygame.transform.scale(player_image , (170 , 170))
playerX = 300
playerY = 400
playerX_change = 0

# enemy ekleme kismi 
enemy_image = []
enemyX = []
enemyY = []
enemy_turn = []
enemyX_change = 0
num_of_enemys = 6
firstX_enemy = 10
for __ in range(num_of_enemys):
	sayi = random.randint(0, 100)
	if sayi < 25:
		foto = pygame.image.load("ekrem.png")
		enemy_image.append(pygame.transform.scale(foto , (170 , 170)))
	elif sayi <50:
		foto = pygame.image.load("kilicdaroglu.png")
		enemy_image.append(pygame.transform.scale(foto , (135 , 135)))
	elif sayi < 75:
		foto = pygame.image.load("mansur.png")
		enemy_image.append(pygame.transform.scale(foto , (250 , 140)))
	else:
		foto = pygame.image.load("ozgur.png")
		enemy_image.append(pygame.transform.scale(foto , (160 , 140)))
	enemyX.append(firstX_enemy)
	firstX_enemy += 100
	enemyY.append(0)
	enemy_turn.append(False)
	print(enemy_turn)

# ready you can't see the bullet on the screen
# fire bullet is currently on the moving
bullet_image = pygame.image.load("kuran.png")
bullet_image = pygame.transform.scale(bullet_image , (100 , 100))
bulletX = 0
bulletY = 400
bulletY_change = 10
bullet_state = "ready"

pygame.mixer.Sound.play(ezan_sound)
izmir_marsi = pygame.mixer.Sound("game_over.mp3")
izmir_marsi.set_volume(2)

## score kodu
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)
testX = 0
testY = 0

def show_score(testX , testY):
	score = font.render("Score: " + str(score_value) , True , (255 , 255 , 255))
	screen.blit(score , (testX , testY))

def player(x , y):
	screen.blit(player_image , (x , y))
def enemy(x , y , i):
	screen.blit(enemy_image[i] , (x , y))
def fire_bullet(x , y):
	global bullet_state  # now we can access the value of the bullet from here
	bullet_state = "fire"

	screen.blit(bullet_image , (x + 40, y + 10))
def is_collation(enemyX , enemyY , bulletX , bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX , 2) + math.pow(enemyY - bulletY , 2))
	if distance < 55:
		return True
	else:
		return False
running = True


while running:

	#screen.fill((0 , 255 , 0))
	#playerX += 1
	screen.blit(background_image , (0, 0))
	player(playerX , playerY)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change -= 2
			if event.key == pygame.K_RIGHT:
				playerX_change += 2
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(playerX , bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	playerX += playerX_change

	if playerX < 0 :
		playerX = 0
	if playerX > 600:
		playerX = 600
	for i in range(num_of_enemys):
		if enemy_turn[i] == False :
			enemyX[i] += 1
		elif enemy_turn[i] == True :
			enemyX[i] -= 1
		if enemyX[i] == 1 or enemyX[i] == 599:
			enemyY[i] += 10
			if enemy_turn[i] == False:
				enemy_turn[i] = True
			else:
				enemy_turn[i] = False
		collision = is_collation(enemyX[i] , enemyY[i] , bulletX , bulletY)
		if collision:
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemy_sound = pygame.mixer.Sound("kilicdaroglu_ses.mp3")
			enemy_sound.play()
			enemyX[i] = random.randint(1, 599)
			enemyY[i] = random.randint(0, 200)
			sayi = random.randint(0 , 100)
			if sayi < 25:
				foto = pygame.image.load("ekrem.png")
				enemy_image[i] = (pygame.transform.scale(foto , (170 , 170)))
			elif sayi <50:
				foto = pygame.image.load("kilicdaroglu.png")
				enemy_image[i] = (pygame.transform.scale(foto , (135 , 135)))
			elif sayi < 75:
				foto = pygame.image.load("mansur.png")
				enemy_image[i] = (pygame.transform.scale(foto , (250 , 140)))
			else:
				foto = pygame.image.load("ozgur.png")
				enemy_image[i] = (pygame.transform.scale(foto , (160 , 140)))

		enemy(enemyX[i] , enemyY[i] , i) 

		if enemyY[i] > 260:
			for a in range(num_of_enemys):
				enemyY[a] = 1500
			playerY = 1500
			ezan_sound.stop()
			izmir_marsi.play()
			game_over = font.render("LAIKLIK KAZANDI" , True , (0 , 0 , 0))
			background_image = pygame.image.load("ataturk.jpg")
			background_image = pygame.transform.scale(background_image , (800 , 600))
			screen.blit(game_over , (250 , 20))
	# bullet moving
	if bullet_state is "fire":
		fire_bullet(bulletX , bulletY)
		bulletY -= bulletY_change
	# bullet refire
	if bulletY < -60:
		bulletY = 350
		bullet_state = "ready"
	# collision

	#score table 
	show_score(testX , testY)


	
	pygame.display.update()