from tamagotchi import Tamagotchi

def print_tams(tamagotchis):
    print()
    for name in sorted(tamagotchis):
        print(tamagotchis.get(name))

def time_pass(tamagotchis):
    for name in sorted(tamagotchis):
        pet = tamagotchis.get(name)
        pet.increment_time()

if  __name__ == "__main__":
    tamagotchis = {}
    while True:
        command = input("Command: ")
        if command == "":
            print()
            break

        l = command.split()
        if l[0] == "create" and len(l) != 1:
            if l[1] in tamagotchis and not tamagotchis.get(l[1]).is_dead():
                print("You already have a Tamagotchi called that.")
            else:
                tamagotchis[l[1]] = Tamagotchi(l[1])
                print_tams(tamagotchis)
                time_pass(tamagotchis)
        elif l[0] == "feed"and len(l) != 1:
            if l[1] in tamagotchis:
                pet = tamagotchis.get(l[1])
                pet.feed()
                print_tams(tamagotchis)
                time_pass(tamagotchis)
            else:
                print("No Tamagotchi with that name.")
        elif l[0] == "play"and len(l) != 1:
            if l[1] in tamagotchis:
                pet = tamagotchis.get(l[1])
                pet.play()
                print_tams(tamagotchis)
                time_pass(tamagotchis)
            else:
                print("No Tamagotchi with that name.")
        elif l[0] == "wait":
            print_tams(tamagotchis)
            time_pass(tamagotchis)
        else:
            print("Invalid command.")
