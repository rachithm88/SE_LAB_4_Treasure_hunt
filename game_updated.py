import pygame
import random
import sys

# --- CONSTANTS ---
GRID_WIDTH = 15
GRID_HEIGHT = 11
TILE_SIZE = 48
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE + 60  # Extra space for HUD status

# Tile Types
FLOOR = 0
WALL = 1
KEY = 2
CHEST = 3
TRAP = 4

# Colors
COLOR_BG = (20, 20, 20)
COLOR_FLOOR = (40, 40, 45)
COLOR_WALL = (80, 80, 95)
COLOR_KEY = (240, 200, 40)
COLOR_CHEST_LOCKED = (150, 75, 0)
COLOR_CHEST_OPEN = (50, 205, 50)
COLOR_TRAP = (200, 50, 50)
COLOR_PLAYER = (50, 150, 250)
COLOR_GUARD = (220, 100, 30)
COLOR_UI_TEXT = (240, 240, 240)
COLOR_HUD_BG = (30, 30, 35)

# --- MAP LAYOUT ---
# 0 = Floor, 1 = Wall, 2 = Key, 3 = Chest, 4 = Trap
DUNGEON_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 4, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

START_POS = (1, 1)


class Player:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.reset()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.has_key = False

    def move(self, dx, dy, grid):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if grid[new_y][new_x] != WALL:
                self.x = new_x
                self.y = new_y


