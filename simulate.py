import random
#simulates title fight or normal fight of two fighters
def simulate_fight(fighter1,fighter2,round_num):

    f1_ts=0
    f2_ts=0

    for r in range(1,round_num+1):
        f1_rs,f2_rs=simulate_round(fighter1,fighter2)
        f1_ts+=f1_rs
        f2_ts+=f2_rs
        print("Round:"+ str(r)+"   "+fighter1.name+": "+str(f1_rs)+"    "+fighter2.name+": "+ str(f2_rs)+"\n")
    print(fighter1.name+": "+ str(f1_ts))
    print(fighter2.name+": "+ str(f2_ts))

    if f1_ts>f2_ts:
        print("\n")
        print(fighter1.name + " wins! " + str(f1_ts) +" to " + str(f2_ts))
        print("\n")
    elif f2_ts>f1_ts:
        print("\n")
        print(fighter2.name + " wins! "+ str(f2_ts) +" to " + str(f1_ts))
        print("\n")
    else:
        print("\n")
        print("It is a draw!")
        print("\n")

#Round by round simulation
def simulate_round(f_1,f_2):
    # Returns the score of a fighter for a round
    def score_round(fighter):
        striking = fighter.striking_score * random.uniform(.9,1.5)
        grappling = fighter.grappling_score * random.uniform(.9,1.5)
        defense = fighter.defense_score * random.uniform(.9,1.3)
        return striking+grappling+defense
    
    f1_score = score_round(f_1)
    f2_score = score_round(f_2)
    
    if abs(f1_score-f2_score) < 1:
        return (10,10)
    elif abs(f1_score-f2_score) < 15:
        if f1_score>f2_score:
            return (10,9)
        else:
            return (9,10)
    elif abs(f1_score-f2_score) > 15:
        if f1_score>f2_score:
            return (10,8)
        else:
            return (8,10)

def multiple_fights(fighter1,fighter2,num_rounds,num_fights):
    f1_twins=0
    f2_twins=0
    draw=0
    for r in range (1, num_fights+1):
        f1_ts=0
        f2_ts=0
        for r in range(1,num_rounds+1):
            f1_rs,f2_rs=simulate_round(fighter1,fighter2)
            f1_ts+=f1_rs
            f2_ts+=f2_rs
        if f1_ts>f2_ts:
            f1_twins+=1
        elif f2_ts>f1_ts:
            f2_twins+=1
        else:
            draw+=1
    if draw==0:
        print("\n")
        print("Out of " + str(num_fights)+ " fights... "+fighter1.name +" won "+ str(f1_twins) +" times and "+fighter2.name +" won "+ str(f2_twins)+ " times")
    else:
        print("\n")
        print("Out of " + str(num_fights)+ " fights... "+fighter1.name +" won "+ str(f1_twins) +" times and "+fighter2.name +" won "+ str(f2_twins)+ " times and " + str(draw)+ " fights were draws")
