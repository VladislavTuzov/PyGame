class Pattern:
    def __init__(self, pattern):
        self.pattern = list(pattern)

    def add_top_gate(self):
        wall = self.pattern[0]
        new_wall = self.with_gate(wall)
        self.pattern[0] = new_wall

    def add_bottom_gate(self):
        wall = self.pattern[-1]
        new_wall = self.with_gate(wall)
        self.pattern[-1] = new_wall

    def add_left_gate(self):
        wall = [line[0] for line in self.pattern]
        new_wall = self.with_gate(wall)
        self.pattern = [s + line[1:] for s, line in zip(new_wall, self.pattern)]

    def add_right_gate(self):
        wall = [line[-1] for line in self.pattern]
        new_wall = self.with_gate(wall)
        self.pattern = [line[:-1] + s for s, line in zip(new_wall, self.pattern)]

    @staticmethod
    def with_gate(wall):
        wall_len = len(wall)
        if wall_len % 3 == 0:
            gate = 'G' * (wall_len // 3)
            new_wall = 'W' * (wall_len // 3) + gate + 'W' * (wall_len // 3)
        else:
            if wall_len % 2 == 1:
                gate_len = wall_len // 2
                wall = 'W' * ((wall_len - gate_len) // 2)
                new_wall = wall + 'G' * gate_len + wall
            else:
                gate_len = wall_len // 2 - wall_len // 2 % 2
                wall = 'W' * ((wall_len - gate_len) // 2)
                new_wall = wall + 'G' * gate_len + wall

        return new_wall


def get_random_pattern():
    return pattern


pattern = ('           WWWWW',
           '               W',
           '               W',
           '               W',
           '               G',
           '               G',
           '               G',
           'W              G',
           'W   W      W   W',
           'W              W',
           'WWWWGGGGGGGGWWWW',)


spawn = ('WWWWWWWWW',
         'W       W',
         'W       W',
         'W   B   W',
         'W       W',
         'WWWWWWWWW',)

scheme = ('P-#-#',
          '  |  ',
          '#-#  ',
          '  |  ',
          '  #-S')
