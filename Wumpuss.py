import pygame
import random

# Define constants
CELL_SIZE = 50
GRID_SIZE = 4
WINDOW_SIZE = CELL_SIZE * GRID_SIZE

class WumpusWorld:
    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.agent_position = (0, 0)
        self.wumpus_position = self.generate_random_position()
        self.gold_position = self.generate_random_position()
        self.pit_positions = [self.generate_random_position() for _ in range(size)]
        self.is_game_over = False
        self.has_gold = False

    def generate_random_position(self):
        return random.randint(0, self.size - 1), random.randint(0, self.size - 1)

    def move_agent(self, action):
        if action == "up" and self.agent_position[0] > 0:
            self.agent_position = (self.agent_position[0] - 1, self.agent_position[1])
        elif action == "down" and self.agent_position[0] < self.size - 1:
            self.agent_position = (self.agent_position[0] + 1, self.agent_position[1])
        elif action == "left" and self.agent_position[1] > 0:
            self.agent_position = (self.agent_position[0], self.agent_position[1] - 1)
        elif action == "right" and self.agent_position[1] < self.size - 1:
            self.agent_position = (self.agent_position[0], self.agent_position[1] + 1)

    def check_perceptions(self):
        percept = ""
        if self.agent_position == self.wumpus_position:
            percept += "You smell a terrible stench! "
        if self.agent_position in self.pit_positions:
            percept += "You feel a breeze! "
        if self.agent_position == self.gold_position:
            percept += "You see a glitter! "
        return percept

    def take_action(self, action):
        self.move_agent(action)
        percept = self.check_perceptions()

        if self.agent_position == self.wumpus_position or self.agent_position in self.pit_positions:
            self.is_game_over = True
            percept += "Game Over! You were caught by the Wumpus or fell into a pit."
        elif self.agent_position == self.gold_position:
            self.has_gold = True
            self.is_game_over = True
            percept += "You found the gold! You win!"

        return percept


def draw_grid(screen):
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (WINDOW_SIZE, y))


def draw_elements(screen, world):
    for row in range(world.size):
        for col in range(world.size):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if (row, col) == world.agent_position:
                pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))
            elif (row, col) == world.wumpus_position:
                pygame.draw.rect(screen, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))
            elif (row, col) == world.gold_position:
                pygame.draw.rect(screen, (255, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))
            elif (row, col) in world.pit_positions:
                pygame.draw.rect(screen, (0, 0, 255), (x, y, CELL_SIZE, CELL_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Wumpus World")

    world = WumpusWorld()

    clock = pygame.time.Clock()

    while not world.is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                world.is_game_over = True

        screen.fill((0, 0, 0))

        draw_grid(screen)
        draw_elements(screen, world)

        pygame.display.flip()

        clock.tick(5)  # Adjust the speed of the game

        action = input("Enter your action (up, down, left, right): ")
        percept = world.take_action(action)
        print(percept)

    if world.has_gold:
        print("Congratulations! You won!")
    else:
        print("Better luck next time!")

    pygame.quit()


if __name__ == "__main__":
    main()
