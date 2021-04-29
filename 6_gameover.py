# 1. キャラクターがボールにぶつかった時（失敗）
# 2. 全てのボールを消したらゲーム終了（成功）
# 3. 時間制限　９９秒を超過時ゲーム終了（失敗）


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

#make a ball(4個の大きさに対して別に処理)
ball_iamges = [
    pygame.image.load(os.path.join(image_path,"ballon1.png")),
    pygame.image.load(os.path.join(image_path,"ballon2.png")),
    pygame.image.load(os.path.join(image_path,"ballon3.png")),
    pygame.image.load(os.path.join(image_path,"ballon4.png"))
] 
#ボールの大きさによる最初スピード
ball_speed_y = [-18,-15,-12,-9] #index　0,1,2,3に該当する値

#balls
balls = []

#最初、発生する大きいボール追加
balls.append({
    "pos_x" : 50, #ボールのx座標
    "pos_y" : 50, #ボールのy座標
    "img_idx" : 0, #ボールのイメージ　インデックス
    "to_x" : 3, #ボールのx軸移動方向、　－３だったら左に、３だったら右に
    "to_y" : -6,#y軸移動方向,
    "init_spd_y": ball_speed_y[0]}) #yの最初速度

#消える武器、ボールの情報変数
weapon_to_remove = -1
ball_to_remove = -1

#font 定義
game_font = pygame.font.Font(None,40)
total_time = 30
start_ticks = pygame.time.get_ticks() #スタート時間定義

#game over message
#time out（時間超過　失敗）, mission complete（成功）, game over(キャラクターがボールにぶつかる　失敗)
game_result = "GAME OVER"

running = True 
while running:
    dt = clock.tick(30) 

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

    #ボールの位置定義
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_iamges[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #横の壁に触れたときボールの移動方向変更　（弾く　効果）
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        
        #縦位置
        #ステージに弾かれて上がる処理
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]

        #それ以外の場合には速度を上げていく　
        else: #ボールが上がるときは最初値がマイナスになってるから速度を上げたらボールの速度は遅くなって０になったら落ちる
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. crash check 

    #character rect data update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        #ball rect data update
        ball_rect = ball_iamges[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #ボールとキャラクターの衝突処理
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #ボールと武器たちの衝突処理   
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #armor rect information update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #ボールにぶつかった武器を消す値の設定
                ball_to_remove = ball_idx #該当ボールを消すための値の設定

                #一番小さいボールじゃなければ次の大きさのボールに分けてあげる
                if ball_img_idx < 3:
                    #現在、ボールの大きさの情報を持ってくる
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #分けられたボールの情報
                    small_ball_rect = ball_iamges[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]


                    #左に弾かれて行く小さいボール
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width/2) - (small_ball_width/2), #ボールのx座標
                        "pos_y" : ball_pos_y + (ball_height/2) - (small_ball_height/2), #ボールのy座標
                        "img_idx" : ball_img_idx + 1, #ボールのイメージ　インデックス
                        "to_x" : -3, #ボールのx軸移動方向、　－３だったら左に、３だったら右に
                        "to_y" : -6,#y軸移動方向,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) #yの最初速度})

                    #右に弾かれて行く小さいボール
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width/2) - (small_ball_width/2), #ボールのx座標
                        "pos_y" : ball_pos_y + (ball_height/2) - (small_ball_height/2), #ボールのy座標
                        "img_idx" : ball_img_idx + 1, #ボールのイメージ　インデックス
                        "to_x" : 3, #ボールのx軸移動方向、　－３だったら左に、３だったら右に
                        "to_y" : -6,#y軸移動方向,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]}) #yの最初速度})

                break
        else: #続いてゲームを進行
            continue  #内側のfor文の条件が会わなければ continue. 外側のfor文は続いて進行
        break #内側for文でbreakになったらここに侵入可能。２重for文を一回で脱出

    #衝突したボール　or　武器消す
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #全てのボールを消した場合ゲーム終了（成功）
    if len(balls) == 0:
        game_result = "MISSION COMPLETE"
        running = False

    # 5. draw on display
    screen.blit(background,(0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_iamges[ball_img_idx],(ball_pos_x, ball_pos_y))

    screen.blit(stage,(0,screen_height - stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))

    #経過時間計算
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #ms->s
    timer = game_font.render("TIME : {}".format(int(total_time - elapsed_time)),True,(255,255,255))
    screen.blit(timer,(10,10))

    #時間超過した場合
    if total_time - elapsed_time <= 0:
        game_result = "TIME OVER"
        running = False

    pygame.display.update() #ゲーム画面を書き直す！(ずっと画面を書き直している感じ)必ず必要

#game over message
msg = game_font.render(game_result, True, (255, 255, 0)) #yellow 
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

#２秒待機
pygame.time.delay(2000)

pygame.quit()
