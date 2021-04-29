import os
import pygame
##############################################################################
#������ *(�K���K�v)�@
pygame.init() #�G���[�o���� FILE - preferences - linting(����) - linting enabled(�`�F�b�N����)

# ��ʂ̑傫���ݒ�
screen_width = 640 #��
screen_height = 480 #�c
screen = pygame.display.set_mode((screen_width, screen_height)) 

#��ʃ^�C�g���ݒ�
pygame.display.set_caption("pang Game") #�Q�[�����O

#FPS
clock = pygame.time.Clock()
##############################################################################

# 1.user game initialization (background, game image, coordinates, speed, font, etc)

current_path = os.path.dirname(__file__) #���݃t�@�C���̈ʒu��Ԃ�
image_path = os.path.join(current_path,"images") #image�@�t�H���_�̈ʒu��Ԃ�

#�w�i
background = pygame.image.load(os.path.join(image_path,"background.png"))

#make a stage
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #�X�e�[�W�̍����ɃL�����N�^�[��u������

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

#�e�͈�x�ɉ����ł����ˉ\
weapons = []

#weapon movement speed
weapon_speed = 10

#make a ball(4�̑傫���ɑ΂��ĕʂɏ���)
ball_iamges = [
    pygame.image.load(os.path.join(image_path,"ballon1.png")),
    pygame.image.load(os.path.join(image_path,"ballon2.png")),
    pygame.image.load(os.path.join(image_path,"ballon3.png")),
    pygame.image.load(os.path.join(image_path,"ballon4.png"))
] 
#�{�[���̑傫���ɂ��ŏ��X�s�[�h
ball_speed_y = [-18,-15,-12,-9] #index�@0,1,2,3�ɊY������l

#balls
balls = []

#�ŏ��A��������傫���{�[���ǉ�
balls.append({
    "pos_x" : 50, #�{�[����x���W
    "pos_y" : 50, #�{�[����y���W
    "img_idx" : 0, #�{�[���̃C���[�W�@�C���f�b�N�X
    "to_x" : 3, #�{�[����x���ړ������A�@�|�R�������獶�ɁA�R��������E��
    "to_y" : -6,#y���ړ�����,
    "init_spd_y": ball_speed_y[0]}) #y�̍ŏ����x

#�����镐��A�{�[���̏��ϐ�
weapon_to_remove = -1
ball_to_remove = -1

running = True 
while running:
    dt = clock.tick(60) 

    # 2. processing event (keyboard, mouse, etc)
    print("fps : " + str(clock.get_fps())) #display fps on terminal

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #�L�����N�^�[������
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT: #�L�����N�^�[���E��
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
    #x_position?? w[0]? ??? ?? y_position?? w[1]? weapon_speen ??? ? ?
    weapons = [[w[0],w[1] - weapon_speed] for w in weapons]

    # �V��ɒ������������
    weapons = [[w[0],w[1]]  for w in weapons if w[1] > 0] #??? ?? ?? ?? ???? ???? ???

    #�{�[���̈ʒu��`
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_iamges[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #���̕ǂɐG�ꂽ�Ƃ��{�[���̈ړ������ύX�@�i�e���@���ʁj
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        
        #�c�ʒu
        #�X�e�[�W�ɒe����ďオ�鏈��
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]

        #����ȊO�̏ꍇ�ɂ͑��x���グ�Ă����@
        else: #�{�[�����オ��Ƃ��͍ŏ��l���}�C�i�X�ɂȂ��Ă邩�瑬�x���グ����{�[���̑��x�͒x���Ȃ��ĂO�ɂȂ����痎����
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 4. crash check 

    #character rect data update
    character_rect = character.get._rect()
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

        #�{�[���ƃL�����N�^�[�̏Փˏ���
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #�{�[���ƕ��킽���̏Փˏ���   
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #armor rect information update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #�{�[���ɂԂ���������������l�̐ݒ�
                ball_to_remove = ball_idx #�Y���{�[�����������߂̒l�̐ݒ�
                break

    #�Փ˂����{�[���@or�@�������
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

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

    
    pygame.display.update() #�Q�[����ʂ����������I(�����Ɖ�ʂ����������Ă��銴��)�K���K�v

pygame.quit()
