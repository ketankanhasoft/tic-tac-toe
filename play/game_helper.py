

class GameHelper:

    GameList={}

    def __init__(self, game_id):
        self.game_id = game_id
        if game_id not in self.GameList:
            self.GameList[game_id] = {}
        pass
    
    def game_info(self):
        return self.GameList.get(self.game_id)