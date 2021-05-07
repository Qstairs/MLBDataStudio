

class Game:
    def __init__(self, data):
        for key, val in data.items():
            try:
                setattr(self, key, int(val))
            except:
                setattr(self, key, val)

    def __str__(self):
        return str(self.__dict__)