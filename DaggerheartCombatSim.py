from collections import Counter
import copy
import random
import customtkinter as ctk
import creatures
import creature_editor
import sim
import time


WIDTH,HEIGHT = (1600,1000)

class ChosenMonstersFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.gen_frame()


    def gen_frame(self):
        player_scroll = ctk.CTkScrollableFrame(self,label_text="Chosen Players",height=150,width=WIDTH/4)
        player_scroll.grid(row =1, column=1, padx = 10,pady=(10,10),sticky = "n")
        play_buttons = []
        for i,val in enumerate(self.master.players):
            play_buttons.append(ctk.CTkButton(player_scroll,text=val, command = lambda m=val:self.del_player(m),width=WIDTH/5))
            play_buttons[-1].grid(row=i,column=0,padx=10,pady=(10,0),sticky="w")
        mon_scroll = ctk.CTkScrollableFrame(self,label_text="Chosen Monsters",height=150,width=WIDTH/4)
        mon_scroll.grid(row =3, column=1, padx = 10,pady=(10,10),sticky = "n")
        mon_buttons = []
        for i,val in enumerate(self.master.monsters):
            mon_buttons.append(ctk.CTkButton(mon_scroll,text=val, command = lambda m=val:self.del_monster(m),width=WIDTH/5))
            mon_buttons[-1].grid(row=i,column=0,padx=10,pady=(10,0),sticky="w")
            
    def del_player(self,mon):
        self.master.players.remove(mon)
        self.gen_frame()
    def del_monster(self,mon):
        self.master.monsters.remove(mon)
        self.gen_frame()

class SimFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.gen_frame()


    def gen_frame(self):
        self.enter_label = ctk.CTkLabel(self,text="Enter # of sims:")
        self.enter_label.grid(row=0,column=0,padx=(20,20),pady=(20,20),sticky="nw")
        self.enter = ctk.CTkEntry(self)
        self.enter.grid(row=0,column=1,padx=(20,20),pady=(20,20),sticky="n")
        self.run_but = ctk.CTkButton(self,text="Run Simulation",command=self.run_sim)
        self.run_but.grid(row=1,column=0,padx=20,pady=20)
        self.wins_label = ctk.CTkLabel(self,text="Wins:   ")
        self.wins_label.grid(row=2,column=0,padx=(20,20),pady=(20,20),sticky="n")
        self.loses_label = ctk.CTkLabel(self,text="Losses: ")
        self.loses_label.grid(row=3,column=0,padx=(20,20),pady=(20,20),sticky="n")
            
    def del_player(self,mon):
        self.master.players.remove(mon)
        self.gen_frame()
    def del_monster(self,mon):
        self.master.monsters.remove(mon)
        self.gen_frame()

    def run_sim(self):
        simmy = sim.simulation()
        wins = 0
        losses = 0
        survivals = Counter()
        deaths = Counter()
        alls = []
        for i in self.master.players:
            alls.append(i.name)
        for i in self.master.monsters:
            alls.append(i.name)
        print(alls)
        sim_num = int(self.enter.get())
        total_play = 0
        total_mon = 0
        last_update = time.time()
        simmy.players = copy.deepcopy(self.master.players)
        simmy.monsters = copy.deepcopy(self.master.monsters)
        for i in range(sim_num):
            simmy.players = copy.deepcopy(self.master.players)
            simmy.monsters = copy.deepcopy(self.master.monsters)
            random.shuffle(simmy.players)
            random.shuffle(simmy.monsters)
            #print(list(map(str,sim.players)),list(map(str,sim.monsters)))
            out = simmy.run_sim()
            if len(out[0]) > len(out[1]):
                wins += 1
            else:
                losses += 1
            deaths.update(alls)
            temps = []
            for i in simmy.players:
                temps.append(i.name)
            for i in simmy.monsters:
                temps.append(i.name)
            deaths.subtract(temps)
            survivals.update(temps)
            total_play += out[2]
            total_mon += out[3]
            if time.time() - last_update > 2:
                self.wins_label.configure(text="Wins:   " + str(wins))
                self.loses_label.configure(text="Losses:" + str(losses))
                last_update = time.time()
        self.wins_label.configure(text="Wins:   " + str(wins))
        self.loses_label.configure(text="Losses:" + str(losses))
        print("WINS ",wins,"     LOSSES ",losses)
        print("PLAY ",total_play/sim_num,"      MON ",total_mon/sim_num,"     TOTAL ",(total_play+total_mon)/sim_num)
        print(survivals.most_common())
        print(deaths.most_common())

class main(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.players = []
        self.monsters = []
        self.title("Daggerheart Combat Calc")
        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.char_frame = None
        self.edit_char_button = ctk.CTkButton(self,width=WIDTH/4,height=HEIGHT/10,command=self.character_editor,text="Open Character Editor")
        self.edit_char_button.grid(row=0,column=0,padx=(20,20),pady=(20,20),sticky="n")
        self.gen_sel_frame()
        self.gen_center_frame()
        self.sim_frame = SimFrame(self)
        self.sim_frame.grid(row=1,column=2,padx=(20,20),pady=(20,20),sticky="n")

    def character_editor(self):
        self.edit_win = creature_editor.CharacterApp()
        self.edit_win.mainloop()
        self.edit_win = None
        

    def gen_sel_frame(self):
        self.sel_frame = creature_editor.AvailableMonstersFrame(self,new_buttons=False)
        self.sel_frame.grid(row=1,column=0,padx=(20,10),pady=(20,20),sticky = "nsw")


    def gen_center_frame(self):
        self.cen_frame = ChosenMonstersFrame(self)
        self.cen_frame.grid(row=1,column=1,padx=(10,10),pady=(20,20),sticky = "nsw")

    def load_creature(self,creature,file):
        #fields = list(filter(lambda x: "__" not in x[0] and (type(x[1]) is int or type(x[1]) is str or type(x[1]) is list),inspect.getmembers(creature)))
        #self.char_frame = CharacterInfoFrame(self, fields, creature=creature,write_loc=file)
        #self.char_frame.grid(row=0, column=1, padx=10, pady=(20,20),sticky = "nsw")
        if type(creature) is creatures.player:
            self.players.append(creature)
        elif type(creature) is creatures.monster:
            self.monsters.append(creature)
        self.cen_frame.gen_frame()
        
        

if __name__ == "__main__":
    app = main()
    app.mainloop()