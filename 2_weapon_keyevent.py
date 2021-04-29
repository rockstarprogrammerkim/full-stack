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

#character movement
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

#character speed
character_speed = 5

#make a weapon
weapon = pygame.image.load(os.path.join(image_path,"weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#銃は一度に何発でも発射可能
weapons = []

#weapon movement speed
weapon_speed = 10




running = True 
while running:
    dt = clock.tick(60) 

    # 2. processing event (keyboard, mouse, etc)
    print("fps : " + str(clock.get_fps())) #display fps on terminal

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #キャラクターを左に
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT: #キャラクターを右に
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE: #fire weapon
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0 
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0


    # 3. definition of character location information 
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT 

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #weapon position control
    #100,200 -> 100, 180,160,140,...
    #500,200 -> 500, 180,160,140,...
    #x_position값인 w[0]은 그대로 두고 y_position값인 w[1]은 weapon_speen 만큼을 뺀 값
    weapons = [[w[0],w[1] - weapon_speed] for w in weapons]

    # 天井に着いた武器消す
    weapons = [[w[0],w[1]]  for w in weapons if w[1] > 0] #천장에 닿지 않은 것에 대해서만 리스트를 만든다

    # 4. crash check 

    # 5. draw on display
    screen.blit(background,(0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage,(0,screen_height - stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    
    pygame.display.update() #ゲーム画面を書き直す！(ずっと画面を書き直している感じ)必ず必要

pygame.quit()
