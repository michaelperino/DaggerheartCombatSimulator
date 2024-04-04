from collections import Counter
import copy
import random
import itertools
import creatures

class simulation:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.fear = 0
        self.actions = 0
        self.player_idx = 0
        self.monster_idx = 0
    
    def run_sim(self):
        while len(self.players) > 0 and len(self.monsters) > 0:
            fear = False
            monster = self.monsters[0]
            while not fear:
                self.actions += 1
                player = self.players[self.player_idx%len(self.players)]
                att_out = player.attack()
                fear = att_out[0]
                d = monster.defend(att_out[1],att_out[2])
                #print(player,monster,att_out,d)
                if monster.hitpoints <= 0:
                    self.monsters.pop(0)
                    if len(self.monsters) == 0:
                        break
                    monster = self.monsters[0]
                self.player_idx += 1
            if len(self.monsters) > 0:
                player = self.players[0]
                while self.actions > 0:
                    self.actions -= 1
                    monster = self.monsters[self.monster_idx%(len(self.monsters))]
                    att_out = monster.attack()
                    d = player.defend(att_out[1],att_out[2])
                    #print(monster,player,att_out,d)
                    if player.hitpoints <= 0:
                        self.players.pop(0)
                        if len(self.players) == 0:
                            break
                        player = self.players[0]
                    self.monster_idx += 1

        #print(list(map(str,self.players)),list(map(str,self.monsters)))
        return([list(map(str,self.players)),list(map(str,self.monsters))])
                
if __name__ == "__main__":
    players = []
    players.append(creatures.player())
    players[-1].load("Marlowe")
    players.append(creatures.player())
    players[-1].load("El Jefe")
    players.append(creatures.player())
    players[-1].load("Brev")

    
    monsters = []
    monsters.append(creatures.monster())
    monsters[-1].load("Thistlefolk Ambusher")
    monsters.append(creatures.monster())
    monsters[-1].load("Thistlefolk Ambusher")
    monsters.append(creatures.monster())
    monsters[-1].load("Thistlefolk Ambusher")
    monsters.append(creatures.monster())
    monsters[-1].load("Thistlefolk Thief")

    outs = []
    sim = simulation()
    wins = 0
    losses = 0
    survivals = Counter()
    deaths = Counter()
    alls = []
    for i in players:
        alls.append(i.name)
    for i in monsters:
        alls.append(i.name)
    print(alls)
    for i in range(10):
        sim.players = copy.deepcopy(players)
        sim.monsters = copy.deepcopy(monsters)
        random.shuffle(sim.players)
        random.shuffle(sim.monsters)
        #print(list(map(str,sim.players)),list(map(str,sim.monsters)))
        out = sim.run_sim()
        if len(out[0]) > len(out[1]):
            wins += 1
        else:
            losses += 1
        deaths.update(alls)
        temps = []
        for i in sim.players:
            temps.append(i.name)
        for i in sim.monsters:
            temps.append(i.name)
        deaths.subtract(temps)
        survivals.update(temps)
    print("WINS ",wins,"     LOSSES ",losses)
    print(survivals.most_common())
    print(deaths.most_common())

