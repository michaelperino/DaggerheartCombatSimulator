import creatures

p = creatures.player()
p.name = "Marlowe"
p.evasion = 9
p.armor_amt = 5
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [3,8,13]
p.damage_dice = [8]
p.damage_add = 2
p.att_bonus = 2

p.save()

p = creatures.player()
p.name = "El Jefe"
p.evasion = 13
p.armor_amt = 3
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [4,9,14]
p.damage_dice = [8]
p.damage_add = 2
p.att_bonus = 2

p.save()

p = creatures.player()
p.name = "Brev"
p.evasion = 7
p.armor_amt = 9
p.armor_pts = 3
p.hitpoints = 6
p.damage_lim = [3,8,13]
p.damage_dice = [8]
p.damage_add = 0
p.att_bonus = 2

p.save()

p = creatures.monster()
p.name = "Thistlefolk Ambusher"
p.hitpoints = 3
p.evasion = 13
p.damage_lim = [1,6,10]
p.damage_dice = [8,8]
p.damage_add = 1
p.att_bonus = 1

p.save()

p = creatures.monster()
p.name = "Thistlefolk Thief"
p.hitpoints = 3
p.evasion = 14
p.damage_lim = [1,10,15]
p.damage_dice = [6,6,6]
p.damage_add = 0
p.att_bonus = 1

p.save()