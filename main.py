import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    # Create the main game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0 # Delta time (time elapsed per frame)
    
    # Sprite groups
    updatable = pygame.sprite.Group() # Objects that need updating each frame
    drawable = pygame.sprite.Group() # Objects that need to be drawn
    asteroids = pygame.sprite.Group() # Asteroids only
    shots = pygame.sprite.Group() # Player shots

    # Assign containers for automatic sprite registration
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    # Create main game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return # Exit the game cleanly
            
        updatable.update(dt) # Update all objects

        # Check collisions 
        for asteroid in asteroids:
            if asteroid.collision_check(player): # Between each asteroids and the player
                print("GAME OVER")
                pygame.quit()
                sys.exit()
            for shot in shots: # Between each shot and the asteroid.
                if asteroid.collision_check(shot):
                    asteroid.split()
                    shot.kill()

        screen.fill("black") # Clear screen

        # Draw all drawable objects
        for item in drawable:
            item.draw(screen)

        pygame.display.flip() # Flip the display buffer
        dt = clock.tick(60) / 1000 # Limit FPS and calculate delta time in seconds
        

if __name__ == "__main__":
    main()
