# Daggerheart Combat Simulator

I wanted a quick calculator to gauge the difficulty of various combat encounters and ended up with this. Please visit Daggerheart at https://www.daggerheart.com/ and playtest today!

## Installation

Clone the repository and run with Python 3. 

I've tested on Python 3.11 on Windows 10, only external package needed should be customtkinter

## Usage

Run `python3 DaggerheartCombatSim.py` to start the program. Making a player should be straightforward, stress is currently inoperable though. Simply put in the stats from your character sheet into the corresponding lines on the character creator. Armor_amt is the amount that is subtracted from your damage when using an armor_pt. Also, hit points are a positive number that is subtracted from (most players will start with 6). damage_lim is simply the minor->major->severe scale comma delimited. I've included the characters from the quick start module for comparison with their player sheets.

For attacks, they are sorted so that higher priority # attacks are attempted first. The hope_cost field is implemented for players and monsters, the hope_cost field is actually fear cost on monsters. The AOE number is the amount of creatures hit past the first. For example, if you estimate that in combat, there will be 2 creatures within very close range for an AOE attack that does the same damage to both creatures, you'd put "AOE 1" and "AOE_Mult 1". Unfortunately, AOE_Mult needs to be repaired to allow floating point values as the current method of only accepting integers isn't ideal... I'd recommend taking a look at Marlowe for how I attempted to implement her AOE Gilgamesh attack.

One current issue is that I didn't track damage types which would be necessary to accurately simulate the Forest Wraith fight. You could go ahead and copy your physical damage dealers to versions with 50% damage if you want to attempt that fight though.

I haven't implemented healing spells yet.

## Contributing

Pull requests are welcome, especially if you see a spot where my analysis is incorrect (I've only played one combat session and I can't guarantee we played correctly...)
I'd like to not bog down the program with every feature under the sun though. 

For an example on adding custom fields to characters, I did create the \_\_notgoodenough__ field purely for testing its effectiveness on Garrick (it's not super effective by the way).