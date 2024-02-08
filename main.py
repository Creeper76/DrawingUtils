import pygame
import sys
from screeninfo import get_monitors

# Initialize Pygame
pygame.init()

# Set the window size
monitor = get_monitors()[0]
width, height = monitor.width, monitor.height
window = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Drawing")

# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set the clock
clock = pygame.time.Clock()

# Set the variables
drawing = False
rainbow = False
button = 0
radius = 7
pos = (0, 0)

# Store the previous mouse position
prev_pos = None

def draw(r, isDrawing, drawCircle = False):
    global prev_pos

    # Get the current mouse position
    pos = pygame.Vector2(pygame.mouse.get_pos())

    if isDrawing != 1 and not rainbow:
      pygame.draw.circle(window, black, (int(pos.x), int(pos.y)), int(r))
      prev_pos = None
      return
    elif isDrawing != 1 and rainbow:
      c = get_color_from_pos(pos)
      for x in range (int(pos.x) - r*2, int(pos.x) + r*2, 7):
        for y in range (int(pos.y) - r*2, int(pos.y) + r*2, 7):
          draw_with_pos(x, y, 7)
      prev_pos = None
      return
    
    if rainbow and not drawCircle and prev_pos is not None:
      pygame.draw.line(window, white, prev_pos, pos, r)
      pygame.draw.circle(window, white, prev_pos, r/2)
      pygame.draw.circle(window, white, pos, r/2)
      prev_pos = pos
      return
    elif rainbow and drawCircle:
      pygame.draw.circle(window, white, pos, r/2)
      prev_pos = pos
      return

    c = get_color_from_pos(pos)

    # Draw the line
    if drawCircle:
      pygame.draw.circle(window, c, pos, r/2)
    elif prev_pos is not None:
      pygame.draw.line(window, c, prev_pos, pos, r)
      pygame.draw.circle(window, c, prev_pos, r/2)
      pygame.draw.circle(window, c, pos, r/2)

    # Update the previous mouse position
    prev_pos = pos
    
def draw_with_pos(x, y, r):
  c = get_color_from_pos(pygame.Vector2(x, y))
  pygame.draw.circle(window, c, (x, y), r)
    
def get_color_from_pos(pos):
  # Normalize the mouse position
  norm_pos = pygame.Vector2(pos.x / window.get_width(), pos.y / window.get_height())

  # Interpolate between the colors of the rainbow
  hue = norm_pos.x * 360
  if hue < 0:
    hue = 0
  elif hue > 360:
    hue = 360
  saturation = 100
  lightness = 20 + norm_pos.y * 60
  c = pygame.Color(0)
  c.hsla = (hue, saturation, lightness, 1)
  return c

# Main loop
while True:
  for event in pygame.event.get():
    # Handle closing the window
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
      pygame.quit()
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      # C to clear the screen
      if event.key == pygame.K_c:
        window.fill(black)
        rainbow = False
      
      # W to make the screen white
      elif event.key == pygame.K_w:
        window.fill(white)
        rainbow = False
        
      # R to make the screen rainbow
      elif event.key == pygame.K_r:
        for x in range(0, width, 7):
          for y in range(0, height, 7):
            draw_with_pos(x, y, 7)
        rainbow = True
      
    # Checks for mouse button events
    if event.type == pygame.MOUSEBUTTONDOWN:
      drawing = True
      button = event.button
      if event.button == 1:  # Left mouse button.
        draw(radius, 1, True)
      elif event.button == 3:  # Right mouse button.
        draw(radius * 2, 0)
        
      # Middle scroll wheel to change the radius
      elif event.button == 4:
        radius += 1  # Scrolling up
      elif event.button == 5:
        radius -= 1  # Scrolling down
        if radius < 1:
          radius = 1
    elif event.type == pygame.MOUSEBUTTONUP:
      drawing = False
      prev_pos = None
    
    # Draw while the mouse is moving
    if event.type == pygame.MOUSEMOTION and drawing:
      # Check the type of button
      case = button
      if case == 1:
        draw(radius, 1)
      elif case == 3:
        draw(radius * 3, 0)
      else:
        pass

  # Draw
  pygame.display.flip()
  clock.tick(512)
  print("FPS:", clock.get_fps())