import sys
import random
sys.path.append("../")
from gameModules import snakeGame as game

hdX = 0
hdY = 0
noGo = (0, 0)

def run():
    game.start(True)
    pass

def check2(sX, sY, parts = []):
    return True

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
    
    global hdX, hdY
    snX = game.snackx
    snY = game.snacky
    dist = [hdX - snX, hdY - snY]
    
    for c in range(2):
        randir = random.choice([-1,1])
        if snX - hdX == 0:
            if snY - hdY > 0 and noGo != (0, 1):# and willCol == False:
                #If the snack is below the snake, look down.
                #print(f"Food is below. Moving down. Y: {snY-hdY}; {dist}")
                game.diry = 1
                game.dirx = 0
                
                hdY += 1
            elif snY - hdY < 0 and noGo != (0, -1):
                #If the snack is above the snake, look up.
                #print(f"Food is above. Moving up. Y: {snY-hdY}; {dist}")
                game.diry = -1
                game.dirx = 0
                
                hdY -= 1
                
            elif snY - hdY > 0 and noGo == (0, 1):# and willCol == False:
                #If the snack is below the snake, look down.
                #print(f"Food is below. Moving down. Y: {snY-hdY}; {dist}")
                game.diry = 0
                game.dirx = randir
                
                hdY += 1
            elif snY - hdY < 0 and noGo == (0, -1):
                #If the snack is above the snake, look up.
                #print(f"Food is above. Moving up. Y: {snY-hdY}; {dist}")
                game.diry = 0
                game.dirx = randir
                
                hdY -= 1
                
        elif snX - hdX > 0 and noGo != (1, 0):
            #If the snack to the right of the snake, look right.
            #print(f"Food at right. Moving right. X: {snX-hdX}; {dist}")
            game.dirx = 1
            game.diry = 0
            
            hdX += 1
        elif snX - hdX < 0 and noGo != (-1, 0):
            #If the snack to the left of the snake, look left.
            #print(f"Food at left. Moving left. X: {snX-hdX}; {dist}")
            game.dirx = -1
            game.diry = 0
            
            hdX -= 1
    
        elif snX - hdX > 0 and noGo == (1, 0):
            #If the snack to the right of the snake, look right.
            #print(f"Food at right. Moving right. X: {snX-hdX}; {dist}")
            game.dirx = randir
            game.diry = 0
            
            hdX += 1
        elif snX - hdX < 0 and noGo == (-1, 0):
            #If the snack to the left of the snake, look left.
            #print(f"Food at left. Moving left. X: {snX-hdX}; {dist}")
            game.dirx = randir
            game.diry = 0
            
            hdX -= 1
    
    #print(f"Hd: {hdX}, {hdY}")
    
if __name__ == "__main__":
    run()