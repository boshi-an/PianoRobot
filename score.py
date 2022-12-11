import time

note_list = [
    "_",
    "F3",
    #"#F3",
    "G3",
    #"#G3",
    "A4",
    #"#A4",
    "B4",
    "C4",
    #"#C4",
    "D4",
    #"#D4",
    "E4",
    "F4",
    #"#F4",
    "G4",
    #"#G4",
    "A5",
    #"#A5",
    "B5",
    "C5",
    #"#C5",
    "D5",
    #"#D5",
    "E5",
    "F5",
    #"#F5",
    "G5",
    #"#G5",
    "A6",
    #"#A6",
    "B6",
    "C6",
    #"#C6",
    "D6",
    #"#D6",
    "E6",
    "F6"
]

class Note() :
    
    def __init__(self, name, length) :
        
        if name not in note_list :
            
            raise ValueError("{} is not playble on the melodion.".format(name))
    
        self.id = note_list.index(name.upper())
        self.lt = length
    
    def duration(self, tempo) :
        
        return 60 / tempo * self.lt

class Score() :
    
    '''
    tempo: howmany full notes per minute
    init_list: the initial note list to play
    '''
    def __init__(self, tempo, init_list=[]) :
        
        self.score = init_list
        self.tempo = tempo
    
    def append(self, note) :
        
        self.score.append(note)
    
    def set_tempo(self, tempo) :
        
        self.tempo = tempo
    
    def player(self) :
        
        pass
        
class Player() :

    def __init__(self, score) :
        
        self.start = []
        cur_time = 0
        self.score = score
        self.score.append(Note("_", 1))
        for note in self.score.score :
            self.start.append(cur_time)
            cur_time += note.duration(self.score.tempo)
        self.start.append(cur_time)
        self.cur_t = 0 # current playing progress
        self.cur_n = 0 # current playing note
    
    def reset(self) :
        
        self.cur_t = 0
        self.cur_n = 0
    
    '''
    t: the current time of playing. t need to be ascending during playing
    return value: (current note, remaining playing time of current note, next note, done)
    '''
    def get_state(self, t) :
        
        if t < self.cur_t :
            raise ValueError("Please reset player before playing again.")
        else :
            self.cur_t = t

        while self.cur_n < len(self.score.score) and t >= self.start[self.cur_n+1] :  
            self.cur_n += 1
        
        if self.cur_n+1 < len(self.score.score) :
            return self.score.score[self.cur_n].id, self.start[self.cur_n+1]-t, self.score.score[self.cur_n+1].id, False
        else :
            return 0, 0, 0, True


if __name__ == "__main__" :
    
    score = Score(tempo=20)
    score.append(Note("C5", 0.25))
    score.append(Note("C5", 0.25))
    score.append(Note("G5", 0.25))
    score.append(Note("G5", 0.25))
    
    player = Player(score)
    
    start_time = time.time()
    
    while True :
        dt = time.time() - start_time
        c, t, c2, done = player.get_state(dt)
        print(c, t, c2, done)
        time.sleep(0.1)
        if done :
            break