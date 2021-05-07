
class Pitch:
    def __init__(self, data):
        for key, val in data.items():
            try:
                if key == 'id' or key == 'event_num':
                    setattr(self, key, int(val))
                else:
                    setattr(self, key, float(val))
            except:
                setattr(self, key, val)

        try:
            self.raw_px = self.px
            self.raw_pz = self.pz
            self.px = self.px * -1 # 実データは審判目線なので反転する
        except:
            pass

    def __str__(self):
        return str(self.__dict__)