class Water:
    def __init__(self, volume):
        self.volume = volume
    def get_volume(self):
        return self.volume
    def freeze(self):
        return Ice(self.volume)
class Ice:
    def __init__(self, volume):
        self.volume = volume
    def melt(self):
        return Water(self.volume)

ice = Ice(47)
print(ice)
print(ice.melt().freeze())
for i in range(1,8):
    print(i)