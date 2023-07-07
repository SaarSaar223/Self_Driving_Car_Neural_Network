import pygame
import time
import math
import utils
import neat
from Car import Car
import sys


current_generation = 0 # Generation counter
BORDER_COLOR = (111,112,116) # Color To Crash on Hit

current_generation = 0 # Generation counter

TRACK = utils.scale_image(pygame.image.load("imgs/track.png"), 1)
TRACK_BORDER = utils.scale_image(pygame.image.load("imgs/track-border.png"), 1)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
CAR = utils.scale_image(pygame.image.load("imgs/car.png"), 0.4)
FPS = 60
BORDER_COLOR = (111,112,116)

CAR_SIZE_X = CAR.get_width()    
CAR_SIZE_Y = CAR.get_height()
WIDTH = TRACK.get_width()
HEIGHT = TRACK.get_height()

def run_simulation(genomes, config):
    
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load('imgs/track.png') # Convert Speeds Up A Lot

    global current_generation
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))  
            if choice == 0:
                car.angle += 3 # Left
            elif choice == 1:
                car.angle -= 3 # Right
            elif choice == 2:
                if(car.speed - .4 >= 2):
                    car.speed -= .4 # Slow Down
            else:
                if(car.speed + .4 <= 6):
                    car.speed += .4 # Speed Up
        
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update()
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 90: 
            break

        # Draw Map And All Cars That Are Alive
        screen.fill((255,255,255))
        screen.blit(game_map, (0, 0))
        for car in cars:
            if car.is_alive():
                car.draw(screen)
        
        # Generation and Still Alive Information
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (100, 790)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (100, 820)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)


