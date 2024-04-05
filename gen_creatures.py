import inspect
import creatures

p = creatures.player()
p.name = "Marlowe"
p.evasion = 9
p.armor_amt = 5
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [3,8,13]
a = creatures.attack()
a.damage_dice = [8]
a.damage_add = 2
a.att_bonus = 2
a.prio = 0
p.attacks.append(a)
a = creatures.attack()
a.prio = 1
a.hope_cost = 2
a.AOE = 2
a.AOE_Mult = 1
a.damage_dice = [10]
a.damage_add = 0
p.attacks.append(a)
p.save()

p = creatures.player()
p.name = "El Jefe"
p.evasion = 13
p.armor_amt = 3
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [4,9,14]
a = creatures.attack()
a.damage_dice = [8]
a.damage_add = 2
a.att_bonus = 2
a.prio = 0
p.attacks.append(a)

p.save()

p = creatures.player()
p.name = "Brev"
p.evasion = 7
p.armor_amt = 9
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [3,8,13]
a = creatures.attack()
a.damage_dice = [8]
a.damage_add = 0
a.att_bonus = 2
p.attacks.append(a)

p.save()

p = creatures.monster()
p.name = "Thistlefolk Ambusher"
p.hitpoints = 3
p.evasion = 13
p.damage_lim = [1,6,10]
a = creatures.attack()
a.damage_dice = [8,8]
a.damage_add = 1
a.att_bonus = 1
p.attacks.append(a)

p.save()

p = creatures.monster()
p.name = "Thistlefolk Thief"
p.hitpoints = 3
p.evasion = 14
p.damage_lim = [1,10,15]
a = creatures.attack()
a.damage_dice = [6,6,6]
a.damage_add = 0
a.att_bonus = 3
p.attacks.append(a)
a = creatures.attack()
a.damage_dice = [8,8]
a.damage_add = 0
a.att_bonus = 3
a.prio = 1
p.attacks.append(a)


p.save()