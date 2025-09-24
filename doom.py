import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Get display info for fullscreen
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Window setup - fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Cursors")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
DOOM_RED = (180, 0, 0)
DOOM_DARK_RED = (120, 0, 0)

# Font setup
font = pygame.font.Font(None, int(HEIGHT * 0.08))  # Scale font with screen size
small_font = pygame.font.Font(None, int(HEIGHT * 0.04))
# Large font for Doom-style title
doom_font = pygame.font.Font(None, int(HEIGHT * 0.2))

# Game state
game_started = False

# Number of cursors (one for real mouse + virtual mice)
NUM_CURSORS = 10  # Reduced for better performance and realistic mouse count
cursors = []

# Virtual mice tracking (simulating multiple mouse inputs)
virtual_mice = []

# Function to generate random color
def random_color():
	return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Function to create cursor surface with color
def create_cursor_surface(color):
	surface = pygame.Surface((int(WIDTH * 0.02), int(WIDTH * 0.02)), pygame.SRCALPHA)
	pygame.draw.polygon(surface, color, [(0, 0), (0, int(WIDTH * 0.015)), (int(WIDTH * 0.006), int(WIDTH * 0.01)), (int(WIDTH * 0.012), int(WIDTH * 0.025)), (int(WIDTH * 0.015), int(WIDTH * 0.022)), (int(WIDTH * 0.009), int(WIDTH * 0.011)), (int(WIDTH * 0.018), int(WIDTH * 0.011))])
	return surface

# Function to create start button
def create_start_button():
	button_width = int(WIDTH * 0.25)
	button_height = int(HEIGHT * 0.08)
	button_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - button_height//2, button_width, button_height)
	return button_rect

# Function to draw Doom-style text with shadow effect
def draw_doom_text(surface, text, font, color, shadow_color, x, y):
	# Draw shadow first (offset slightly)
	shadow_text = font.render(text, True, shadow_color)
	surface.blit(shadow_text, (x + 5, y + 5))
	
	# Draw main text
	main_text = font.render(text, True, color)
	surface.blit(main_text, (x, y))

# Function to calculate distance between two points
def distance(x1, y1, x2, y2):
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Initialize virtual mice
def initialize_virtual_mice():
	global virtual_mice
	virtual_mice = []
	
	# One less virtual mouse since we'll use the real mouse for cursor 0
	for i in range(NUM_CURSORS - 1):
		# Each virtual mouse starts at a different position
		start_x = random.randint(int(WIDTH * 0.1), int(WIDTH * 0.9))
		start_y = random.randint(int(HEIGHT * 0.1), int(HEIGHT * 0.9))
		
		# Virtual mouse data: [x, y, dx, dy, last_update_time]
		virtual_mice.append([start_x, start_y, 0, 0, 0])

# Initialize cursors in a circle
def initialize_cursors_in_circle():
	global cursors
	cursors = []
	center_x, center_y = WIDTH // 2, HEIGHT // 2
	radius = min(WIDTH, HEIGHT) * 0.2  # Scale radius with screen size
	
	for i in range(NUM_CURSORS):
		# Calculate position in circle
		angle = (2 * math.pi * i) / NUM_CURSORS
		x = center_x + radius * math.cos(angle) - int(WIDTH * 0.01)  # Offset for cursor center
		y = center_y + radius * math.sin(angle) - int(WIDTH * 0.01)
		
		# Initialize cursor data
		# [x, y, target_x, target_y, cursor_surface, rotation_angle, rotation_speed, mouse_id, following_mouse, is_real_mouse]
		color = random_color()
		cursor_surface = create_cursor_surface(color)
		rotation_angle = random.uniform(0, 360)
		rotation_speed = random.uniform(-3, 3)
		mouse_id = i
		is_real_mouse = (i == 0)  # First cursor follows real mouse
		cursors.append([x, y, x, y, cursor_surface, rotation_angle, rotation_speed, mouse_id, False, is_real_mouse])

# Update virtual mice positions
def update_virtual_mice():
	import time
	current_time = time.time()
	
	for i, mouse in enumerate(virtual_mice):
		# Add some random movement to virtual mice
		if current_time - mouse[4] > 0.1:  # Update every 0.1 seconds
			mouse[2] = random.uniform(-2, 2)  # dx
			mouse[3] = random.uniform(-2, 2)  # dy
			mouse[4] = current_time
		
		# Update position
		mouse[0] += mouse[2]
		mouse[1] += mouse[3]
		
		# Keep within screen bounds
		mouse[0] = max(0, min(WIDTH, mouse[0]))
		mouse[1] = max(0, min(HEIGHT, mouse[1]))

# Initialize virtual mice and cursors
initialize_virtual_mice()
initialize_cursors_in_circle()

