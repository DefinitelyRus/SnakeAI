import sys
import random
sys.path.append("../")
from gameModules import snakeGame as game

# x = 0
# y = 0
# xl = [0, 0, -1, 1]
# yl = [-1, 1]


def run():
    game.start(True)
    pass

def check():
    """
    Stage 1:
    This function first checks if there are obstacles (such as the tail), if an obstacle is going to be hit in the next frame update, it turns to the direction where there is no obstacle.
    
    If an obstacle is present on both immediate directions, it checks which one is further, then turns to that direction.
    
    If both directions are equally far, it randomly chooses where to turn.
    
    If there are no safe turns, it will simply continue to the next turn (and probably die).
    
    Stage 2:
    If this check returns False, the AI will turn to the direction closest to the snack. So if the snack is higher by 3 units and 6 units to the right, the AI will turn upwards until the snack 0 units higher and 6 units to the right of the snake. When either X or Y reaches 0, the AI turns again to the direction closest to the snack.
    
    If the snack is exactly diagonal (equal both X and Y), the AI will pass 1 frame update, then does the check mentioned above.
    
    Note:
    This process will continue until the AI loses. This does not use Machine Learning and cannot improve from its mistakes.
    """
    
    #global snX, snY, hdX, hdY
    snX = game.snackx
    snY = game.snacky
    hdX = game.headPosX
    hdY = game.headPosY
    dist = [hdX - snX, hdY - snY]
    print(dist)
    print(f"Head: {hdX}, {hdY}\nSnack: {snX}, {snY}")
    if abs(hdX - snX) > abs(hdY - snY):
        print(f"Checking vertical.")
        #If the distance between the snake and the snack is further horizontally than vertically...
        if hdY - snY > 0:
            #If the snack is below the snake, look down.
            print(f"Food is below. Moving down. Y: {hdY-snY}; {dist}")
            game.diry = 1
            game.dirx = 0
            
            hdY += 1
        elif hdY - snY < 0:
            #If the snack is above the snake, look up.
            print(f"Food is above. Moving up. Y: {hdY-snY}; {dist}")
            game.diry = -1
            game.dirx = 0
            
            hdY -= 1
    else:# abs(snX - hdX) < abs(snY - hdY):
        print(f"Checking horizontal.")
        #If the distance between the snake and the snack is further vertically than horizontally...
        if hdX - snX > 0:
            #If the snack to the right of the snake, look right.
            print(f"Food at right. Moving right. X: {snX-hdX}; {dist}")
            game.dirx = 1
            game.diry = 0
            
            hdX += 1
        elif hdX - snX < 0:
            #If the snack to the left of the snake, look left.
            print(f"Food at left. Moving left. X: {snX-hdX}; {dist}")
            game.dirx = -1
            game.diry = 0
            
            hdX -= 1
#     game.dirx = random.choice(xl)
#     if game.dirx == 0:
#         game.diry = random.choice(yl)
#     
#     pass