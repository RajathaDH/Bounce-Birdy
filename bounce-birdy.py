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

pygame.display.set_caption('Bounce Birdy')

# assets
img_background = pygame.image.load('assets/background.png').convert()
img_floor = pygame.image.load('assets/floor.png').convert()
img_pipe = pygame.image.load('assets/pipe.png').convert_alpha()
img_bird = pygame.image.load('assets/bird.png').convert()

# top pipe is created by vertically flipping pipe
img_pipe_top = pygame.transform.flip(img_pipe, False, True)

def main():
    clock = pygame.time.Clock()

    pipes = []
    floor_pos = 0

    # add one pipe when game starts
    pipes.extend(new_pipe(None))

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

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

        floor_pos -= 1
        if floor_pos <= -WINDOW_WIDTH:
            floor_pos = 0

        draw(pipes, floor_pos)
        
        pygame.display.update()

    pygame.quit()

def draw(pipes, floor_pos):
    WIN.blit(img_background, (0, 0))

    # draw pipes
    for pipe in pipes:
        if pipe.bottom >= 500:
            WIN.blit(img_pipe, pipe)
        else:
            WIN.blit(img_pipe_top, pipe)

    # draw floor
    WIN.blit(img_floor, (floor_pos, 500))
    WIN.blit(img_floor, (floor_pos + WINDOW_WIDTH, 500))

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

if __name__ == '__main__':
    main()