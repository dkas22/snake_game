import pygame
import sys
from pygame.math import Vector2
import random


class SNAKE:
	def __init__(self):
		self.body = [Vector2(11,10), Vector2(10,10), Vector2(9,10)]
		self.direction = Vector2(0,0) # keep direction in which the snake has to move


		self.head_up = pygame.image.load("graphics/head_up.png")
		self.head_down = pygame.image.load("graphics/head_down.png")
		self.head_right = pygame.image.load("graphics/head_right.png")
		self.head_left = pygame.image.load("graphics/head_left.png")
		
		self.tail_up = pygame.image.load("graphics/tail_up.png")
		self.tail_down = pygame.image.load("graphics/tail_down.png")
		self.tail_right = pygame.image.load("graphics/tail_right.png")
		self.tail_left = pygame.image.load("graphics/tail_left.png")


		self.body_vertical = pygame.image.load("graphics/body_vertical.png")
		self.body_horizontal = pygame.image.load("graphics/body_horizontal.png")

		self.body_tr = pygame.image.load("graphics/body_tr.png")
		self.body_tl = pygame.image.load("graphics/body_tl.png")
		self.body_br = pygame.image.load("graphics/body_br.png")
		self.body_bl = pygame.image.load("graphics/body_bl.png")

		self.crunch_sound = pygame.mixer.Sound('sounds/crunch.wav')
		self.death_sound = pygame.mixer.Sound('sounds/death.wav')

	def draw_snake(self):
		# for block in self.body:
		# 	x_pos = block.x * cell_size
		# 	y_pos = block.y * cell_size
		# 	block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
		# 	pygame.draw.rect(screen, (183, 111, 122), block_rect)
		self.update_head_graphics() # create self.head attribute
		self.update_tail_graphics()

		for index, block in enumerate(self.body):
			x_pos = block.x * cell_size
			y_pos = block.y * cell_size
			block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

			# direction of head
			if index == 0:
				screen.blit(self.head, block_rect) #self.head attribute is used here created by update_head_graphics() above
			elif index == len(self.body)-1:
				screen.blit(self.tail, block_rect) 
			else:
				previous_block = self.body[index+1]- block
				next_block = self.body[index-1] - block

				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical, block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal, block_rect)
				else:
					if previous_block.x == -1 and next_block.y ==-1 or previous_block.y ==-1 and next_block.x == -1:
						screen.blit(self.body_tl, block_rect)
					elif previous_block.x == -1 and next_block.y ==1 or previous_block.y ==1 and next_block.x == -1:
						screen.blit(self.body_bl, block_rect)
					elif previous_block.x == 1 and next_block.y ==-1 or previous_block.y ==-1 and next_block.x == 1:
						screen.blit(self.body_tr, block_rect)
					else:
						screen.blit(self.body_br, block_rect)








	def update_head_graphics(self):

		snake_direction = self.body[0] - self.body[1]
		if snake_direction == Vector2(1,0):
			self.head = self.head_right
		elif snake_direction == Vector2(-1,0):
			self.head = self.head_left
		elif snake_direction == Vector2(0,1):
			self.head = self.head_down
		elif snake_direction == Vector2(0,-1):
			self.head = self.head_up

	def update_tail_graphics(self):

		tail_direction = self.body[-2] - self.body[-1]
		if tail_direction == Vector2(-1,0):
			self.tail = self.tail_right
		elif tail_direction == Vector2(1,0):
			self.tail = self.tail_left
		elif tail_direction == Vector2(0,-1):
			self.tail = self.tail_down
		elif tail_direction == Vector2(0,1):
			self.tail = self.tail_up




	def move_snake(self):
		if self.direction != Vector2(0,0):
			body_copy = self.body[:-1] # we don't want last element
			body_copy.insert(0, body_copy[0] + self.direction)
			self.body = body_copy[:] # returning back to body
	def add_block(self):
		body_copy = self.body[:]
		body_copy.insert(0, body_copy[0]+ self.direction)
		self.body = body_copy[:]

