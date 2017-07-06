from random import randint

target_in_screen =(('tree','compass','hole'),('fence','shrubs'),('maxine','girl','parchment','well','bushes','rock','shop'),\
                   ('clothes','bailey','hammer','marbles','sign','desk'),('guard','river','rope','sharpener','rod','raft'),\
                   ('john','peddler','igor','tent','clarinet'),\
                   ('bray','clock','lucious','stable','haberdashery','cart','hands','enzo','sword','octopus'),\
                   ('dario','machine','suits'),('mud','pile','spider','cogs'),('samara','desert','woman'),\
                   ('monolith','drawbridge','palace'),(),(),(),('vincent'),('chest','chamber'),('maiodin','basileus','prism'),\
                   ())
current_inv = ['gold',50,'dagger','clothes']
action_list = ('look','take','talk','go','open','use')
direction_access = {'north':True,'west':False,'east':True,'south':False}
direction = ['north','west','east','south']
event_dict = {'last':True,'none':False,'compass_get':False,'sharp_dagger':False,'cut_shrub':False,'rock_get':False,'rope_get':False,\
              'doll_get':False,'cloak_get':False,'bailey_hug':False,'hammer_get':False,'marbles_get':False,'sword_get':False,\
              'sword_give':False,'hands_get':False,'clarinet_get':False,'turtle_get':False,'river_cross':False,'octopus_get':False,\
              'cogs_get':False,'whistle_get':False,'clean_octopus':False,'guitar_get':False,'give_octopus':False,'clock_game':False,\
              'key_get':False,'wrestle_igor':False,'clock_fix':False,'orb_get':False,'desert_get':False,'secret_passage':False,\
              'vincent_trust':False,'emerald_get':False,'maiodin_nope':False,'emerald_use':False}
counter = ('%','$','&','*')
move_dict = {'n':'north','s':'south','w':'west','e':'east'}

def Introduction():
    splash = open('splash.txt','r')
    line = splash.readline()
    while line[0] != '*':
        print(line.strip('\n'))
        line = splash.readline()
    input('Press ENTER to continue')
    intro = open('introEndF.txt','r')
    line = intro.readline()
    count = 1
    while count < 13:
        while line[0] != '*':
            print(line.strip('\n'))
            line = intro.readline()
        count = count + 1
        line = intro.readline()
        input()
    input('Press ENTER to continue')
    line = intro.readline()
    while line[0] != '*':
        print(line.strip('\n'))
        line = intro.readline()

    
def initiate_game():
    print('This game is quite simple. You interact with the game by typing two word commands')



def EndGame():
    end = open('introEndF.txt.','r')
    line = end.readline()
    while line[0] != '&':
        line = end.readline()
    line = end.readline()
    while line[0] != '%':
        print(line.strip('\n'))
        line = end.readline()


def location(current):
    this_screen = True 
    description(current)
    while this_screen:
        this_move = get_move(current)
        current_new = make_move(this_move,current)
        if event_dict["emerald_use"] == True:
            current_new = 17
        if current_new != current:
            this_screen = False
    return current_new


def descr_print(count,scene_info):
    line = scene_info.readline()
    while line[0] != counter[count]:
        line = scene_info.readline()
    line = scene_info.readline()
    flag = line[0:len(line)-1]
    line = scene_info.readline()
    if str(event_dict[line[0:len(line)-6]]) == flag:
        dir_count = 0
        for k in line[len(line)-5:len(line)-1]:
            if k == '1':
                direction_access[direction[dir_count]] = True
                dir_count += 1
            elif k == '0':
                direction_access[direction[dir_count]] = False
                dir_count += 1
        line = scene_info.readline()
        while line[0] != counter[count+1]:
            print(line.strip('\n'))
            line = scene_info.readline()
        terminate = True
    elif str(event_dict[line[0:len(line)-6]]) != flag:
        count = count + 1
        terminate = False

    return count,terminate

              
def description(current):
    count = 0
    scene_info = open('scene_descriptionsF.txt','r')
    line = scene_info.readline()
    while line[0:len(line)-1] != str(current):
        line = scene_info.readline()
    terminate = False
    while not terminate:
        count,terminate = descr_print(count,scene_info)
    scene_info.close()







    
def get_move(current):
    blank = False
    while not blank:
        blank = True
        move = input('What would you like to do? \n')
        if move == 'boolean':
            print(event_dict)
        if move == 'inventory' or move == 'i':
            print('\nYour current inventory consists of:\n')
            for k in current_inv[2:len(current_inv)]:
                print(k)
            print('You have',current_inv[1],'Gold\n')
            blank = False
        where_blank = move.find(' ')
        if where_blank == -1 and move != 'inventory' and move != 'i':
            blank = False
            print("\nThat doesn't make any sense.\n")
        if blank:
            move = check_move(move,current)
            blank = move[2]

    return move


