import sys
import numpy as np
import os

# Code map[x][y] with x is Vertical  axis,  y is Horizontal axis
# Move map[x][y] with x is Horizontal axis, y is Vertical axis

global boxes_will_be_exploded
'''
The list contains all the boxes that will be exploded right after
the bomb has been planted 
'''
boxes_will_be_exploded = []

def input_data():
    # Take input from server
    map = []
    for i in range(height):
        row = input()
        row = [*row]
        map.append(row)

    for cordinate in boxes_will_be_exploded:
        x, y = cordinate[0], cordinate[1]
        map[x][y] = '.'


    entities = int(input())
    for i in range(entities):
        entity_type, owner, y, x, param_1, param_2 = [int(j) for j in input().split()]
        print('entity', entity_type, owner, y, x, param_1, param_2, file=sys.stderr)
        

        # The next following code blocks will encode the map with Player Position, Bomb and Buffs
        if entity_type == 0 and owner == my_id:
            map[x][y] = 'P' + str(owner)
            P0x, P0y = x, y
            P0_1 = param_1
            P0_2 = param_2

        elif entity_type == 1:
            map[x][y] = 'B' + str(owner)
            check_damage(map, x, y, param_2)

        elif entity_type == 0:
            map[x][y] = 'P' + str(owner)
        
        elif entity_type == 2 and param_1 == 1:
            map[x][y] = 'ER' + str(owner)

        elif entity_type == 2 and param_1 == 2:
            map[x][y] = 'EB' + str(owner)    

    return [map, P0x, P0y, P0_1, P0_2]

