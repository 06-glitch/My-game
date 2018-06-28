import pygame
import random
import math 

pygame.init()

#constants
screen_width=1000
screen_height=600
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
black=(0,0,0)
white=(255,255,255)
colors=[red,green,blue,black,white]
background=pygame.image.load("background.jpg")
font=pygame.font.SysFont("Bookman",60)
small_font=pygame.font.SysFont("comicsansms",40)
ball=pygame.image.load("ball.png")
ball_width=ball.get_rect().width
ball_height=ball.get_rect().height
convert=180/math.pi
crash_sound=pygame.mixer.Sound("crash.wav")
clock=pygame.time.Clock()

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("My game")

def inside(center,radius,point):
	return (point[0]-center[0])**2+(point[1]-center[1])**2<radius*radius

def intersect(vertical_acceleration,b,center,radius):
	if vertical_acceleration[0]==b[0]:
		if center[0]-radius<vertical_acceleration[0]<center[0]+radius:
			return min(vertical_acceleration[1],b[1])<center[1]<max(vertical_acceleration[1],b[1])
		else:
			return False
	else:
		if center[1]-radius<vertical_acceleration[1]<center[1]+radius:
			return min(vertical_acceleration[0],b[0])<center[0]<max(vertical_acceleration[0],b[0])
		else:
			return False


def collided(square,center,radius):
	for i in square:
		if inside(center,radius,i):
			return True
	for i in range(4):
		if intersect(square[i],square[(i+1)%4],center,radius):
			return True
	return False

