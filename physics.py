from servo import HandServo, ArmServo
from planning import Planner
from score import Note, Score
import time

score = Score(tempo=20)
score.append(Note("C5", 0.5))
score.append(Note("C5", 0.5))
score.append(Note("G5", 0.5))
score.append(Note("G5", 0.5))
score.append(Note("A6", 0.5))
score.append(Note("A6", 0.5))
score.append(Note("G5", 1.0))
score.append(Note("F5", 0.5))
score.append(Note("F5", 0.5))
score.append(Note("E5", 0.5))
score.append(Note("E5", 0.5))
score.append(Note("D5", 0.5))
score.append(Note("D5", 0.5))
score.append(Note("C5", 1.0))

arm = ArmServo()
arm.init_pose()
hand = HandServo()
hand.set_angle([0, 0, 0, 0, 0])
optimizer = Planner(score, 4, 2, 0.3, 0.25)
finger_seq = optimizer.plan()

d0 = score.score[0].id + finger_seq[0]*2

print("The first finger is {}", finger_seq[0])
print("Ready to go, input 'Y' to play!")
s = input()

if s != 'Y' :
    del hand
    del arm
    exit()
else :
    # Ready to go
    time.sleep(5)

arm.move_to(-2)

for finger, note in zip(finger_seq, score.score) :
    
    print(finger, note.id)
    
    displace = note.id + finger*2
    finger_angle = [0, 0, 0, 0, 0]
    finger_angle[finger+1] = 40
    
    arm.move_to(-displace+d0-2)
    hand.set_angle(finger_angle)
    
    time.sleep(note.lt)
    
    finger_angle = [0, 0, 0, 0, 0]
    hand.set_angle(finger_angle)

arm.move_to(0)
time.sleep(1)

del hand
del arm