def check_move(move,current):
    valid = True
    blank = move.find(' ')
    action = move[0:blank]
    target = move[blank + 1:len(move)]
    target = target.lower()
    if target == 'n' or target == 'e' or target == 's' or target == 'w':
        target = move_dict[target]
    if action not in action_list or (target not in target_in_screen[current] and target not in current_inv\
                                     and target not in direction):
        print("\nSorry, that doesn't work.\n")
        valid = False
    if valid == True and action == 'go' and direction_access[target] == False:
        print('\nYou cannot go there\n')
        valid = False
    if valid == True and action == 'use' and target not in current_inv:
        print('\nYou do not have the',target,'\n')
        valid = False
    
    return (action,target,valid)


def make_move(move,current):
    for k in range(len(action_list)):
        if move[0] == action_list[k]:
            act = k
    if act == 0:
        look(current,move[1])
    elif act == 1:
        take(current,move[1])
    elif act == 2:
        talk(current,move[1])
    elif act == 3:
        current = go(current,move[1])
    elif act == 4:
        open_target(current,move[1])
    elif act == 5:
        use(current,move[1])

    return current










def look_print(count,looktxt):
    line = looktxt.readline()
    while line[0] != counter[count]:
        line = looktxt.readline()
    line = looktxt.readline()
    flag = line[0:len(line)-1]
    line = looktxt.readline()
    if str(event_dict[line[0:len(line)-1]]) == flag:
        line = looktxt.readline()
        while line[0] != counter[count+1]:
            print(line.strip('\n'))
            line = looktxt.readline()
        terminate = True
    elif str(event_dict[line[0:len(line)-1]]) != flag:
        count = count + 1
        terminate = False

    return count,terminate

def look(current,target):
    count = 0
    terminate = False
    looktxt = open('lookF.txt','r')
    done = False
    line = looktxt.readline()
    while not done:
        if line[0] == '#':
            if line[1:len(line)-1] == target:
                done = True
        if not done:
            line = looktxt.readline()
        if line[0:len(line)] == 'the_end':
                print('\nYou cannot look at that\n')
                done = True
                terminate = True
    while not terminate:
        count,terminate = look_print(count,looktxt)
    looktxt.close()





def take_print(count,taketxt):
    last = False
    line = taketxt.readline()
    while line[0] != counter[count]:
        line = taketxt.readline()
    line = taketxt.readline()
    flag = line[0:len(line)-1]
    line = taketxt.readline()
    if str(event_dict[line[0:len(line)-1]]) == flag:
        if count == 2:
            last = True
        line = taketxt.readline()
        while line[0] != counter[count+1]:
            print(line.strip('\n'))
            line = taketxt.readline()
        terminate = True
    elif str(event_dict[line[0:len(line)-1]]) != flag:
        count = count + 1
        terminate = False

    return count,terminate,last,line
    

def take(current,target):
    taketxt = open('takeF.txt','r')
    line = taketxt.readline()
    terminate = False
    last = False
    count = 0
    done = False
    if target in current_inv:
        print('\nYou already have the',target,'\n')
        done = True
        terminate = True
    while not done:
        if line[0] == '#':
            if line[1:len(line)-1] == target:
                done = True
        if not done:
            line = taketxt.readline()
        if line[0:len(line)] == 'the_end':
                print('\nThat is not available to take\n')
                done = True
                terminate = True
    while not terminate:
        count,terminate,last,line = take_print(count,taketxt)
    if last == True:
        current_inv.append(target)
        event_dict[line[1:len(line)-1]] = True
    taketxt.close()










def use_print(count,target,eventtxt,terminate,subject):
    count = count + 1
    line = eventtxt.readline()
    if line[0:len(line)-1] != subject:
        line = eventtxt.readline()
        while line[0] != '%':
            print(line.strip('\n'))
            line = eventtxt.readline()
        terminate = True
    else:
        while line[0] != '%':
            line = eventtxt.readline()
    while not terminate:
        line = eventtxt.readline()
        flag = line[0:len(line)-1]
        line = eventtxt.readline()
        if str(event_dict[line[0:len(line)-1]]) == str(flag):
            line = eventtxt.readline()
            while line[0] != counter[count]:
                print(line.strip('\n'))
                line = eventtxt.readline()
            terminate = True
        elif str(event_dict[line[0:len(line)-1]]) != flag and terminate == False:
            while line[0] != counter[count]:
                line = eventtxt.readline()
            count = count+1
    if count == 3:
        line = eventtxt.readline()
        event_dict[line[0:len(line)-1]] = True
        line = eventtxt.readline()
        if line[0:len(line)-1] != 'none':
            for k in range(len(current_inv)):
                if line[0:len(line)-1] == current_inv[k]:
                    item_to_delete = k
            del current_inv[item_to_delete]
        line = eventtxt.readline()
        if line[0:len(line)-1] != 'none':
            current_inv.append(line[0:len(line)-1])
        line = eventtxt.readline()
        if line[0:len(line)-1] != 'none':
            current_inv[1] = current_inv[1] + int(line[0:len(line)-1])
        line = eventtxt.readline()
        if line[0:len(line)-1] != 'none':
            direction_access[line[0:len(line)-1]] = True
            
        

    return terminate,eventtxt
                

        
