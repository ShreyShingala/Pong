from cmath import rect
from operator import truediv
from turtle import back
import pygame
from pyparsing import White
pygame.init()

width, height = 700, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

fps = 60

white = (255, 255, 255)
black = (0, 0, 0)

score_font = pygame.font.SysFont("calibri", 50)
win_font = pygame.font.SysFont("cambriacambriamath", 150)

paddle_width, paddle_height = 20, 100
ball_radius = 7

winning_score = 10

class paddle:
    color = white
    vel = 4
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = self.original_width = width
        self.height = self.original_height = height
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up:
            self.y -= self.vel
        else:
            self.y += self.vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.width = self.original_width
        self.height = self.original_height
        
            
class Ball:
    max_vel = 7
    color = white
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = self.original_radius = radius
        self.x_vel = self.max_vel
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        
    

def draw(win, paddles, balls, leftscore, rightscore):
    win.fill(black)
    
    left_score_text = score_font.render(f"{leftscore}", 1, white)
    right_score_text = score_font.render(f"{rightscore}", 1, white)
    
    win.blit(left_score_text, (width//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (width * (3/4) - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw(win)
        
    for ball in balls:
        ball.draw(win)
        
    for i in range(10, height, height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, white, (width//2 - 5, i, 10, height//20))
        
    
    pygame.display.update()
    
def handle_collision(ball, leftpaddle, rightpaddle):
    if ball.y + ball_radius >= height:
        ball.y_vel *= -1
    elif ball.y - ball_radius <= 0:
        ball.y_vel *= -1
    #ceiling above    
    
    if ball.x_vel < 0:
        if ball.y >= leftpaddle.y and ball.y <= leftpaddle.y + leftpaddle.height:
            if ball.x - ball_radius <= leftpaddle.x + leftpaddle.width:
                ball.x_vel *= -1
                
                middle_y = leftpaddle.y + leftpaddle.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (leftpaddle.height / 2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
        #left paddle
        
    else:
        if ball.y >= rightpaddle.y and ball.y <= rightpaddle.y + rightpaddle.height:
            if ball.x + ball_radius >= rightpaddle.x:
                ball.x_vel *= -1
                
                middle_y = rightpaddle.y + rightpaddle.height /2
                difference_in_y = middle_y - ball.y
                reduction_factor = (rightpaddle.height / 2) / ball.max_vel
                y_vel = difference_in_y / reduction_factor
                
                ball.y_vel = -1 * y_vel
        #right paddle
    
    
def handle_paddle_movement(keys, leftpaddle, rightpaddle):
    if keys[pygame.K_w] and leftpaddle.y - leftpaddle.vel >= 0 and not keys[pygame.K_s]:
        leftpaddle.move(up=True)
        
    if keys[pygame.K_s] and leftpaddle.y + leftpaddle.vel + leftpaddle.height <= height and not keys[pygame.K_w]:
        leftpaddle.move(up=False)
        
    if keys[pygame.K_UP] and rightpaddle.y - rightpaddle.vel >= 0 and not keys[pygame.K_DOWN]:
        rightpaddle.move(up=True)
        
    if keys[pygame.K_DOWN] and rightpaddle.y + rightpaddle.vel + rightpaddle.height <= height and not keys[pygame.K_UP]:
        rightpaddle.move(up=False)

def draweverything(win):
    win.fill(black)
    pygame.draw.rect(win, white, (width//2 - 150, height/10, 300, 50))
    pygame.draw.rect(win, white, (width//2 - 150, ((height/10) * 1), 300, 50))
    pygame.draw.rect(win, white, (width//2 - 150, 400, 300, 50))
    
    #working on this right now
    
    oneplayer = score_font.render("1 player", 1, black)
    twoplayer = score_font.render("2 player", 1, black)
    quit = score_font.render("quit", 1, black)
    
    pygame.display.update()
    

def mainmenu():
    running = True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(fps)
        
        draweverything(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
    

def main():
    run = True
    clock = pygame.time.Clock()
    
    leftpaddle = paddle(10, height//2 - paddle_height//2, paddle_width, paddle_height)
    rightpaddle = paddle(width - 10 - paddle_width, height//2 - paddle_height//2, paddle_width, paddle_height)
    ball = Ball(width//2, height//2, ball_radius)
    
    leftscore = 0
    rightscore = 0
    
    while run:
        clock.tick(fps)
        draw(win, [leftpaddle, rightpaddle], [ball], leftscore, rightscore)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, leftpaddle, rightpaddle)
        
        ball.move()
        
        handle_collision(ball, leftpaddle, rightpaddle)
            
        if ball.x < 0:
            rightscore += 1
            ball.reset()
            leftpaddle.reset()
            rightpaddle.reset()
        elif ball.x > width:
            leftscore += 1
            ball.reset()
            leftpaddle.reset()
            rightpaddle.reset()
            
        won = False
            
        left_person_win = win_font.render(f"Player 1 won!", 1, white)
        right_person_win = win_font.render(f"Player 2 won!", 1, white)
        
        if leftscore >= winning_score:
            won = True
            
        elif rightscore >= winning_score:
            won = True
            
        if won:
            ball.reset()
            leftpaddle.reset()
            rightpaddle.reset()
            
            win.fill(black)
            
            if rightscore >= winning_score:
                win.blit(right_person_win, (width//2 - right_person_win.get_width()//2, height//2 - right_person_win.get_height()//2))
            else:
                win.blit(left_person_win, (width//2 - left_person_win.get_width()//2, height//2 - left_person_win.get_height()//2))
            
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
            
    pygame.quit()
    
if __name__ == "__main__":
    mainmenu()