def check_around(map, x, y, param_2):
    '''
    Input: map, Cordinate of the box and range of bomb (aka bomb damage)
    Output:  list of best score, best position from the box and best direction
    The func will simulate if we plant the bomb on 4 ways (North, East, South, West)
    from the bombs, which direction will be optimized, also the distance from the bomb also
    For example:  1 . 1
                  . . 1
                  . O .
                  . . .
        Solution, plant on North side and 2 blocks away from the box (O)
    '''
    # If plant bomb on the top of box
    local_score = []
    for i in range(1, param_2):        
        box_exploded = 0
        bomb_position_x = x - i

        try:
            if map[bomb_position_x][y] in ['0','1','2', 'x']:
                local_score.append(-10)
                break
        except IndexError:
            local_score.append(-10)
            break

        if bomb_position_x < 0:
            local_score.append(-10)
            break
        else:
            try:
                if map[bomb_position_x][y] :
                    flag = [0, 0, 0]
                    for j in range(1, param_2):
                        # Now we will simulate if we plant the bomb at 'j' distance from the box 
                        # then how many box will explode
                        if map[bomb_position_x][y - j] in ['0','1','2'] and y - j >= 0 and flag[0] == 0:
                            # to the left
                            box_exploded += 1 
                            flag[0] = 1

                        elif map[bomb_position_x][y - j] == 'x' and y - j >= 0  and flag[0] == 0:
                            flag[0] = 1

                        if map[bomb_position_x][y + j] in ['0','1','2'] and flag[1] == 0:
                            # to the right
                            box_exploded += 1
                        elif map[bomb_position_x][y + j] == 'x' and flag[1] == 0:
                            flag[1] = 1

                        if map[bomb_position_x - j][y] in ['0','1','2'] and bomb_position_x - j >= 0 and flag[2] == 0:
                            # to the top
                            box_exploded += 1
                        elif map[bomb_position_x - j][y] == 'x' and bomb_position_x - j >= 0 and flag[2] == 0:
                            flag[2] = 1
                        
                        if flag == [1, 1, 1]:
                            break

                    local_score.append(box_exploded)
            except Exception as e:
                local_score.append(-1)

    best_position = local_score.index(max(local_score))
    # best position will get index of best score among the j position
    best_score = max(local_score)
    

    # print('top', local_score, file=sys.stderr)

    global_best_score = best_score
    global_best_position = best_position + 1
    global_best_dir = 'top'

    # If plant bomb on the right of box
    local_score = []
    for i in range(1, param_2):  

        box_exploded = 0
        bomb_position_y = y + i
        
        try:
            if map[x][bomb_position_y] in ['0','1','2', 'x']:
                local_score.append(-10)
                break
        except IndexError:
            local_score.append(-10)
            break

        if bomb_position_y < 0:
            local_score.append(-10)
            break
        else:
            try:
                if map[x][bomb_position_y]:
                    flag = [0, 0, 0]
                    for j in range(1, param_2):
                        # Now we will simulate if we plant the bomb at 'j' distance from the box 
                        # then how many box will explode

                        if map[x - j][bomb_position_y] in ['0','1','2'] and x - j >= 0 and flag[0] == 0:
                            # to the top 
                            box_exploded += 1 
                            flag[0] = 1
                        elif map[x - j][bomb_position_y] == 'x' and x - j >= 0 and flag[0] == 0:
                            flag[0] = 1

                        if map[x + j][bomb_position_y] in ['0','1','2'] and flag[1] == 0:
                            # to the bottom
                            box_exploded += 1
                            flag[1] = 1
                        elif map[x + j][bomb_position_y] == 'x' and flag[1] == 0:
                            flag[1] = 1

                        if map[x][bomb_position_y + j] in ['0','1','2'] and flag[2] == 0:
                            # to the right
                            box_exploded += 1
                            flag[2] = 1
                        elif map[x][bomb_position_y + j] == 'x' and flag[2] == 0:
                            flag[2] = 1

                        if flag == [1, 1, 1]:
                            break
                        
                    local_score.append(box_exploded)

            except Exception as e:
                local_score.append(-1)

    best_position = local_score.index(max(local_score))
    best_score = max(local_score)
    
    # print('right', local_score, file=sys.stderr)

    if global_best_score < best_score:
            global_best_score = best_score
            global_best_position = best_position + 1
            global_best_dir = 'right'

    # If plant bomb on the bottom of box
    local_score = []
    for i in range(1, param_2):        
        box_exploded = 0
        bomb_position_x = x + i
        try:
            if map[bomb_position_x][y] in ['0','1','2', 'x']:
                local_score.append(-10)
                break
        except IndexError:
            local_score.append(-10)
            break

        if bomb_position_x < 0:
            local_score.append(-10)
            break
        else:
        
            try:
                if map[bomb_position_x][y]:
                    flag = [0, 0, 0]
                    for j in range(1, param_2):
                        # Now we will simulate if we plant the bomb at 'j' distance from the box 
                        # then how many box will explode
                        if map[bomb_position_x][y - j] in ['0','1','2'] and y - j >= 0 and flag[0] == 0 :
                            # to the left
                            box_exploded += 1 
                            flag[0] = 1
                        elif map[bomb_position_x][y - j] == 'x' and flag[0] == 0:
                            flag[0] = 1

                        if map[bomb_position_x][y + j] in ['0','1','2'] and flag[1] == 0:
                            # to the right
                            box_exploded += 1
                            flag[1] = 1
                        elif map[bomb_position_x][y + j] == 'x' and flag[1] == 0:
                            flag[1] = 1

                        if map[bomb_position_x + j][y] in ['0','1','2'] and flag[2] == 0:
                            # to the bottom
                            box_exploded += 1
                            flag[2] = 1
                        elif map[bomb_position_x + j][y] == 'x' and flag[2] == 0:
                            flag[2] =1

                        if flag == [1, 1, 1]:
                            break
                        
                    local_score.append(box_exploded)
            except Exception as e:
                local_score.append(-1)

    best_position = local_score.index(max(local_score))
    best_score = max(local_score)

    # print('bottom', local_score, file=sys.stderr)

    if global_best_score < best_score:
            global_best_score = best_score
            global_best_position = best_position + 1
            global_best_dir = 'bottom'


    # if plant bomb on the left of box
    local_score = []
    for i in range(1, param_2):        
        box_exploded = 0
        bomb_position_y = y - i

        try:
            if map[x][bomb_position_y] in ['0','1','2']:
                local_score.append(-10)
                break
        except IndexError:
            local_score.append(-10)
            break


        if bomb_position_y < 0:
            local_score.append(-10)
            
        else:
            try:
                if map[x][bomb_position_y]:
                    flag = [0, 0, 0]
                    for j in range(1, param_2):
                        # Now we will simulate if we plant the bomb at 'j' distance from the box 
                        # then how many box will explode
                        if map[x - j][bomb_position_y] in ['0','1','2'] and x - j >= 0 and flag[0] == 0:
                            # to the top 
                            box_exploded += 1 
                            flag[0] = 1
                        elif map[x - j][bomb_position_y] == 'x' and flag[0] == 0:
                            flag[0] = 1
                        
                        if map[x + j][bomb_position_y] in ['0','1','2'] and flag[1] == 0:
                            # to the bottom
                            box_exploded += 1
                            flag[1] = 1 
                        elif map[x + j][bomb_position_y] == 'x' and flag[1] == 0:
                            flag[1] = 1 
                        
                        if map[x][bomb_position_y - j] in ['0','1','2'] and bomb_position_y - j >= 0 and flag[2] == 0:
                            # to the left
                            box_exploded += 1
                            flag[2] = 1
                        elif map[x][bomb_position_y - j] == 'x' and flag[2] == 0:
                            flag[2] = 1

                    local_score.append(box_exploded)
            except Exception as e:
                local_score.append(-1)

    best_position = local_score.index(max(local_score))
    best_score = max(local_score)

    # print('left', local_score, file=sys.stderr)

    if global_best_score < best_score:
            global_best_score = best_score
            global_best_position = best_position + 1
            global_best_dir = 'left'
    
    return [global_best_score, global_best_position, global_best_dir]

