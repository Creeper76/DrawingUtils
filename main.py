import pygame
import sys
from screeninfo import get_monitors

# Initialize Pygame
pygame.init()

# Set the window size
monitor = get_monitors()[0]
width, height = monitor.width, monitor.height
window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Drawing")

# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set the clock
clock = pygame.time.Clock()

# Set the variables
drawing = False
button = 0
radius = 7
pos = (0, 0)

# Store the previous mouse position
prev_pos = None

# Draw "watermark" in bottom right corner
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 15)
made_with_love = font.render("Made with love by Creeper76 ", True, (255, 255, 255))
heart = font.render("<3", True, (255, 105, 180))
window.blit(made_with_love, (monitor.width - made_with_love.get_width() - heart.get_width() - 10, monitor.height - made_with_love.get_height() - 10))
window.blit(heart, (monitor.width - heart.get_width() - 10, monitor.height - heart.get_height() - 10))

def draw(r, isDrawing, drawCircle = False):
    global prev_pos

    # Get the current mouse position
    pos = pygame.Vector2(pygame.mouse.get_pos())

    if isDrawing != 1:
      pygame.draw.circle(window, black, (int(pos.x), int(pos.y)), int(r))
      prev_pos = None
      return

    # Normalize the mouse position
    norm_pos = pygame.Vector2(pos.x / window.get_width(), pos.y / window.get_height())

    # Interpolate between the colors of the rainbow
    hue = norm_pos.x * 360
    if hue < 0:
      hue = 0
    saturation = 100
    lightness = 20 + norm_pos.y * 60
    c = pygame.Color(0)
    c.hsla = (hue, saturation, lightness, 1)

    # Draw the line
    if drawCircle:
      pygame.draw.circle(window, c, pos, r/2)
    elif prev_pos is not None:
      pygame.draw.line(window, c, prev_pos, pos, r)
      pygame.draw.circle(window, c, prev_pos, r/2)
      pygame.draw.circle(window, c, pos, r/2)

    # Update the previous mouse position
    prev_pos = pos

# Main loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      drawing = True
      button = event.button
      if event.button == 1:  # Left mouse button.
        draw(radius, 1, True)
      elif event.button == 3:  # Right mouse button.
        draw(radius * 2, 0)
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
  clock.tick(240)
  print("FPS:", clock.get_fps())