def button(x,y,w,h,font,message,messagecolor,inactive,active,action):
	text=font.render(message,True,messagecolor)
	pos=pygame.mouse.get_pos()
	pressed=pygame.mouse.get_pressed()
	if x<pos[0]<x+w and y<pos[1]<y+h:
		if isinstance(active,pygame.Surface):
			screen.blit(pygame.transform.scale(active,(w,h)),(x,y))
		else:
			pygame.draw.rect(screen,active,(x,y,w,h))
		if pressed[0]==1:
			action()
	else:
		if isinstance(inactive,pygame.Surface):
			screen.blit(pygame.transform.scale(inactive,(w,h)),(x,y))
		else:
			pygame.draw.rect(screen,inactive,(x,y,w,h))
	screen.blit(text,text.get_rect(center=(x+w//2,y+h//2)))

def controls():
	while 1:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_quit()
		screen.blit(pygame.transform.scale(background,(screen_width,screen_height)),(0,0))
		text=small_font.render("The objective of this game is to avoid as many blocks as possible.",True,(0,0,200))
		screen.blit(text,(50,50))
		text=small_font.render("Left Arrow Key: Move Left",True,(0,0,200))
		screen.blit(text,(250,150))
		text=small_font.render("Right Arrow Key: Move Right",True,(0,0,200))
		screen.blit(text,(250,250))
		text=small_font.render("Spacebar: Jump",True,(0,0,200))
		screen.blit(text,(300,350))
		text=small_font.render("P: Pause game",True,(0,0,200))
		screen.blit(text,(320,450))
		button(50,screen_height-150,150,50,font,"Back",white,(75,150,0),(75,225,0),gameintro)
		pygame.display.update()
		clock.tick(15)

def game_quit():
	pygame.quit()
	quit()

p=1

def start():
	pygame.mixer.music.unpause()
	global p
	p=0

def pause():
	pygame.mixer.music.pause()
	global p
	p=1
	while p:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_quit()
		screen.blit(pygame.transform.scale(background,(screen_width,screen_height)),(0,0))
		button(screen_width/2-100,100,250,100,font,"Continue",black,(0,150,0),green,start)
		button(screen_width/2-100,300,250,100,font,"Quit",black,(150,0,0),red,game_quit)
		pygame.display.update()
		clock.tick(15)

def play():
	pygame.mixer.music.load("music.mp3")
	pygame.mixer.music.play(-1)
	x_velocity=0
	y_velocity=0
	angular_velocity=0
	jump=0
	vertical_acceleration=6
	horizontal_acceleration=0
	x=350
	y=screen_height-ball_height-10
	angle=0
	rect=ball.get_rect()
	n_blocks=4
	obstacle_speed=[10]*n_blocks
	block_size,x_obstacle,y_obstacle,color=[],[],[],[]
	for i in range(n_blocks):
		block_size.append(random.randint(30,40))
		x_obstacle.append(random.randint(0,screen_width-block_size[i]))
		y_obstacle.append(random.randint(-800,-200))
		color.append(random.choice(colors))
	bullet_width=25
	x_bullet=random.randint(-600,-200)
	y_bullet=screen_height-bullet_width-10
	bullet_speed=8
	bullet_direction=1
	score=0

	while 1:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_quit()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					x_velocity=-5
					angular_velocity=(-x_velocity/(ball_width/2))*convert
					horizontal_acceleration=-0.2
				if event.key==pygame.K_RIGHT:
					x_velocity=5
					angular_velocity=(-x_velocity/(ball_width/2))*convert
					horizontal_acceleration=0.2
				if event.key==pygame.K_SPACE:
					if jump==0:
						y_velocity=-55
						jump=1
				if event.key==pygame.K_p:
					pause()

			if event.type==pygame.KEYUP:
				if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
					horizontal_acceleration=0
					x_velocity=0
					angular_velocity=0
		
		if x_velocity:
			x_velocity+=horizontal_acceleration
			if x_velocity>10:
				x_velocity=10
			angular_velocity=(-x_velocity/(ball_width/2))*convert

		x+=x_velocity
		angle+=angular_velocity
		
		if jump:
			y+=y_velocity
			y_velocity+=vertical_acceleration
		
		if x<0:
			x=0
		if x>screen_width-ball_width:
			x=screen_width-ball_width
		
		if y>screen_height-ball_height-10:
			y=screen_height-ball_height-10
			jump=0
		
		screen.blit(pygame.transform.scale(background,(screen_width,screen_height)),(0,0))
		
		for i in range(n_blocks):
			pygame.draw.rect(screen,color[i],(x_obstacle[i],y_obstacle[i],block_size[i],block_size[i]))
		
		pygame.draw.rect(screen,black,(x_bullet,y_bullet,bullet_width,bullet_width))
		
		rotate=pygame.transform.rotate(ball,angle)
		rect.x=x
		rect.y=y
		screen.blit(rotate,rotate.get_rect(center=rect.center))
		
		for i in range(n_blocks):
			square=[(x_obstacle[i],y_obstacle[i]),(x_obstacle[i]+block_size[i],y_obstacle[i]),(x_obstacle[i]+block_size[i],y_obstacle[i]+block_size[i]),(x_obstacle[i],y_obstacle[i]+block_size[i])]
			if collided(square,rect.center,ball_width/2):
				crash(background,score)

		square=[(x_bullet,y_bullet),(x_bullet+bullet_width,y_bullet),(x_bullet+bullet_width,y_bullet+bullet_width),(x_bullet,y_bullet+bullet_width)]
		if collided(square,rect.center,ball_width/2):
				crash(background,score)

		text=font.render("Score: "+str(score),True,red)
		screen.blit(text,(10,10))

		pygame.display.update()
		
		for i in range(n_blocks):
			y_obstacle[i]+=obstacle_speed[i]
			if y_obstacle[i]>screen_height-block_size[i]-10:
				score+=1
				obstacle_speed[i]+=0.5
				if obstacle_speed[i]>15:
					obstacle_speed[i]=random.randint(12,15)
				block_size[i]+=5
				if block_size[i]>100:
					block_size[i]=random.randint(50,100)
				x_obstacle[i]=random.randint(0,screen_width-block_size[i])
				y_obstacle[i]=random.randint(-800,-200)
				color[i]=random.choice(colors)

		x_bullet+=(bullet_direction*bullet_speed)
		if (x_bullet>screen_width-bullet_width and bullet_direction==1) or (x_bullet<0 and bullet_direction==-1):
			bullet_direction=random.choice([-1,1])
			if bullet_direction==1:
				x_bullet=random.randint(-600,-400)
			else:
				x_bullet=random.randint(1300,1500)
			bullet_speed+=(score//50)

		clock.tick(45)

def crash(background,score):
	pygame.mixer.Sound.play(crash_sound)
	pygame.mixer.music.stop()
	while 1:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_quit()
		if isinstance(background,pygame.Surface):
			screen.blit(pygame.transform.scale(background,(screen_width,screen_height)),(0,0))
		else:
			screen.fill(background)
		text=font.render("You score is "+str(score),True,blue)
		screen.blit(text,(380,100))
		button(screen_width/2-100,250,250,100,font,"Play Again",black,(0,150,0),green,play)
		button(screen_width/2-100,400,250,100,font,"Quit",black,(150,0,0),red,game_quit)
		pygame.display.update()
		clock.tick(15)

def gameintro(background=background):
	while 1:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				game_quit()
		if isinstance(background,pygame.Surface):
			screen.blit(pygame.transform.scale(background,(screen_width,screen_height)),(0,0))
		else:
			screen.fill(background)
		button(screen_width/2-100,100,200,100,font,"Play",black,(0,150,0),green,play)
		button(screen_width/2-100,250,200,100,font,"Controls",black,(0,0,150),blue,controls)
		button(screen_width/2-100,400,200,100,font,"Quit",black,(150,0,0),red,game_quit)
		pygame.display.update()
		clock.tick(15)

gameintro(background)