# Game loop
clock = pygame.time.Clock()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if not game_started:
				button_rect = create_start_button()
				if button_rect.collidepoint(event.pos):
					# Start the game - assign cursors to follow mice
					game_started = True
					# Hide the OS mouse cursor after starting
					pygame.mouse.set_visible(False)
					for i, c in enumerate(cursors):
						if c[9]:  # if is_real_mouse
							# First cursor follows real mouse
							mouse_pos = pygame.mouse.get_pos()
							c[2] = mouse_pos[0]  # target_x
							c[3] = mouse_pos[1]  # target_y
						else:
							# Other cursors follow virtual mice
							virtual_mouse_idx = i - 1  # Adjust index for virtual mice
							if virtual_mouse_idx < len(virtual_mice):
								c[2] = virtual_mice[virtual_mouse_idx][0]  # target_x
								c[3] = virtual_mice[virtual_mouse_idx][1]  # target_y
						c[8] = True  # following_mouse = True

	screen.fill(BLACK)

	# Draw Doom-style "CURSORS" background title
	cursors_text_x = WIDTH // 2 - int(WIDTH * 0.25)
	cursors_text_y = int(HEIGHT * 0.08)
	draw_doom_text(screen, "CURSORS", doom_font, DOOM_RED, DOOM_DARK_RED, cursors_text_x, cursors_text_y)

	if not game_started:
		# Draw start button
		button_rect = create_start_button()
		button_color = DARK_GREEN if button_rect.collidepoint(pygame.mouse.get_pos()) else GREEN
		pygame.draw.rect(screen, button_color, button_rect)
		pygame.draw.rect(screen, WHITE, button_rect, 3)
		
		start_text = small_font.render("START", True, WHITE)
		start_rect = start_text.get_rect(center=button_rect.center)
		screen.blit(start_text, start_rect)
		
		# Draw instructions
		instructions = small_font.render("Click START - your mouse becomes a cursor!", True, WHITE)
		instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT//2 + int(HEIGHT * 0.08)))
		screen.blit(instructions, instructions_rect)
		
		# Draw ESC instruction
		esc_instruction = small_font.render("Press ESC to exit", True, WHITE)
		esc_rect = esc_instruction.get_rect(center=(WIDTH//2, HEIGHT - int(HEIGHT * 0.05)))
		screen.blit(esc_instruction, esc_rect)
		
		# Draw cursors in circle (static)
		for c in cursors:
			# Just rotate, don't move
			c[5] += c[6]  # angle += rotation_speed
			
			# Keep angle between 0 and 360
			if c[5] >= 360:
				c[5] -= 360
			elif c[5] < 0:
				c[5] += 360
			
			# Rotate cursor surface
			rotated_cursor = pygame.transform.rotate(c[4], c[5])
			
			# Get the center of the rotated surface for proper positioning
			rect = rotated_cursor.get_rect()
			rect.center = (c[0] + int(WIDTH * 0.01), c[1] + int(WIDTH * 0.01))
			
			screen.blit(rotated_cursor, rect)
	
	else:
		# Update virtual mice positions
		update_virtual_mice()
		
		# Game is running - cursors follow their assigned mice
		for i, c in enumerate(cursors):
			# Update rotation
			c[5] += c[6]  # angle += rotation_speed
			
			# Keep angle between 0 and 360
			if c[5] >= 360:
				c[5] -= 360
			elif c[5] < 0:
				c[5] += 360
			
			# Each cursor follows its assigned mouse
			if c[8]:  # if following_mouse
				if c[9]:  # if is_real_mouse
					# First cursor follows real mouse position
					mouse_pos = pygame.mouse.get_pos()
					target_x = mouse_pos[0]
					target_y = mouse_pos[1]
				else:
					# Other cursors follow virtual mice
					virtual_mouse_idx = i - 1  # Adjust index for virtual mice
					if virtual_mouse_idx < len(virtual_mice):
						target_x = virtual_mice[virtual_mouse_idx][0]
						target_y = virtual_mice[virtual_mouse_idx][1]
					else:
						continue
				
				# Add small offset to make cursors slightly offset from mouse positions (except for real mouse)
				if not c[9]:  # Don't offset the real mouse cursor
					offset_distance = int(WIDTH * 0.02) + (i * 3)
					offset_angle = (2 * math.pi * i) / NUM_CURSORS
					offset_x = offset_distance * math.cos(offset_angle)
					offset_y = offset_distance * math.sin(offset_angle)
					
					target_x += offset_x
					target_y += offset_y
				
				# Smooth interpolation towards target (faster for real mouse)
				speed = 0.3 if c[9] else 0.15
				c[0] += (target_x - c[0]) * speed
				c[1] += (target_y - c[1]) * speed
				
				# Keep cursors within screen bounds
				c[0] = max(int(WIDTH * 0.01), min(WIDTH - int(WIDTH * 0.01), c[0]))
				c[1] = max(int(WIDTH * 0.01), min(HEIGHT - int(WIDTH * 0.01), c[1]))
			
			# Rotate cursor surface
			rotated_cursor = pygame.transform.rotate(c[4], c[5])
			
			# Get the center of the rotated surface for proper positioning
			rect = rotated_cursor.get_rect()
			rect.center = (c[0] + int(WIDTH * 0.01), c[1] + int(WIDTH * 0.01))
			
			screen.blit(rotated_cursor, rect)
		
		# Draw instructions
		instructions = small_font.render("Your mouse is now a cursor! Move it around!", True, WHITE)
		instructions_rect = instructions.get_rect(center=(WIDTH//2, HEIGHT - int(HEIGHT * 0.05)))
		screen.blit(instructions, instructions_rect)

	pygame.display.flip()
	clock.tick(60)