def check_damage(map, x, y, param_2):
    '''
    Input: map, cordinate of the bomb, range of the bomb aka bomb damage
    Output: all the boxes that will be exploded right after the bomb has been planted
    The function will check if any boxes will be exploded right after the bomb has been 
    planted and append them to boxed_will_be_exploded list 
    '''
    flag = [0, 0, 0, 0] # for marking if box of which direction has exploded
    for i in range(1, param_2):
        try:
            if map[x + i][y] in ['0','1','2'] and flag[0] == 0:
                # Start from South 
                boxes_will_be_exploded.append([x+i, y])
                flag[0] = 1
        except IndexError:
            flag[0] = 1

        try: 
            if map[x][y + i] in ['0','1','2'] and flag[1] == 0:
                # To East 
                boxes_will_be_exploded.append([x, y+i])
                flag[1] = 1
        except IndexError:
            flag[1] = 1

        if map[x - i][y] in ['0','1','2'] and flag[2] == 0 and x - i >= 0:
            # To North 
            boxes_will_be_exploded.append([x-i, y])
            flag[2] = 1

        if map[x][y - i] in ['0','1','2'] and flag[3] == 0 and y - i >= 0:
            # End with West 
            boxes_will_be_exploded.append([x, y-i])
            flag[3] = 1

        if flag == [1,1,1,1]:
            break 

def go_east(map, P0x, P0y, i, P0_1, P0_2):
    '''
    Input: map, cordinate of box, radius, Bomb available, Bomb Dmg
    Output: 'None'
    All the function with go will have the same format and have the same algorithm:
    1) Check the optimized cordinate to plant to the bomb around the box
    2) Get that cordinate
    3) If the Player is out of reach to that cordinate then Program will loop until Player get there and Bomb
    4) After planting the bomb, Program will check the boxes damaged by the bomb and delete that boxes immidiately 
    '''

    print('East', file=sys.stderr)  

    result = check_around(map, P0x, P0y+i, P0_2)
    
    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x - best_cor, P0y + i]
    elif best_dir == 'right':
        cor = [P0x, P0y + i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x + best_cor, P0y + i]
    elif best_dir == 'left':
        cor = [P0x, P0y + i  - best_cor]
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:

        while [P0x, P0y] != cor:            
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)


def go_south(map, P0x, P0y, i, P0_1, P0_2):
    print('South', file=sys.stderr)

    result = check_around(map, P0x+i, P0y, P0_2)

    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x+i - best_cor, P0y]
    elif best_dir == 'right':
        cor = [P0x+i, P0y + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x+i+ best_cor, P0y]
    elif best_dir == 'left':
        cor = [P0x+i, P0y - best_cor]

    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]     
        else:
            if P0_1 >= 0:
                action = 'BOMB'                
                print(action, str(cor[1]), str(cor[0]))
                print(action, str(cor[1]), str(cor[0]), file=sys.stderr)


def go_west(map, P0x, P0y, i, P0_1, P0_2) :
    print('West', file=sys.stderr)
    result = check_around(map, P0x, P0y-i, P0_2)

    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x - best_cor, P0y-i]
    elif best_dir == 'right':
        cor = [P0x, P0y-i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x + best_cor, P0y-i]
    elif best_dir == 'left':
        cor = [P0x, P0y-i - best_cor]

    distance_to_box = abs(cor[0] - P0x) + abs(cor[1] - P0y)
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)


def go_north(map, P0x, P0y, i, P0_1, P0_2) :
    print('North', file=sys.stderr)

    result = check_around(map, P0x - i, P0y, P0_2)

    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x - i- best_cor, P0y]
    elif best_dir == 'right':
        cor = [P0x - i, P0y - i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x - i+ best_cor, P0y]
    elif best_dir == 'left':
        cor = [P0x - i, P0y - best_cor]
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)


