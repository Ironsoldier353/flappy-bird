import pygame
import random
pygame.init()

# Screen setup
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors and fonts
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.gravity = 0.6
        self.lift = -10
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def jump(self):
        self.velocity = self.lift

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, int(self.y)), 15)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = 50
        self.gap = 150
        self.top = random.randint(50, SCREEN_HEIGHT // 2)
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.top + self.gap, self.width, SCREEN_HEIGHT - self.top - self.gap))

    def offscreen(self):
        return self.x < -self.width

# Initialize game objects
bird = Bird()
pipes = [Pipe()]
score = 0
running = True

# Main game loop
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    
    bird.update()
    bird.draw()
    
    for pipe in pipes:
        pipe.update()
        pipe.draw()
        if (pipe.x < bird.x < pipe.x + pipe.width and 
                (bird.y < pipe.top or bird.y > pipe.top + pipe.gap)):
            running = False  # Collision detection
        
        if pipe.offscreen():
            pipes.remove(pipe)
            pipes.append(Pipe())
            score += 1
    
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.update()  # Ensures compatibility with web rendering
    clock.tick(30)

pygame.quit()