class FRUIT:
	def __init__(self):
		self.x = random.randint(0, cell_number-1)
		self.y = random.randint(0, cell_number-1)
		self.pos = Vector2(self.x, self.y)
		# create x and y
		# draw a square
	def draw_fruit(self):
		# Create a rectangle
		fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
		# draw the rectangle
		# pygame.draw.rect(screen,(126,166,114) , fruit_rect)
		screen.blit(apple, fruit_rect)
	def randomize(self):
		self.x = random.randint(0, cell_number-1)
		self.y = random.randint(0, cell_number-1)
		self.pos = Vector2(self.x, self.y)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		file = open("high_score.txt", "rt")
		self.high_score = int(file.read())
		file.close()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_element(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			# reposition fruit
			self.fruit.randomize()
			# add another block to the snake
			self.snake.add_block()
			self.play_crunch_sound()

			for block in self.snake.body[1:]:
				if block == self.fruit.pos:
					self.fruit.randomize()

	def check_fail(self):
		# check if snake hits the wall
		if not 0 <= self.snake.body[0].x <cell_number or not 0 <= self.snake.body[0].y <cell_number:
			self.play_death_sound()
			self.game_over()
		# check if snake hits itself
		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.play_death_sound()
				self.game_over()
				break

	def game_over(self):
		file = open("high_score.txt", "w")
		file.write(str(self.high_score))
		file.close()
		self.snake.body = [Vector2(11,10), Vector2(10,10), Vector2(9,10)]
		self.snake.direction = Vector2(0,0)
		# self.play_death_sound()

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row%2==0:
				for col in range(cell_number):
					if col%2== 0:
						grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)
						# screen.blit(grass2, grass_rect)
					# else:
					# 	grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
					# 	# pygame.draw.rect(screen, grass_color, grass_rect)
					# 	screen.blit(grass1, grass_rect)

			else:
				for col in range(cell_number):
					if col%2 != 0:
						grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)
						# screen.blit(grass2, grass_rect)
					# else:
					# 	grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
					# 	# pygame.draw.rect(screen, grass_color, grass_rect)
					# 	screen.blit(grass1, grass_rect)


	def draw_score(self):
		current_score = (len(self.snake.body)-3)*5
		score_text = "Score : " + str(current_score)
		score_surface = score_font.render(score_text, True, (56,74, 12))
		score_x = int(cell_size * cell_number -80)
		score_y = int(30)

		score_rect = score_surface.get_rect(center = (score_x, score_y))
		screen.blit(score_surface, score_rect)

		if current_score > self.high_score:
			self.high_score = current_score
		high_score_text = "High Score : " + str(self.high_score)
		high_score_surface = high_score_font.render(high_score_text, True, (56,74, 12))
		high_score_x = 90
		high_score_y = 30

		high_score_rect = high_score_surface.get_rect(center = (high_score_x, high_score_y))
		screen.blit(high_score_surface, high_score_rect)
	def play_crunch_sound(self):
		self.snake.crunch_sound.play()

	def play_death_sound(self):
		self.snake.death_sound.play()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


cell_size = 40 #each cell be 40*40 pixel
cell_number = 20 
screen = pygame.display.set_mode((cell_size * cell_number, cell_number*cell_size))
clock = pygame.time.Clock()
FPS = 60 # frame per second
font_size = 20


apple = pygame.image.load("graphics/apple.png")
apple = pygame.transform.scale(apple, (40, 40))

grass1 = pygame.image.load("graphics/grass1.jpg")
grass1 = pygame.transform.scale(grass1, (40, 40))


grass2 = pygame.image.load("graphics/grass2.jpg")
grass2 = pygame.transform.scale(grass2, (40, 40))

score_font = pygame.font.Font('fonts/PoetsenOne-Regular.ttf', font_size)
high_score_font = pygame.font.Font('fonts/PoetsenOne-Regular.ttf', font_size)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 60)


finished = False
while not finished:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y !=1:
					main_game.snake.direction = Vector2(0, -1)
			elif event.key == pygame.K_DOWN:
				if main_game.snake.direction.y !=-1:
					main_game.snake.direction = Vector2(0, 1)
			elif event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x !=-1:
					main_game.snake.direction = Vector2(1, 0)
			elif event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1, 0)
	screen.fill((170,215,70))
	main_game.draw_element()
	pygame.display.update()
	clock.tick(60)


