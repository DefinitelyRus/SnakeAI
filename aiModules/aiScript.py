from gameModules import snakeGame

def run():
    snakeGame.start(True)
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
    pass