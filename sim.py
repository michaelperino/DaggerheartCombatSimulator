from collections import Counter
import copy
import random
import creatures

class simulation:
    def __init__(self):
        self.players = []
        self.monsters = []
        self.fear = 0
        self.actions = 0
        self.player_idx = 0
        self.monster_idx = 0
        self.player_actions = 0
        self.monster_actions = 0
    
    def run_sim(self):
        self.player_actions = 0
        self.monster_actions = 0
        fear = random.randint(1,10) <= 2
        if fear:
            self.actions = 4
        while len(self.players) > 0 and len(self.monsters) > 0:
            monster = self.monsters[0]
            while not fear:
                self.player_actions += 1
                self.actions += 1
                player = self.players[self.player_idx%len(self.players)]
                att_out = player.attack()
                fear = not att_out[0]
                for i in range(att_out[3]+1):
                    if i < len(self.monsters):
                        monster = self.monsters[i]
                        d = monster.defend(att_out[1],att_out[2]*(att_out[4] if i > 0 else 1))
                        #print(player,monster,att_out,d)
                        if monster.hitpoints <= 0:
                            self.monsters.pop(i)
                            if len(self.monsters) == 0:
                                break
                            #monster = self.monsters[0]
                self.player_idx += 1
            if len(self.monsters) > 0:
                self.monster_actions += 1
                player = self.players[0]
                while self.actions > 0:
                    self.actions -= 1
                    monster = self.monsters[self.monster_idx%(len(self.monsters))]
                    att_out = monster.attack(self.fear)
                    self.fear -= att_out[5]
                    for i in range(att_out[3]+1):
                        if i < len(self.players):
                            player = self.players[i]
                            d = player.defend(att_out[1],att_out[2])
                            #print(monster,player,att_out,d)
                            if player.hitpoints <= 0:
                                self.players.pop(i)
                                if len(self.players) == 0:
                                    break
                                #player = self.players[0]`
                    self.monster_idx += 1
            fear = False
        #print(list(map(str,self.players)),list(map(str,self.monsters)))
        return([list(map(str,self.players)),list(map(str,self.monsters)),self.player_actions,self.monster_actions])
                
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
    sim_num = 100000
    total_play = 0
    total_mon = 0
    for i in range(sim_num):
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
        total_play += out[2]
        total_mon += out[3]
    print("WINS ",wins,"     LOSSES ",losses)
    print("PLAY ",total_play/sim_num,"      MON ",total_mon/sim_num,"     TOTAL ",(total_play+total_mon)/sim_num)
    print(survivals.most_common())
    print(deaths.most_common())