def go_north_east(map, P0x, P0y, i, P0_2) :
    print('North East', file=sys.stderr)
    result = check_around(map, P0x - i, P0y + i, P0_2)

    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x - i - best_cor, P0y + i]
    elif best_dir == 'right':
        cor = [P0x - i, P0y + i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x - i + best_cor, P0y + i]
    elif best_dir == 'left':
        cor = [P0x - i, P0y + i - best_cor]
    
    distance_to_box = abs(cor[0] - P0x) + abs(cor[1] - P0y)

    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                print(action, str(cor[1]), str(cor[0]))
                
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)


def go_south_east(map, P0x, P0y, i, P0_2) :
    print('South East', P0x+i, P0y+i, file=sys.stderr)


    result = check_around(map, P0x+i, P0y+i, P0_2)

    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x + i - best_cor, P0y + i]
    elif best_dir == 'right':
        cor = [P0x + i, P0y + i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x + i + best_cor, P0y + i]
    elif best_dir == 'left':
        cor = [P0x + i, P0y + i - best_cor]
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))


def go_south_west(map, P0x, P0y, i, P0_2) :
    print('South West', file=sys.stderr)

    result = check_around(map, P0x+i, P0y-i, P0_2)


    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x + i - best_cor, P0y - i]
    elif best_dir == 'right':
        cor = [P0x + i, P0y - i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x + i + best_cor, P0y - i]
    elif best_dir == 'left':
        cor = [P0x + i, P0y - i - best_cor]
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)

    
def go_north_west(map, P0x, P0y, i, P0_2) :
    print('North West', file=sys.stderr)

    result = check_around(map, P0x - i, P0y - i, P0_2)


    best_cor = result[1]
    best_dir = result[2]

    if best_dir == 'top':
        cor = [P0x - i - best_cor, P0y - i]
    elif best_dir == 'right':
        cor = [P0x - i, P0y - i + best_cor]
    elif best_dir == 'bottom':
        cor = [P0x - i + best_cor, P0y - i]
    elif best_dir == 'left':
        cor = [P0x - i, P0y - i - best_cor]
    
    if [P0x, P0y] == cor and P0_1 != 0:
        action = 'BOMB'
        print(action, str(cor[1]), str(cor[0]))
        # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
        return
    else:
        while [P0x, P0y] != cor:
            action = 'MOVE'
            print(action, str(cor[1]), str(cor[0]))
            # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)
            data =  input_data()
            P0x, P0y = data[1], data[2]
        else:
            if P0_1 >= 0:
                action = 'BOMB'
                
                print(action, str(cor[1]), str(cor[0]))
                # print(action, str(cor[1]), str(cor[0]), file=sys.stderr)

def ultimate_case(map, P0x, P0y):
    # This case only happen when all option above are unavailable
    # The func will move Player to the top and move left or right to scan
    print('UC', file=sys.stderr)

    while [P0x, P0y] != [0, P0y]:
        print('MOVE', P0y, 0)
        data =  input_data()
        P0x, P0y = data[1], data[2]
    else:
        try:
            print('MOVE', P0y-1, 0)
        except IndexError:
            print('MOVE', P0y+1, 0)
                    
#####################################################################################################################
global my_id
width, height, my_id = [int(i) for i in input().split()]


# game loop

