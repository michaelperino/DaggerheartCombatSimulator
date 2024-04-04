import os
import pickle
import random


class player:
    def __init__(self):
        self.name = None
        self.hitpoints = 0
        self.evasion = 0
        self.damage_lim = [0,0,0]
        self.armor_amt = 0
        self.armor_pts = 0
        self.stress = 0
        self.hope = 2
        self.damage_dice = []
        self.damage_add = 0
        self.att_bonus = 0
        self.AOE = 0
        self.AOE_Mult = 1

    def attack(self):
        hope = random.randint(1,12)
        fear = random.randint(1,12)
        damage = 0
        if hope == fear:
            hope = 60
            for i in self.damage_dice:
                damage += i
            self.hope = min(5,self.hope+1)
            self.stress = max(0,self.stress - 1)
        for i in self.damage_dice:
            damage += random.randint(1,i)
        damage += self.damage_add
        return(hope>fear,hope+fear+self.att_bonus,damage)
    
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
        self.damage_dice =loady.damage_dice 
        self.damage_add =loady.damage_add 
        self.att_bonus =loady.att_bonus 
        self.AOE =loady.AOE 
        self.AOE_Mult =loady.AOE_Mult 

        

class monster:
    def __init__(self):
        self.name = None
        self.hitpoints = 0
        self.evasion = 0
        self.damage_lim = [0,0,0]
        self.stress = 0
        self.damage_dice = []
        self.damage_add = 0
        self.att_bonus = 0
        self.AOE = 0
        self.AOE_Mult = 1

    def attack(self):
        roll = random.randint(1,20)
        crit = 0
        if roll == 20:
            crit = 1
        roll += self.att_bonus
        damage = self.damage_add
        for i in self.damage_dice:
            damage += i * crit + random.randint(1,i)
        return (True if crit else False,roll,damage)
    
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
        self.damage_dice =loady.damage_dice 
        self.damage_add =loady.damage_add 
        self.att_bonus =loady.att_bonus 
        self.AOE =loady.AOE 
        self.AOE_Mult =loady.AOE_Mult 