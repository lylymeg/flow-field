import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flow Field Particle Simulation (Generative Art)")
clock = pygame.time.Clock()

# Couleurs (Fond sombre, particules aux teintes néon/cyan)
DARK_BG = (10, 12, 18)
WHITE = (255, 255, 255)
GRAY = (120, 130, 150)

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = 0.0
        self.vy = 0.0
        self.max_speed = random.uniform(2.0, 4.5)
        self.color = random.choice([
            (0, 210, 255),  # Cyan
            (0, 255, 157),  # Vert menthe
            (120, 100, 255),# Violet électrique
            (255, 140, 0)   # Orange flamboyant
        ])
        self.lifespan = random.randint(150, 350)
        self.age = 0

    def update(self, z_offset):
        # Calculer l'angle du champ vectoriel en fonction de la position (bruit mathématique fluide)
        scale = 0.003
        angle = math.sin(self.x * scale + z_offset) * math.cos(self.y * scale - z_offset) * math.pi * 4

        # Convertir l'angle en force de direction
        self.vx = math.cos(angle) * self.max_speed
        self.vy = math.sin(angle) * self.max_speed

        self.x += self.vx
        self.y += self.vy
        self.age += 1

        # Si la particule sort de l'écran ou arrive en fin de vie, on la régénère ailleurs
        if not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT) or self.age > self.lifespan:
            self.x = random.uniform(0, WIDTH)
            self.y = random.uniform(0, HEIGHT)
            self.age = 0
            self.lifespan = random.randint(150, 350)

    def draw(self, surface):
        # Dessiner un petit trait ou un point pour créer un effet de sillage
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 2)

# Initialisation des particules
particles = [Particle() for _ in range(1200)]
z_offset = 0.0

# Surface semi-transparente pour créer l'effet de traînée (motion blur artistique)
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
trail_surface.fill((10, 12, 18, 25)) # Transparence pour laisser les traînées s'effacer lentement

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Régénérer toutes les particules
                particles = [Particle() for _ in range(1200)]

    # Faire évoluer lentement le champ vectoriel au fil du temps
    z_offset += 0.012

    # Effet de fondu progressif sur l'écran pour les traînées
    screen.fill(DARK_BG)

    # Mise à jour et dessin des particules
    for p in particles:
        # Si on clique, la souris attire ou repousse les particules
        if mouse_pressed[0] and mouse_pos[1] > 70:
            dx = mouse_pos[0] - p.x
            dy = mouse_pos[1] - p.y
            dist = math.hypot(dx, dy)
            if dist < 150:
                p.x -= (dx / dist) * 2.5
                p.y -= (dy / dist) * 2.5

        p.update(z_offset)
        p.draw(screen)

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("FLOW FIELD — ART GÉNÉRATIF & SIMULATION DE FLUX", True, WHITE)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 15))

    inst_txt = font_small.render("CLIC GAUCHE (maintenir) : Répulser les particules | R : Réinitialiser", True, GRAY)
    screen.blit(inst_txt, (WIDTH // 2 - inst_txt.get_width() // 2, 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()