while True:
    
    map, P0x, P0y, P0_1, P0_2 = input_data()
    print(np.array(map), file=sys.stderr)

    radius = 1

    while True:   
        '''
        We will scan the whole enviroment around Player Position
        with 8 direction: N, E, S, W, NE, SE, SW, NW
        '''     
        i = radius

        print('radius', i, file=sys.stderr)

        try:
            if map[P0x + i][P0y] in ['0','1','2']:                   
                go_south(map, P0x, P0y, i, P0_1, P0_2)             
                break

            elif map[P0x][P0y+i] in ['0','1','2']:
                go_east(map, P0x, P0y, i, P0_1, P0_2)              
                break

            elif map[P0x - i][P0y] in ['0','1','2'] and P0x - i >= 0:
             
                go_north(map, P0x, P0y, i, P0_1, P0_2)
                break

            elif map[P0x][P0y-i] in ['0','1','2'] and P0y - i >= 0:

                go_west(map, P0x, P0y, i, P0_1, P0_2) 
                break

            elif map[P0x+i][P0y-i] in ['0','1','2'] and P0y - i >= 0:
                go_south_west(map, P0x, P0y, i, P0_2)
                break

            elif map[P0x + i][P0y + i] in ['0','1','2']:
                go_south_east(map, P0x, P0y, i, P0_2)
                break

            elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                go_north_east(map, P0x, P0y, i, P0_2)
                break

            elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                go_north_west(map, P0x, P0y, i, P0_2)
                break

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
            try:
                if map[P0x][P0y+i] in ['0','1','2']:
                    go_east(map, P0x, P0y, i, P0_1, P0_2)              
                    break

                elif map[P0x - i][P0y] in ['0','1','2'] and P0x - i >= 0:
                
                    go_north(map, P0x, P0y, i, P0_1, P0_2)
                    break

                elif map[P0x][P0y-i] in ['0','1','2'] and P0y - i >= 0:

                    go_west(map, P0x, P0y, i, P0_1, P0_2) 
                    break

                elif map[P0x+i][P0y-i] in ['0','1','2'] and P0y - i >= 0:
                    go_south_west(map, P0x, P0y, i, P0_2)
                    break

                elif map[P0x + i][P0y + i] in ['0','1','2']:
                    go_south_east(map, P0x, P0y, i, P0_2)
                    break

                elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                    go_north_east(map, P0x, P0y, i, P0_2)
                    break

                elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                    go_north_west(map, P0x, P0y, i, P0_2)
                    break

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)

                try:
                    if map[P0x - i][P0y] in ['0','1','2'] and P0x - i >= 0:
                    
                        go_north(map, P0x, P0y, i, P0_1, P0_2)
                        break

                    elif map[P0x][P0y-i] in ['0','1','2'] and P0y - i >= 0:

                        go_west(map, P0x, P0y, i, P0_1, P0_2) 
                        break

                    elif map[P0x+i][P0y-i] in ['0','1','2'] and P0y - i >= 0:
                        go_south_west(map, P0x, P0y, i, P0_2)
                        break

                    elif map[P0x + i][P0y + i] in ['0','1','2']:
                        go_south_east(map, P0x, P0y, i, P0_2)
                        break

                    elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                        go_north_east(map, P0x, P0y, i, P0_2)
                        break

                    elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                        go_north_west(map, P0x, P0y, i, P0_2)
                        break

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                    try:
                        if map[P0x][P0y-i] in ['0','1','2'] and P0y - i >= 0:

                            go_west(map, P0x, P0y, i, P0_1, P0_2) 
                            break

                        elif map[P0x+i][P0y-i] in ['0','1','2'] and P0y - i >= 0:
                            go_south_west(map, P0x, P0y, i, P0_2)
                            break

                        elif map[P0x + i][P0y + i] in ['0','1','2']:
                            go_south_east(map, P0x, P0y, i, P0_2)
                            break

                        elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                            go_north_east(map, P0x, P0y, i, P0_2)
                            break

                        elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                            go_north_west(map, P0x, P0y, i, P0_2)
                            break

                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                        try:

                            if map[P0x+i][P0y-i] in ['0','1','2'] and P0y - i >= 0:
                                go_south_west(map, P0x, P0y, i, P0_2)
                                break

                            elif map[P0x + i][P0y + i] in ['0','1','2']:
                                go_south_east(map, P0x, P0y, i, P0_2)
                                break

                            elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                                go_north_east(map, P0x, P0y, i, P0_2)
                                break

                            elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                                go_north_west(map, P0x, P0y, i, P0_2)
                                break

                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                            try:

                                if map[P0x + i][P0y + i] in ['0','1','2']:
                                    go_south_east(map, P0x, P0y, i, P0_2)
                                    break

                                elif map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                                    go_north_east(map, P0x, P0y, i, P0_2)
                                    break

                                elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                                    go_north_west(map, P0x, P0y, i, P0_2)
                                    break

                            except Exception as e:
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                                try:

                                    if map[P0x-i][P0y+i] in ['0','1','2'] and P0x - i >= 0:
                                        go_north_east(map, P0x, P0y, i, P0_2)
                                        break

                                    elif map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                                        go_north_west(map, P0x, P0y, i, P0_2)
                                        break
                                except Exception as e:
                                    exc_type, exc_obj, exc_tb = sys.exc_info()
                                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                    print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                                    try:
                                        if map[P0x-i][P0y-i] in ['0','1','2'] and P0x - i >= 0 and P0y - i >= 0:
                                            go_north_west(map, P0x, P0y, i, P0_2)
                                            break

                                    except Exception as e:
                                        exc_type, exc_obj, exc_tb = sys.exc_info()
                                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                        print(exc_type, fname, exc_tb.tb_lineno, file=sys.stderr)
                                        ultimate_case(map, P0x, P0y)
                                        break
        
        radius += 1
        
