import os
import pygame
##############################################################################
#初期化 *(必ず必要)　
pygame.init() #エラー出たら FILE - preferences - linting(検索) - linting enabled(チェック解除)

# 画面の大きさ設定
screen_width = 640 #横
screen_height = 480 #縦
screen = pygame.display.set_mode((screen_width, screen_height)) 

#画面タイトル設定
pygame.display.set_caption("pang Game") #ゲーム名前

#FPS
clock = pygame.time.Clock()
##############################################################################

# 1.user game initialization (background, game image, coordinates, speed, font, etc)

current_path = os.path.dirname(__file__) #現在ファイルの位置を返す
image_path = os.path.join(current_path,"images") #image　フォルダの位置を返す

#背景
background = pygame.image.load(os.path.join(image_path,"background.png"))

#make a stage
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #ステージの高さにキャラクターを置くため

#make a character
character = pygame.image.load(os.path.join(image_path,"character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width /2)
character_y_pos = screen_height - character_height - stage_height


running = True 
while running:
    dt = clock.tick(60) 

    # 2. processing event (keyboard, mouse, etc)
    print("fps : " + str(clock.get_fps())) #display fps on terminal

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

    # 3. definition of character location information 

    # 4. crash check 

    # 5. draw on display
    screen.blit(background,(0,0))
    screen.blit(stage,(0,screen_height - stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    pygame.display.update() #ゲーム画面を書き直す！(ずっと画面を書き直している感じ)必ず必要

pygame.quit()
