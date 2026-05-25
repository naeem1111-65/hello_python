import random

def get_choices():
    player_choice=input("Enter a choice(rock,paper,scissers):")
    options=["rock","paper","scissors"]
    computer_choice=random.choice(options)
    choice={"player":player_choice,"computer":computer_choice}

    return choice

def check_win(player,computer):
    print(f"You chose {player},computer chose {computer}")
    if player==computer:
        return "It's tie bro"
    elif player=="rock":
        if computer=="scissors":
            return("Rock smashes scissors. Sooo you win bady ")
        else:
            return(" OHh Paper cover rock!. And you loss man")
    elif player=="paper":
        if computer=="scissors":
            return("scissors cuts paper . Sooo you loss stupit ")
        else:
            return(" OHh Paper cover rock!. And you win")
    elif player=="scissors":
        if computer=="rock":
            return("Rock smashes scissors. Sooo you loss idiot ")
        else:
            return(" scissors cuts paper!. And you win man")
    else:
        return "Invalid choice!"
choices=get_choices()
result=check_win(choices["player"],choices["computer"])
print(result)
