
from fighterbase import fighter_database
from simulate import simulate_fight,multiple_fights
import pandas as pd

#function searches list of dictonaries to find matching name
def find_fighter(name):
    return fighter_database.get(name.lower())
    
#prompts user to select fighter 1 from database
fighter_a = find_fighter(input("Choose your first fighter: "))

#displays stats and name for first fighter
print("\n")
print("Fighter 1 selected:", fighter_a.name + ", "+ fighter_a.nickname)
print("Stats:", fighter_a.raw_stats)
print("\n")

#prompts user to select fighter 2 from database
fighter_b = find_fighter(input("Choose your second fighter: "))



#displays stats and name for second fighter
print("\n")
print("Fighter 2 selected:", fighter_b.name + ", "+ fighter_b.nickname)
print("Stats:", fighter_b.raw_stats)
print("\n")

#prompts user to select number of rounds(3 or 5)
is_title_fight=input("Is this a title fight? ")
print("\n")
if is_title_fight.lower()=="no":
    num_rounds=3
else:
    num_rounds=5

num_fights=int(input("How many fights would you like to simulate? "))
#Simulates fight
if num_fights==1:
    simulate_fight(fighter_a,fighter_b,num_rounds)
else:
    multiple_fights(fighter_a,fighter_b,num_rounds,num_fights)