def use(current,target):
    count = 0 
    valid = False
    eventtxt = open('eventsF.txt','r')
    line = eventtxt.readline()
    terminate = False
    subject = input('\nWhat/Whom would you like to use it with? \n')
    subject = subject.lower()
    if subject not in target_in_screen[current]:
        print('\nYou cannot use the',target,'there.\n')
        terminate = True
    while not terminate:
        while line[0] != '#':
            line = eventtxt.readline()
        line = eventtxt.readline()
        if line[0:len(line)-1] == target:
            terminate,eventtxt = use_print(count,target,eventtxt,terminate,subject)
            if event_dict['clock_game'] == True and event_dict['clock_fix'] == False:
                event_dict['clock_game'] = clockPuzzle()
                if event_dict['clock_game']:
                    event_dict['clock_fix'] = True
                    current_inv.append('orb')
                    for k in range(len(current_inv)):
                        if current_inv[k] == 'hands':
                            item_to_delete = k
                    del current_inv[item_to_delete]
        elif line[0:len(line)-1] == 'the_end':
            line = eventtxt.readline()
            print(line)
            eventtxt.close()

    return










def talk_print(count,talktxt):
    line = talktxt.readline()
    while line[0] != counter[count]:
        line = talktxt.readline()
    line = talktxt.readline()
    flag = line[0:len(line)-1]
    line = talktxt.readline()
    if str(event_dict[line[0:len(line)-1]]) == flag:
        line = talktxt.readline()
        while line[0] != counter[count+1]:
            print(line.strip('\n'))
            line = talktxt.readline()
        terminate = True
    elif str(event_dict[line[0:len(line)-1]]) != flag:
        count = count + 1
        terminate = False

    return count,terminate

    
def talk(current,target):
    count = 0
    terminate = False
    done = False
    talktxt = open('talkF.txt','r')
    line = talktxt.readline()
    while not done:
        if line[0] == '#':
            if line[1:len(line)-1] == target:
                done = True
        if not done:
            line = talktxt.readline()
        if line[0:len(line)] == 'the_end':
                print('\nThat is not available to talk to\n')
                done = True
                terminate = True
    while not terminate:
        count,terminate = talk_print(count,talktxt)
    talktxt.close()

    









def go(current,target):
    
    if target == 'north':
        ncurrent = current + 4
    if target == 'south':
        ncurrent = current - 4
    if target == 'east':
        ncurrent = current + 1
    if target == 'west':
        ncurrent = current - 1

    return ncurrent



def clockPuzzle():
    game = True
    time = input('Set clock hands to time(hh:mm): ')
    if time == "2:47" or time == "02:47":
        clocktxt = open('clockF.txt','r')
        line = clocktxt.readline()
        while line[0] != '#':
            print(line.strip('\n'))
            line = clocktxt.readline()
        input('Press any key to continue')
        line = clocktxt.readline()
        while line[0] != '#':
            print(line.strip('\n'))
            line = clocktxt.readline()

        play = True
        while play:
            lower = 0
            upper = 100
            target = randint(0,100)
            player_win = False
            clock_win = False
            guessed = False
            
            while not guessed:
                valid = False
                while not valid:
                    player = input('\nChoose a number: ')
                    if player.isdigit() == True:
                        valid = True
                    else:
                        print('Invalid value')
                player = int(player)
                if player < lower or player > upper:
                    print('Your guess was not in the range. You lose a turn.\n')
                    valid = False
                if valid:
                    if player == target:
                        player_win = True
                        print('That was the correct number!')
                    else:
                        if player < target:
                            lower = player+1
                        if player > target:
                            upper = player-1
                if not player_win:
                    clock = randint(lower,upper)
                    print("The Clock's guess is: ",clock)
                    if clock == target:
                        clock_win = True
                    else:
                        if clock < target:
                            lower = clock+1
                        if clock > target:
                            upper = clock-1
                if player_win or clock_win:
                    guessed = True
                else:
                    print('\nThe correct number has not yet been guessed\n')
                    print('---The new limits are:\n---lower:',lower,'\n---upper:',upper)
            if player_win:
                print('\nCongratulations! You beat the clock!\n')
                play = False
            if clock_win:
                print('\nUnfortunately, the clock beat you!')
                retry = input('Press any key to try again. Type x to exit the Clock Puzzle: ')
                if retry == 'x' or retry == 'X':
                    play = False
        line = clocktxt.readline()
        while line[0:len(line)-1] != str(player_win):
            line = clocktxt.readline()
        line = clocktxt.readline()
        while line[0] != '*':
            print(line.strip('\n'))
            line = clocktxt.readline()
        clocktxt.close()
    else:
        print("Nothing happens")
        player_win = False
               
    return player_win
    




## MAIN ##

Introduction()

#initiate_game()

game_in_progress = True

while game_in_progress:

    end_flag = True
    
    current_screen = 0#int(input('enter screen'))

    while end_flag :

        current_screen = location(current_screen)

        if current_screen == 17:
            end_flag = False



    EndGame()

    game_in_progress = False

print("Thank You For Playing ""PRISM""! We hope you enjoyed the game/nYou Scored 100/100. It is not possible to acheive any\
    other score. You are super Cool!")

    
