import copy
import os
import pickle
import random

class attack:
    def __init__(self):
        self.prio = 0
        self.damage_dice = []
        self.damage_add = 0
        self.att_bonus = 0
        self.AOE = 0
        self.AOE_Mult = 1
        self.hope_cost = 0
        self.stress_cost = 0

    def __str__(self):
        return "prio"+str(self.prio)+" dice"+str(self.damage_dice)+" aoe"+str(self.AOE)

class player:
    def __init__(self):
        self.name = ""
        self.hitpoints = 0
        self.evasion = 0
        self.damage_lim = [0,0,0]
        self.armor_amt = 0
        self.armor_pts = 0
        self.stress = 0
        self.hope = 2
        self.attacks = []
        #self.damage_dice = []
        #self.damage_add = 0
        #self.att_bonus = 0
        #self.AOE = 0
        #self.AOE_Mult = 1

    def attack(self):
        for i in self.attacks:
            if i.hope_cost <= self.hope:
                att = i
                break
        hope = random.randint(1,12)
        fear = random.randint(1,12)
        damage = 0
        if hope == fear:
            hope = 60
            for i in att.damage_dice:
                damage += i
            self.hope = min(5,self.hope+1)
            self.stress = max(0,self.stress - 1)
        for i in att.damage_dice:
            damage += random.randint(1,i)
        damage += att.damage_add
        if hope > fear:
            self.hope = min(5,self.hope+1)
        return(hope>fear,hope+fear+att.att_bonus,damage,att.AOE,att.AOE_Mult)
    
    def calc_damage(self, damage):
        for i in range(0,3):
            if damage < self.damage_lim[i]:
                return(i)
        return(3)

    def defend(self, att_roll, damage):
        if att_roll >= self.evasion:
            hit = self.calc_damage(damage=damage)
            hit2 = self.calc_damage(damage=(damage - self.armor_amt))
            if hit2 < hit and self.armor_pts > 0:
                hit = hit2
                self.armor_pts -= 1
            self.hitpoints -= hit
            return(True, hit)
        return(False, 0)

    def __str__(self):
        return " ".join(map(str,[self.name,self.hitpoints,self.armor_pts,self.hope]))
    
    def save(self,filename=None,folderpath="./players/"):
        if not filename:
            filename = self.name
        with open(folderpath+filename,'wb') as f:
            pickle.dump(self,f)

    def load(self,filename=None,folderpath="./players/"):
        if not filename:
            filename = self.name
        if os.path.exists(folderpath+filename):
            with open(folderpath+filename,'rb') as f:
                loady = pickle.load(f)
            self.name =loady.name 
            self.hitpoints =loady.hitpoints 
            self.evasion =loady.evasion 
            self.damage_lim =loady.damage_lim 
            self.armor_amt =loady.armor_amt 
            self.armor_pts =loady.armor_pts 
            self.stress =loady.stress 
            self.hope =loady.hope 
            for i in range(len(loady.attacks)):
                self.attacks.append(copy.deepcopy(loady.attacks[i]))
            self.attacks.sort(key=lambda x:x.prio,reverse=True)

        

class monster:
    def __init__(self):
        self.name = ""
        self.hitpoints = 0
        self.evasion = 0
        self.damage_lim = [0,0,0]
        self.stress = 0
        #self.damage_dice = []
        #self.damage_add = 0
        #self.att_bonus = 0
        #self.AOE = 0
        #self.AOE_Mult = 1
        self.attacks = []

    def attack(self,fear):
        for i in self.attacks:
            if i.hope_cost <= fear:
                att = i
                fear_change = i.hope_cost
                break
        roll = random.randint(1,20)
        crit = 0
        if roll == 20:
            #crit = 1
            crit = 0
        roll += att.att_bonus
        damage = att.damage_add
        for i in att.damage_dice:
            damage += i * crit + random.randint(1,i)
        return (True if crit else False,roll,damage,att.AOE,att.AOE_Mult,fear_change)
    
    def calc_damage(self, damage):
        for i in range(0,3):
            if damage < self.damage_lim[i]:
                return(i)
        return(3)

    def defend(self, att_roll, damage):
        if att_roll >= self.evasion:
            hit = self.calc_damage(damage=damage)
            self.hitpoints -= hit
            return (True, hit)
        return (False, 0)

    def __str__(self):
        return " ".join(map(str,[self.name,self.hitpoints]))
    
    def save(self,filename=None,folderpath="./monsters/"):
        if not filename:
            filename = self.name
        with open(folderpath+filename,'wb') as f:
            pickle.dump(self,f)

    def load(self,filename=None,folderpath="./monsters/"):
        if not filename:
            filename = self.name
        if os.path.exists(folderpath+filename):
            with open(folderpath+filename,'rb') as f:
                loady = pickle.load(f)
            self.name =loady.name 
            self.hitpoints =loady.hitpoints 
            self.evasion =loady.evasion 
            self.damage_lim =loady.damage_lim 
            self.stress =loady.stress 
            for i in range(len(loady.attacks)):
                self.attacks.append(copy.deepcopy(loady.attacks[i]))
            self.attacks.sort(key=lambda x:x.prio,reverse=True)