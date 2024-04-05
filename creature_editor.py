import customtkinter as ctk
import inspect
import creatures
import re
import glob

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
PLAYER_DIR = "players/*"
MON_DIR = "monsters/*"
WIDTH,HEIGHT = (1200,1000)

class CharacterInfoFrame(ctk.CTkFrame):
    def int_callback(self, inp : str):
        if inp.isdigit() or inp == "":
            return True
        return False
    def list_callback(self, inp : str):
        #for i in inp:
            #if not(i.isdigit() or i in ["",",","[","]"," "]):
            #    return False
        return self.list_match.match(inp) is not None
    
    def gen_attack_listing(self):
        self.att_scroll = None
        self.att_scroll = ctk.CTkScrollableFrame(self.att_frame,label_text="Saved Attacks",height=150,width=WIDTH/4)
        self.att_scroll.grid(row =1, column=0, padx = 10,pady=(10,10),sticky = "n")
        self.att_buttons = []
        for i,val in enumerate(self.creature.attacks):
            self.att_buttons.append(ctk.CTkButton(self.att_scroll,text=val, command = lambda m=val:self.load_att(m),width=WIDTH/5))
            self.att_buttons[-1].grid(row=i,column=0,padx=10,pady=(10,0),sticky="w")

    def __init__(self, master, fields, creature, write_loc):
        self.creature = creature
        self.write_loc = write_loc
        super().__init__(master)
        self.master = master
        self.list_match = re.compile("^\[([0-9\,\ ])+\]$")
        self.ic = self.register(self.int_callback)
        self.lc = self.register(self.list_callback)
        self.att = None
        self.creature_frame = ctk.CTkFrame(self)
        self.creature_frame.grid(row=1,column=0,sticky="nw")
        self.save_button = ctk.CTkButton(self.creature_frame,text="Save Player", command = self.save_player,width=WIDTH/5)
        self.save_button.grid(row=0,column=0,padx=10,pady=(10,0),sticky="w")
        self.fields = []
        for count,i in enumerate(fields):
            if i[0] != "attacks":
                r,c=(count+1,0)
                self.fields.append(ctk.CTkLabel(self.creature_frame,text=i[0]))
                self.fields[-1].grid(row=r,column=c,padx=10,pady=(10,0),sticky="w")
                r,c=(count+1,1)
                self.fields.append(ctk.CTkEntry(self.creature_frame,width=WIDTH/6,height=50))
                self.fields[-1].grid(row=r,column=c,padx=10,pady=(10,0),sticky="w")
                if type(i[1]) is list:
                    if len(i[1]) == 0:
                        self.fields[-1].insert(0,"[ ]")
                    self.fields[-1].configure(validate="key",validatecommand=(self.lc,"%P"))
                if type(i[1]) is int:
                    self.fields[-1].configure(validate="key",validatecommand=(self.ic,"%P"))
                print(str(i[1]))
                self.fields[-1].insert(0,str(i[1]))
                count += 1
        self.att_frame = ctk.CTkFrame(self)
        self.att_frame.grid(row=1,column=1,padx=10,pady=(10,10),sticky="nw")
        self.new_a_button = ctk.CTkButton(self.att_frame,text="New Attack", command = self.new_att,width=WIDTH/8)
        self.new_a_button.grid(row = 0, column = 0, padx=10,pady=(10,0),sticky="n")
        self.new_a_button = ctk.CTkButton(self.att_frame,text="Save Attack", command = self.save_att,width=WIDTH/8)
        self.new_a_button.grid(row = 2, column = 0, padx=10,pady=(10,0),sticky="n")
        self.new_a_button = ctk.CTkButton(self.att_frame,text="Delete Attack", command = self.del_att,width=WIDTH/8)
        self.new_a_button.grid(row = 3, column = 0, padx=10,pady=(10,0),sticky="n")
        self.gen_attack_listing()
        
    def save_player(self):
        for i in range(0,len(self.fields),2):
            print(self.fields[i].cget("text"))
            print(self.fields[i+1].get())
            prev = self.creature.__getattribute__(self.fields[i].cget("text"))
            if type(prev) is int:
                self.creature.__setattr__(self.fields[i].cget("text"),int(self.fields[i+1].get()))
            elif type(prev) is list:
                listy = map(self.cust_int,self.fields[i+1].get()[1:-1].split(","))
                print(listy)
                self.creature.__setattr__(self.fields[i].cget("text"),list(listy))
            else:
                self.creature.__setattr__(self.fields[i].cget("text"),self.fields[i+1].get())
        self.creature.save()
        self.master.gen_sel_frame()
    
    def new_att(self):
        self.att = creatures.attack()
        self.creature.attacks.append(self.att)
        self.disp_att()

    def del_att(self):
        if self.att:
            self.creature.attacks.remove(self.att)
            self.gen_attack_listing()
            self.att = None

    def cust_int(self, val):
        try:
            return int(val)
        except:
            return 0
        
    def save_att(self):
        for i in range(0,len(self.attfields),2):
            print(self.attfields[i].cget("text"))
            print(self.attfields[i+1].get())
            prev = self.att.__getattribute__(self.attfields[i].cget("text"))
            if type(prev) is int:
                self.att.__setattr__(self.attfields[i].cget("text"),int(self.attfields[i+1].get()))
            elif type(prev) is list:
                listy = map(self.cust_int,self.attfields[i+1].get()[1:-1].split(","))
                print(listy)
                self.att.__setattr__(self.attfields[i].cget("text"),list(listy))
            else:
                self.att.__setattr__(self.attfields[i].cget("text"),self.attfields[i+1].get())
        print(self.att)
        self.gen_attack_listing()

    def load_att(self,att):
        self.att = att
        self.disp_att()

    def disp_att(self):
        fields = list(filter(lambda x: "__" not in x[0] and (type(x[1]) is int or type(x[1]) is str or type(x[1]) is list),inspect.getmembers(self.att)))
        self.attd_frame = ctk.CTkFrame(self.att_frame)
        self.attd_frame.grid(row=4,column=0,padx=10,pady=(10,10),sticky="w")
        self.attfields = []
        for count,i in enumerate(fields):
            if i[0] != "attacks":
                r,c=(count,0)
                self.attfields.append(ctk.CTkLabel(self.attd_frame,text=i[0]))
                self.attfields[-1].grid(row=r,column=c,padx=10,pady=(10,0),sticky="w")
                r,c=(count,1)
                self.attfields.append(ctk.CTkEntry(self.attd_frame,width=WIDTH/6,height=50))
                self.attfields[-1].grid(row=r,column=c,padx=10,pady=(10,0),sticky="w")
                if type(i[1]) is list:
                    if len(i[1]) == 0:
                        self.attfields[-1].insert(0,"[ ]")
                    self.attfields[-1].configure(validate="key",validatecommand=(self.lc,"%P"))
                if type(i[1]) is int:
                    self.attfields[-1].configure(validate="key",validatecommand=(self.ic,"%P"))
                print(str(i[1]))
                self.attfields[-1].insert(0,str(i[1]))
                count += 1
   

class AvailableMonstersFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        new_p_button = ctk.CTkButton(self,text="New Player", command = self.new_player,width=WIDTH/4.5)
        new_p_button.grid(row = 0, column = 1, padx=10,pady=(10,0),sticky="n")
        player_scroll = ctk.CTkScrollableFrame(self,label_text="Saved Players",height=150,width=WIDTH/4)
        player_scroll.grid(row =1, column=1, padx = 10,pady=(10,10),sticky = "n")
        play_buttons = []
        for i,val in enumerate(glob.glob(PLAYER_DIR)):
            play_buttons.append(ctk.CTkButton(player_scroll,text=val, command = lambda m=val:self.load_player(m),width=WIDTH/5))
            play_buttons[-1].grid(row=i,column=0,padx=10,pady=(10,0),sticky="w")
        new_m_button = ctk.CTkButton(self,text="New Monster", command = self.new_monster,width=WIDTH/4.5)
        new_m_button.grid(row = 2, column = 1, padx=10,pady=(10,0),sticky="n")
        mon_scroll = ctk.CTkScrollableFrame(self,label_text="Saved Monsters",height=150,width=WIDTH/4)
        mon_scroll.grid(row =3, column=1, padx = 10,pady=(10,10),sticky = "n")
        mon_buttons = []
        for i,val in enumerate(glob.glob(MON_DIR)):
            mon_buttons.append(ctk.CTkButton(mon_scroll,text=val, command = lambda m=val:self.load_monster(m),width=WIDTH/5))
            mon_buttons[-1].grid(row=i,column=0,padx=10,pady=(10,0),sticky="w")
            
    def load_player(self,file):
        print("LOAD ",file)
        pl = creatures.player()
        pl.load(file,"")
        self.master.load_creature(pl,file)
    def load_monster(self,file):
        print("LOAD ",file)
        mo = creatures.monster()
        mo.load(file,"")
        self.master.load_creature(mo,file)
    def new_player(self):
        self.load_player(None)
    def new_monster(self):
        self.load_monster(None)

class CharacterApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Character Editor")
        self.geometry(str(WIDTH)+"x"+str(HEIGHT))
        self.gen_sel_frame()
        self.char_frame = None

    def gen_sel_frame(self):
        self.sel_frame = AvailableMonstersFrame(self)
        self.sel_frame.grid(row=0,column=0,padx=(20,10),pady=(20,20),sticky = "nsw")
        
    def load_creature(self,creature,file):
        fields = list(filter(lambda x: "__" not in x[0] and (type(x[1]) is int or type(x[1]) is str or type(x[1]) is list),inspect.getmembers(creature)))
        self.char_frame = CharacterInfoFrame(self, fields, creature=creature,write_loc=file)
        self.char_frame.grid(row=0, column=1, padx=10, pady=(20,20),sticky = "nsw")


    
        

if __name__ == "__main__":
    app = CharacterApp()
    app.mainloop()