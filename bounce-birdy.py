import random
import pygame

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

pygame.init()

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
FPS = 60

SPEED = 2
PIPE_GAP_VERTICAL = 150
PIPE_GAP_HORIZONTAL = 200
GRAVITY = 0.2
FLY_FORCE = 4

pygame.display.set_caption('Bounce Birdy')

# assets
img_background = pygame.image.load('assets/background.png').convert()
img_floor = pygame.image.load('assets/floor.png').convert()
img_pipe = pygame.image.load('assets/pipe.png').convert_alpha()
img_bird = pygame.image.load('assets/bird.png').convert_alpha()

# scale assets to fit screen
img_background = pygame.transform.scale(img_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
img_floor = pygame.transform.scale(img_floor, (WINDOW_WIDTH, WINDOW_HEIGHT // 6))
img_pipe = pygame.transform.scale(img_pipe, (img_pipe.get_width(), WINDOW_HEIGHT - 200))

# top pipe is created by vertically flipping pipe
img_pipe_top = pygame.transform.flip(img_pipe, False, True)

def main():
    clock = pygame.time.Clock()

    pipes = []
    floor_x_pos = 0
    floor_y_pos = WINDOW_HEIGHT - img_floor.get_height()
    bird_velocity = 0
    game_running = True

    img_bird_rect = img_bird.get_rect(center=(50, WINDOW_HEIGHT / 2))

    # add one pipe when game starts
    pipes.extend(new_pipe(None))

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_running:
                    bird_velocity = 0
                    bird_velocity -= FLY_FORCE
                if event.key == pygame.K_SPACE and not game_running:
                    pipes = []
                    pipes.extend(new_pipe(None))
                    img_bird_rect.center = (50, WINDOW_HEIGHT / 2)
                    bird_velocity = 0
                    game_running = True

        for pipe in pipes:
            # add new pipes
            if pipe.right < WINDOW_WIDTH - 100 and len(pipes) <= WINDOW_WIDTH / PIPE_GAP_HORIZONTAL: # window width / horizontal gap will give maximum number of pipes in list
                pipes.extend(new_pipe(pipes[-1]))

            # remove pipes from list when it goes out of screen
            if pipe.right < 0:
                pipes.pop(0) # bottom pipe
                pipes.pop(0) # top pipe
            
            # move each  pipe to the left by the speed
            pipe.centerx -= SPEED

        # move floor
        floor_x_pos -= 1
        if floor_x_pos <= -WINDOW_WIDTH:
            floor_x_pos = 0

        if game_running:
            bird_velocity += GRAVITY
            img_bird_rect.centery += bird_velocity

            if bird_collide(img_bird_rect, pipes):
                game_running = False

        draw(pipes, (floor_x_pos, floor_y_pos), img_bird_rect)
        
        pygame.display.update()

    pygame.quit()

def draw(pipes, floor_pos, img_bird_rect):
    WIN.blit(img_background, (0, 0))

    # draw pipes
    for pipe in pipes:
        if pipe.bottom >= 500:
            WIN.blit(img_pipe, pipe)
        else:
            WIN.blit(img_pipe_top, pipe)

    # draw floor
    floor_x_pos, floor_y_pos = floor_pos
    WIN.blit(img_floor, (floor_x_pos, floor_y_pos))
    WIN.blit(img_floor, (floor_x_pos + WINDOW_WIDTH, floor_y_pos))

    # draw bird
    WIN.blit(img_bird, img_bird_rect)

def new_pipe(last_pipe):
    heights = [220, 250, 300, 350, 400, 450, 480]

    if last_pipe:
        pipe_x_pos = last_pipe.right + PIPE_GAP_HORIZONTAL
    else:
        pipe_x_pos = WINDOW_WIDTH + 100

    pipe_y_pos = random.choice(heights)

    pipe_bottom = img_pipe.get_rect(midtop=(pipe_x_pos, pipe_y_pos))
    pipe_top = img_pipe.get_rect(midbottom=(pipe_x_pos, pipe_y_pos - PIPE_GAP_VERTICAL))

    return pipe_bottom, pipe_top

def bird_collide(bird, pipes):
    # check collision with top
    if bird.top <= 0:
        return True
    
    # check collision with bottom
    if bird.bottom >= WINDOW_HEIGHT - img_floor.get_height():
        return True
    
    # check collision with pipes
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True

    return False

if __name__ == '__main__':
    main()