class Guard:
    """Task 2: Enemy Guard patrolling near the chest"""

    def __init__(self, start_x, y, patrol_dist, speed=0.03):
        self.x = float(start_x)
        self.y = y
        self.min_x = start_x
        self.max_x = start_x + patrol_dist
        self.direction = 1  # 1 = right, -1 = left
        self.speed = speed

    def update(self):
        self.x += self.direction * self.speed
        if self.x >= self.max_x:
            self.x = float(self.max_x)
            self.direction = -1
        elif self.x <= self.min_x:
            self.x = float(self.min_x)
            self.direction = 1

    def check_collision(self, player_x, player_y):
        # Grid-based distance check
        return abs(self.x - player_x) < 0.6 and self.y == player_y


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Treasure Hunt")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.reset_game()

    def reset_game(self):
        self.grid = [row[:] for row in DUNGEON_MAP]
        self.player = Player(START_POS[0], START_POS[1])
        # Task 2 Guard near chest at row 9 (x range 8 to 11)
        self.guard = Guard(start_x=8, y=9, patrol_dist=3, speed=0.04)
        self.status_message = "Explore the dungeon! Collect the key."
        self.game_won = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                    return
                
                if self.game_won:
                    return

                dx, dy = 0, 0
                if event.key in (pygame.K_w, pygame.K_UP):
                    dy = -1
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    dy = 1
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    dx = -1
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    dx = 1

                if dx != 0 or dy != 0:
                    self.player.move(dx, dy, self.grid)
                    self.check_tile_interaction()

    def check_tile_interaction(self):
        px, py = self.player.x, self.player.y
        tile = self.grid[py][px]

        # Collect Key
        if tile == KEY:
            self.player.has_key = True
            self.grid[py][px] = FLOOR
            self.status_message = "Key collected! Now find the chest."

        # Task 1: Traps
        elif tile == TRAP:
            self.player.x, self.player.y = self.player.start_x, self.player.start_y
            self.status_message = "Stepped on a TRAP! Reset to start!"

        # Open Chest
        elif tile == CHEST:
            if self.player.has_key:
                self.game_won = True
                self.status_message = "YOU WIN! You opened the treasure chest!"
            else:
                self.status_message = "Chest is locked! You need a key."

    def update(self):
        if not self.game_won:
            # Task 2: Update guard movement frame-by-frame
            self.guard.update()
            
            # Check guard collision
            if self.guard.check_collision(self.player.x, self.player.y):
                self.player.x, self.player.y = self.player.start_x, self.player.start_y
                self.status_message = "Caught by Guard! Reset to start!"

    def draw_minimap(self):
        """Task 3: Real-time Mini-map in top-right corner"""
        map_tile_size = 4
        padding = 10
        map_w = GRID_WIDTH * map_tile_size
        map_h = GRID_HEIGHT * map_tile_size
        start_x = SCREEN_WIDTH - map_w - padding
        start_y = padding

        # Mini-map Background
        pygame.draw.rect(self.screen, (10, 10, 10), (start_x - 2, start_y - 2, map_w + 4, map_h + 4))
        pygame.draw.rect(self.screen, (150, 150, 150), (start_x - 2, start_y - 2, map_w + 4, map_h + 4), 1)

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = (120, 120, 130) if self.grid[y][x] == WALL else (40, 40, 40)
                rect = (start_x + x * map_tile_size, start_y + y * map_tile_size, map_tile_size, map_tile_size)
                pygame.draw.rect(self.screen, color, rect)

        # Player Dot
        player_mm_x = start_x + self.player.x * map_tile_size
        player_mm_y = start_y + self.player.y * map_tile_size
        pygame.draw.rect(self.screen, (0, 255, 255), (player_mm_x, player_mm_y, map_tile_size, map_tile_size))

    def draw_inventory_ui(self):
        """Task 4: Inventory UI HUD slot"""
        slot_x, slot_y = 15, SCREEN_HEIGHT - 50
        slot_size = 40
        
        # Draw Slot Box
        pygame.draw.rect(self.screen, (50, 50, 60), (slot_x, slot_y, slot_size, slot_size))
        pygame.draw.rect(self.screen, (200, 200, 200), (slot_x, slot_y, slot_size, slot_size), 2)

        if self.player.has_key:
            # Key Icon Symbol
            pygame.draw.circle(self.screen, COLOR_KEY, (slot_x + 15, slot_y + 20), 7, 2)
            pygame.draw.line(self.screen, COLOR_KEY, (slot_x + 20, slot_y + 20), (slot_x + 30, slot_y + 20), 3)
            pygame.draw.line(self.screen, COLOR_KEY, (slot_x + 27, slot_y + 20), (slot_x + 27, slot_y + 26), 2)

    def draw(self):
        self.screen.fill(COLOR_BG)

        # Draw Grid Tiles
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile = self.grid[y][x]

                if tile == WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                elif tile == FLOOR:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
                elif tile == KEY:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
                    pygame.draw.circle(self.screen, COLOR_KEY, (x * TILE_SIZE + 24, y * TILE_SIZE + 24), 10)
                elif tile == CHEST:
                    color = COLOR_CHEST_OPEN if self.game_won else COLOR_CHEST_LOCKED
                    pygame.draw.rect(self.screen, color, rect)
                elif tile == TRAP:
                    pygame.draw.rect(self.screen, COLOR_TRAP, rect)

                pygame.draw.rect(self.screen, (30, 30, 30), rect, 1)

        # Draw Guard (Task 2)
        guard_pixel_x = int(self.guard.x * TILE_SIZE)
        guard_pixel_y = int(self.guard.y * TILE_SIZE)
        pygame.draw.rect(self.screen, COLOR_GUARD, (guard_pixel_x + 8, guard_pixel_y + 8, TILE_SIZE - 16, TILE_SIZE - 16))

        # Draw Player
        pygame.draw.rect(
            self.screen,
            COLOR_PLAYER,
            (self.player.x * TILE_SIZE + 6, self.player.y * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12),
        )

        # Draw Mini-map (Task 3)
        self.draw_minimap()

        # Draw HUD Area
        hud_rect = (0, GRID_HEIGHT * TILE_SIZE, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, COLOR_HUD_BG, hud_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, GRID_HEIGHT * TILE_SIZE), (SCREEN_WIDTH, GRID_HEIGHT * TILE_SIZE), 2)

        # Draw Inventory (Task 4)
        self.draw_inventory_ui()

        # Draw Status Text
        text_surf = self.font.render(self.status_message, True, COLOR_UI_TEXT)
        self.screen.blit(text_surf, (70, SCREEN_HEIGHT - 38))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameEngine()
    game.run()