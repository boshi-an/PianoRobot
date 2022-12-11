import numpy as np
from score import Score, Note

class Planner() :
    
    '''
    The planner optimizes total loss on the whole trajectory,
    parameters for finger separation, finger lifting delay and horizontal moving speed should be given.
    
    score: the score file for the music
    h_spd: horizontal moving speed of hand, unit in notes/sec
    f_sep: finger separation, unit in notes
    f_dly: finger lift delay time, unit in sec
    t_ovr: max overlap time of finger lifting and horizontal moving, unit in sec
    '''
    def __init__ (self, score, h_spd, f_sep, f_dly, t_ovr) :
        
        self.h_spd = h_spd
        self.f_sep = f_sep
        self.f_dly = f_dly
        self.t_ovr = t_ovr
        self.score = score
        
        self.loss = np.ones((len(self.score.score), 4)) * np.inf
        self.trans = np.zeros((len(self.score.score), 4), dtype=int)
        self.finger = np.zeros((len(self.score.score),), dtype=int)
        
    def calc_loss(self, last_n, cur_n, last_f, cur_f) :
        
        if last_f == 1 :
            return 123123
        if last_f == 2 :
            return 123123
        if cur_f == 1 :
            return 123123
        if cur_f == 2 :
            return 123123
        
        dist = abs((last_n + self.f_sep*last_f) - (cur_n + self.f_sep*cur_f))
        h_time = dist / self.h_spd
        
        if last_f == cur_f :
            delta_t = max(h_time-2*self.t_ovr+2*self.f_dly, 2*self.f_dly)
        else :
            delta_t = max(h_time-2*self.t_ovr+2*self.f_dly, self.f_dly)
        
        return delta_t**2
        
    def plan(self) :
        
        for finger in range(self.loss.shape[1]) :
            
            self.loss[0, finger] = 0
    
        for note in range(1, self.loss.shape[0]) :
            
            for last_f in range(self.loss.shape[1]) :
                
                for cur_f in range(self.loss.shape[1]) :
                    
                    last_note = self.score.score[note-1].id
                    cur_note = self.score.score[note].id
                    cur_min = self.loss[note, cur_f]
                    new_delta = self.calc_loss(last_note, cur_note, last_f, cur_f)
                    new_min = new_delta + self.loss[note-1, last_f]
                    
                    # print(last_note, cur_note, last_f, cur_f, ":", self.loss[note-1, last_f], new_delta, new_min)
                    
                    if cur_min > new_min :
                        self.trans[note, cur_f] = last_f
                        self.loss[note, cur_f] = new_min
        
        print("The DP array:")
        print(self.loss)
        
        min_finger = 0
        min_value = np.inf
        for finger in range(self.loss.shape[1]) :
            
            if self.loss[-1, finger] < min_value  :
                
                min_finger = finger
                min_value = self.loss[-1, finger]
        
        cur_finger = min_finger
        cur_note = self.loss.shape[0]-1
        while cur_note >= 0 :
            self.finger[cur_note] = cur_finger
            cur_finger = self.trans[cur_note, cur_finger]
            cur_note -= 1
        
        print("The best finger oreger:")
        print(self.finger)
        
        print("The corresponding loss:", min_value)
        
        return self.finger

if __name__ == "__main__" :
    
    score = Score(tempo=20)
    score.append(Note("C5", 0.25))
    score.append(Note("C5", 0.25))
    score.append(Note("G5", 0.25))
    score.append(Note("G5", 0.25))
    score.append(Note("A6", 0.25))
    score.append(Note("A6", 0.25))
    score.append(Note("G5", 0.5))
    score.append(Note("F5", 0.25))
    score.append(Note("F5", 0.25))
    score.append(Note("E5", 0.25))
    score.append(Note("E5", 0.25))
    score.append(Note("D5", 0.25))
    score.append(Note("D5", 0.25))
    score.append(Note("C5", 0.5))
    
    optimizer = Planner(score, 4, 2, 0.3, 0.25)
    # print(optimizer.calc_loss(2, 1, 2, 3))
    # print(optimizer.calc_loss(2, 1, 3, 3))
    optimizer.plan()