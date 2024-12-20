import random
import itertools
import os
import json

# Specify the directory name
directory_name = "fantasyoldworlddata"

#==================================================================#
# Basic Functions
#==================================================================#
def first_n_digits(num, n):
    num = abs(num)
    num_str = str(num)

    if n >= len(num_str):
        return num

    return int(num_str[:n])

def HumanTalentsGen():                        #Human Random Talents
    talent = random.randint(1, 100)
    if talent < 5:      #Acurate Hearing
        return 1
    elif talent < 10:   #Ambidextrous
        return 1
    elif talent < 14:   #Coolheaded
        return 1
    elif talent < 19:   #Excellent Vision
        return 1
    elif talent < 23:   #Fleet Footed
        return 1
    elif talent < 28:   #Hardy
        return 1
    elif talent < 32:   #Lighting Reflexes
        return 1
    elif talent < 36:   #Luck
        return 1
    elif talent < 41:   #Marksman
        return 1
    elif talent < 45:   #Mimic
        return 1
    elif talent < 50:   #Night Vision
        return 1
    elif talent < 54:   #Resistance to Disease
        return 1
    elif talent < 58:   #Resistance to Magic
        return 1
    elif talent < 62:   #Resistance to Poison
        return 1
    elif talent < 67:   #Savvy
        return 1
    elif talent < 72:   #Sixth Sense
        return 1
    elif talent < 76:   #Strong-Minded
        return 1
    elif talent < 80:   #Sturdy
        return 1
    elif talent < 84:   #Suave
        return 1
    elif talent < 88:   #Super Numerate
        return 1
    elif talent < 92:   #Very Resilient
        return 1
    elif talent < 96:   #Very Strong
        return 1
    else:               #Warrior Born
        return 1
    
def HalflingTalentsGen(talent):                     #Halfling Random Talents (IE: No NightVision)
    talent = random.randint(1, 100)
    if talent < 6:      #Acurate Hearing
        return 1
    elif talent < 11:   #Ambidextrous
        return 1
    elif talent < 16:   #Coolheaded
        return 1
    elif talent < 21:   #Excellent Vision
        return 1
    elif talent < 26:   #Fleet Footed
        return 1
    elif talent < 30:   #Hardy
        return 1
    elif talent < 34:   #Lighting Reflexes
        return 1
    elif talent < 39:   #Luck
        return 1
    elif talent < 43:   #Marksman
        return 1
    elif talent < 48:   #Mimic
        return 1
    elif talent < 52:   #Resistance to Disease
        return 1
    elif talent < 54:   #Resistance to Magic
        return 1
    elif talent < 58:   #Resistance to Poison
        return 1
    elif talent < 63:   #Savvy
        return 1
    elif talent < 68:   #Sixth Sense
        return 1
    elif talent < 73:   #Strong-Minded
        return 1
    elif talent < 78:   #Sturdy
        return 1
    elif talent < 83:   #Suave
        return 1
    elif talent < 88:   #Super Numerate
        return 1
    elif talent < 92:   #Very Resilient
        return 1
    elif talent < 96:   #Very Strong
        return 1
    else:               #Warrior Born
        return 1


#==================================================================#
# Classes and Game World
#==================================================================#

# Career Template. All Career Entries & Exits are foreign keys for the primary key of the career itself.
# All skills and talents target IDs of the skills & talents table.
# Selectable Skills are Talents are built as {{skillID,SkillID},{SkillID,SkillID}}
# It means for the logistical function that a character to be able to advance to another career, must have at least 1 of these skills.
# Some careers maybe have only 1 case of different skills to be picked, others may not have any as NULL.
# Career Complex refers to the Basic & Advanced Careers. This is to make a pool of available careers that are possible to transition by the player
# Career Trappings goes to all relevant equipment.


class Career:
    id_iter = itertools.count()

    def __init__(self,career_complex: int,career_title: str,career_desc: str,career_ws: int ,career_bs: int,career_s: int,career_t: int,
                 career_ag: int,career_int: int,career_wp: int,career_fel: int,career_a: int,career_w: int,career_m: int,career_mag: int,career_entries: set,career_exits: set):
        
        self.career_id = next(self.id_iter)
        self.career_complex = career_complex
        self.career_title = career_title
        self.career_desc = career_desc
        self.career_ws = career_ws
        self.career_bs = career_bs
        self.career_s = career_s
        self.career_t =  career_t
        self.career_ag =  career_ag
        self.career_int = career_int
        self.career_wp = career_wp
        self.career_fel = career_fel
        self.career_a = career_a
        self.career_w = career_w
        self.career_m = career_m
        self.career_mag = career_mag
        self.career_mandatory_skills = {}
        self.career_selectable_skills = {}
        self.career_mandatory_talents = {}
        self.career_selectable_talents = {}
        self.career_trappings = {}
        self.career_entries = career_entries
        self.career_exits = career_exits
    
    def getCareer(self):
        return(self.career_id,self.career_complex,self.career_title,self.career_desc,self.career_ws,self.career_bs,self.career_s,self.career_t,self.career_ag,self.career_int
                ,self.career_wp,self.career_fel,self.career_a,self.career_w,self.career_m,self.career_mag,self.career_mandatory_skills
                ,self.career_mandatory_talents,self.career_selectable_skills,self.career_selectable_talents,self.career_trappings,self.career_entries,self.career_exits)
    
    def printCareer(self):  
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))    

# Equipment it's the general table for all items in the game. 
# An Item Type it's based if it is item (0), melee weapon (1), ranged weapon (2), armour (3). 
# Item Group refers to only weapons groups rules. And it's based on the talent ID with the specialisation of the weapon group.

class Equipment:
    id_iter = itertools.count()
    def __init__(self,item_type: int, item_group: int,item_name: str,item_effect: set,item_damage: int):
        self.item_id = next(self.id_iter)
        self.item_type = item_type
        self.item_group = item_group
        self.item_name = item_name
        self.item_effect = item_effect
        self.item_damage = item_damage

    def getEquipment(self):
        return (self.item_id,self.item_type,self.item_group,self.item_name,self.item_effect,self.item_damage)
    
    def printEquipment(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))    

def getEquipmentPrint(obj):
    print('-----------------------------------------')
    for attribute in ['item_id','item_type','item_group','item_name','item_effect','item_damage']:
        print(attribute+': '+ str(getattr(obj, attribute)))
    print('-----------------------------------------')

# Race Table is only for the purposes of generating a character by the user or system. Each characteristic has a base number that will use the rolling function.
# Race wounds and fate points rolls will be based on the race id, which normally would be as: 1 = human, 2 = dwarf, 3 = halfling, 4 = elf.
# These 2 will be compared in the function. 

class Race:
    id_iter = itertools.count()
    def __init__(self,race_name: str,race_ws: int,race_bs: int,race_s: int,race_t: int,race_ag: int,race_int: int
                 ,race_wp: int,race_fel: int,race_m: int):
        self.race_id = next(self.id_iter)
        self.race_name = race_name
        self.race_ws = race_ws
        self.race_bs = race_bs
        self.race_s = race_s
        self.race_t =  race_t
        self.race_ag =  race_ag
        self.race_int = race_int
        self.race_wp = race_wp
        self.race_fel = race_fel
        self.race_m = race_m
        self.race_skills = []
        self.race_talents = []
    
    def getRace(self):
        return(self.race_id,self.race_name,self.race_ws,self.race_bs,self.race_s,self.race_t,self.race_ag,self.race_int
            ,self.race_wp,self.race_fel,self.race_m,self.race_skills,self.race_talents)
        

    def printRace(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))   
# Skills & Talents. Skills are self-defined by the corebook standard.
# Talents must have an effect attached in the case an actor's characteristic is affected by it.
# Talents' effects may be null or 0 if they are not required to be applied.
# For Skills: Chars
# WS 1, BS 2, S 3, T 4, Ag 5, Int 6, WP 7, Fel 8.
class Skills:
    id_iter = itertools.count()
    def __init__(self,skill_complexity: bool,skill_name: str, skill_desc: str, skill_char: int, skill_altchar: int):
        self.skill_id = next(self.id_iter)
        self.skill_complexity = skill_complexity
        self.skill_name = skill_name
        self.skill_desc = skill_desc
        self.skill_char = skill_char
        self.skill_altchar = skill_altchar

    def getSkill(self):
        return(self.skill_id,self.skill_name,self.skill_desc,self.skill_char,self.skill_altchar)
    
    def printSkill(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))   

class Talents:
    id_iter = itertools.count()
    def __init__(self,talent_name: str,talent_desc: str,effect_id: int):
        self.talent_id = next(self.id_iter)
        self.talent_name = talent_name
        self.talent_desc = talent_desc
        self.effect_id = effect_id
        
    def getTalent(self):
        return(self.talent_id,self.talent_name,self.talent_desc,self.effect_id)
    
    def printTalent(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

# Effects are considered to be Status & Talents Effect. 
# Effect Type: 0 Mechanic Based (Talents), 1 Situational Based (Talents),2 Equipment Based(Weapon Rules) and 3 Status Based (Rules)
class Effect:
    id_iter = itertools.count()
    def __init__(self,effect_desc: str, effect_type: int, effect_value: list, target: int):
        self.effect_id = next(self.id_iter)
        self.effect_desc = effect_desc
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.target = target
        
    def getEffect(self):
        return(self.effect_id,self.type,self.target)
    
    def printEffect(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

# An Actor is a Character that can be managed by a player or by the AI built-in the game.
# Actors can be generated randomly, as well can be made by an user.
class Actor:
    def __init__(self,actor_id: int,race_id: int,actor_name: str,actor_current_career: int,actor_ws: int,actor_bs: int,actor_s: int,actor_t: int,
                 actor_ag: int,actor_int: int,actor_wp: int,actor_fel: int,actor_a: int,actor_w: int,actor_m: int,actor_mag: int,
                 actor_ip: int,actor_fp: int,actor_experience: int,actor_advancements: int):
        self.actor_id = actor_id
        self.race_id = race_id
        self.actor_name = actor_name
        self.actor_current_career = actor_current_career
        self.actor_previous_career = []
        self.actor_ws = actor_ws
        self.actor_bs = actor_bs
        self.actor_s = actor_s
        self.actor_t = actor_t
        self.actor_ag = actor_ag
        self.actor_int = actor_int
        self.actor_wp = actor_wp
        self.actor_fel = actor_fel
        self.actor_a = actor_a
        self.actor_w = actor_w
        self.actor_m = actor_m
        self.actor_mag = actor_mag
        self.actor_ip = actor_ip
        self.actor_fp = actor_fp
        self.actor_skills = []
        self.actor_talents = {}
        self.actor_experience = actor_experience
        self.actor_advancements = actor_advancements
        self.actor_trappings = []
    def getActor(self):
        return(self.actor_id,self.race_id,self.actor_name,self.actor_current_career,self.actor_previous_career,self.actor_ws,self.actor_bs,self.actor_s,self.actor_t
               ,self.actor_ag,self.actor_int,self.actor_wp,self.actor_fel,self.actor_a,self.actor_w,self.actor_m,self.actor_mag,self.actor_ip,self.actor_fp
               ,self.actor_skills,self.actor_talents,self.actor_experience,self.actor_advancements,self.actor_trappings)
    
    def printActor(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    def StatsGeneration(self):
        #Human
        if self.race_id == 1:
            #Stats Bases are 20
            self.actor_ws = 20 + random.randint(2, 20)
            self.actor_bs = 20 + random.randint(2, 20)
            self.actor_s = 20 + random.randint(2, 20)
            self.actor_t = 20 + random.randint(2, 20)
            self.actor_ag = 20 + random.randint(2, 20)
            self.actor_int = 20 + random.randint(2, 20)
            self.actor_wp = 20 + random.randint(2, 20)
            self.actor_fel = 20 + random.randint(2, 20) 
            #Skill List to be made
            self.actor_skills.extend([])
            #Until Here
            check = False
            talent1 = HumanTalentsGen()
            talent2 = HumanTalentsGen()
            ## TO FIX
            #while(check != True):
            #    if(talent1 == 0):
            #        talent1 = HumanTalentsGen()
            #        talent2 = HumanTalentsGen()
            #    if(talent1 != talent2):
            #        check = True
            #    else:
            #        talent2 = HumanTalentsGen()
            #self.actor_talents.update([talent1,talent2])
            #Human Wounds Table
            woundsRoll = random.randint(1,10)
            if woundsRoll < 4:
                self.actor_w = 10
            elif woundsRoll < 7:
                self.actor_w = 11
            elif woundsRoll < 10:
                self.actor_w = 12
            else:
                self.actor_w = 13
            #Human Fate Table
            fateRoll = random.randint(1,10)
            if fateRoll < 5:
                self.actor_fp = 2
            else:
                self.actor_fp = 3
    
        #Dwarf
        elif self.race_id == 2:
            self.actor_ws = 30 + random.randint(2, 20)
            self.actor_bs = 20 + random.randint(2, 20)
            self.actor_s = 20 + random.randint(2, 20)
            self.actor_t = 30 + random.randint(2, 20)
            self.actor_ag = 10 + random.randint(2, 20)
            self.actor_int = 20 + random.randint(2, 20)
            self.actor_wp = 20 + random.randint(2, 20)
            self.actor_fel = 10 + random.randint(2, 20)
            #Skill List to be made
            self.actor_skills.extend([])
            #Talent List to be made
            #self.actor_talents.update([])
            #Dwarf Wounds Table
            woundsRoll = random.randint(1,10)
            if woundsRoll < 4:
                self.actor_w = 11
            elif woundsRoll < 7:
                self.actor_w = 12
            elif woundsRoll < 10:
                self.actor_w = 13
            else:
                self.actor_w = 14
            #Dwarf Fate Table
            fateRoll = random.randint(1,10)
            if fateRoll < 5:
                self.actor_fp = 1
            elif fateRoll < 8:
                self.actor_fp = 2
            else:
                self.actor_fp = 3
            
            print(1)
        #Halfling
        elif self.race_id == 3:
            self.actor_ws = 10 + random.randint(2, 20)
            self.actor_bs = 30 + random.randint(2, 20)
            self.actor_s = 10 + random.randint(2, 20)
            self.actor_t = 10 + random.randint(2, 20)
            self.actor_ag = 30 + random.randint(2, 20)
            self.actor_int = 20 + random.randint(2, 20)
            self.actor_wp = 20 + random.randint(2, 20)
            self.actor_fel = 30 + random.randint(2, 20)
            #Skill List to be made
            self.actor_skills.extend([])
            #Talent List to be made
            #self.actor_talents.update([HalflingTalentsGen()])
            #Halfling Wounds Table
            woundsRoll = random.randint(1,10)
            if woundsRoll < 4:
                self.actor_w = 8
            elif woundsRoll < 7:
                self.actor_w = 9
            elif woundsRoll < 10:
                self.actor_w = 10
            else:
                self.actor_w = 11
            #Halfling Fate Table
            fateRoll = random.randint(1,10)
            if fateRoll < 8:
                self.actor_fp = 2
            else:
                self.actor_fp = 3
        #Elf
        else:
            self.actor_ws = 20 + random.randint(2, 20)
            self.actor_bs = 30 + random.randint(2, 20)
            self.actor_s = 20 + random.randint(2, 20)
            self.actor_t = 20 + random.randint(2, 20)
            self.actor_ag = 30 + random.randint(2, 20)
            self.actor_int = 20 + random.randint(2, 20)
            self.actor_wp = 20 + random.randint(2, 20)
            self.actor_fel = 20 + random.randint(2, 20)
            #Skill List to be made
            self.actor_skills.extend([])
            #Talent List to be made
            #self.actor_talents.update([])
            #Elf Wounds Table
            woundsRoll = random.randint(1,10)
            if woundsRoll < 4:
                self.actor_w = 9
            elif woundsRoll < 7:
                self.actor_w = 10
            elif woundsRoll < 10:
                self.actor_w = 11
            else:
                self.actor_w = 12
            #Elf Fate Table
            fateRoll = random.randint(1,10)
            if fateRoll < 5:
                self.actor_fp = 1
            else:
                self.actor_fp = 2
            print(1)

def accumulateSkills(obj):
    SkillDict = {}
    for i in obj["actor_skills"]:
        if obj["actor_skills"].count(i) >  3:
            SkillDict.update({i:3})
        else:
            SkillDict.update({i:obj["actor_skills"].count(i)})
    return SkillDict


# Memory is part of an Actor actual progress of advancements. This will check if someone is able to advance
# If only the career's table allows it by comparing values.
class ActorMemory:
    def __init__(self,actor_id: int,memory_ws: int,memory_bs: int,memory_s: int,memory_t: int,memory_ag: int,memory_int: int,memory_wp: int,memory_fel: int
                 ,memory_a: int,memory_w: int,memory_m: int,memory_mag: int):
        self.actor_id = actor_id
        self.memory_ws = memory_ws
        self.memory_bs = memory_bs
        self.memory_s = memory_s
        self.memory_t = memory_t
        self.memory_ag = memory_ag
        self.memory_int = memory_int
        self.memory_wp = memory_wp
        self.memory_fel = memory_fel
        self.memory_a = memory_a
        self.memory_w = memory_w
        self.memory_m = memory_m
        self.memory_mag = memory_mag
    def getActorMemor(self):
        return(self.actor_id,self.memory_ws,self.memory_bs,self.memory_s,self.memory_t,self.memory_ag,self.memory_int,self.memory_wp,self.memory_fel,self.memory_a
               ,self.memory_w,self.memory_m,self.memory_mag)
    
    def printActorMemor(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

# Similar to the Memory above, however, it nests skill ranks in the case it can progress in the next career.
# If a current career the user has the option to upgrade a skill, then it must be nested as {skillID, skillRank}
# Skill rank are as follow. 0 = Not Learned, 1 = Learned, 2 = actor characteristic + 10, 3 = actor's characteristic + 20.
# Any futher value if a new career can be applied above 3, will be considered already "mastered" by standard Corebook.
class ActorMemorySkillsTalents:
    def __init__(self,actor_id: int):
        self.actor_id = actor_id
        self.memory_skills = {}
        self.memory_talents = {}
    def getActorMemSkillTalent(self):
        return(self.actor_id,self.memory_skills,self.memory_talents)

    def printActorMemSkillTalent(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

# Users Tables and Classes. Each Instance of a profile may be able to create one singular actor until they must replace it by the occurance of playing and meeting
# Certain game overs screens.
class UserProfile:
    def __init__(self,user_id: int,username: str):
        self.user_id = user_id
        self.username = username
    def getUser(self):
        return(self.user_id,self.username)

    def printUser(self):
        attrs = vars(self)
        print(', '.join("%s: %s" % item for item in attrs.items()))

def gameInitDemoPlayer():
    Player = Actor(0,1,"Pright","",0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0)
    Player.StatsGeneration()
    return (Player)

def gameInitDemoActors():
    Player = Actor(1,1,"DemoActor","",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    Player.StatsGeneration()
    return (Player)

# For Skills: Chars
# WS 1, BS 2, S 3, T 4, Ag 5, Int 6, WP 7, Fel 8.
# If 0, it means that it's null/non-required
def gameInitSkills():
    SkillsList = []

    SkillsList.append(Skills(True,"Academic Knowledge(Religion)","Academic Knowledge represents a depth of learning far beyond common knowledge and requires extensive study.",6,0))
    SkillsList.append(Skills(False,"Animal Care","Use this skill to take care of farm and domestic animals.",6,0))
    SkillsList.append(Skills(True,"Animal Training","Use this skill to train animals to perform tricks and simple commands.",8,0))
    SkillsList.append(Skills(True,"Blather","Use this skill to stall for time by running off at the mouth.",8,0))
    SkillsList.append(Skills(True,"Channelling","Use this skill to control the Winds of Magic.",7,0))
    SkillsList.append(Skills(False,"Charm","Use this skill to manipulate others. You can affect one person for each 10 points of fellowship",8,0))
    SkillsList.append(Skills(False,"Concealment","Use this skill to hide from unfriendly eyes.",5,0))
    SkillsList.append(Skills(True,"Dodge Blow","Use this skill to avoid attacks in melee combat.",5,0))
    SkillsList.append(Skills(True,"Heal","Use this skill to provide medical attention to the wounded. A succesful heal test restores 1d10 wounds on a lightly wounded character, and 1 wound on a heavily wounded.",6,0))
    SkillsList.append(Skills(False,"Intimidate","Use this skill to coerce or frighten others.",3,0))

    return(SkillsList)

def gameInitEffect():
    EffectsList = []

    EffectsList.append(Effect("AcuteHearing",1,20,[0]))
    EffectsList.append(Effect("AlleyCat",1,10,[0]))
    EffectsList.append(Effect("Ambidextrous",0,0,[0]))

    return(EffectsList)

def gameInitTalents():
    TalentsDict = []

    TalentsDict.append(Talents("Acute Hearing","Your hearing is exceptionally good. You gain a +20 percent bonus on Perception Skill Tests that involve listening.",0))
    TalentsDict.append(Talents("Alley Cat","You are at home on the streets. You gain a +10 percent bonus on Concealment and Silent Moves tests when in urban location",1))
    TalentsDict.append(Talents("Ambidextrous","You can use either hand equally well. You do not suffer the normal -20 percent WS or BS penalty when using a weapon in your secondary hand.",2))
    
    return(TalentsDict)
    
def gameInitWeapons():
    WeaponsList = []

    WeaponsList.append(Equipment(1,"Buckler",{},0,-4))
    WeaponsList.append(Equipment(1,"Dagger",{},0,-3))
    return(WeaponsList)

def gameInitCareer():
    #Lists
    CareerList = []
    #Careers Initialization (By Alphabet, starting id from 0)
    #List to store values and export them later
    CareerList.append(Career(0,"Agitator","Agitators organize on behalf of various causes, handing out leaflets, giving rousing speeches, and stirring up the populace."
                             ,5,5,0,0,5,10,0,10,0,2,0,0,[],[]))
    
    CareerList.append(Career(0
                             ,"Apprentice Wizard","Humans born with magical talent are dangerous and feared individuals. Daemons and disaster gather about an untrained Wizard. To deal with this threat the Empire sends such people away to join one of the eight Orders of Wizardry. During their apprenticeship young Wizards learn how to practice magic safely, and contemplate which Order they will eventually join."
                            ,0,0,0,0,5,10,15,5,0,2,0,1,[],[]))
    
   
    CareerList.append(Career(0,"Bailiff","Bailiffs are manorial officials in the service of Noble Lords.",5,5,5,0,0,10,5,10,0,2,0,0,[],[]))
    
    CareerList.append(Career(0,"Bodyguard","The rich and powerful use Bodyguards to protect themselves from thieves and common riffraff.",10,0,5,5,5,0,0,10,0,2,0,0,[],[]))
    
    CareerList.append(Career(0,"Initiate","Religion has taken second place to Main Profile many young men and women willing to devote their lives to the Secondary Profile Gods."
                             ,5,5,0,5,0,10,10,10,0,2,0,0,[],[]))
    
    return(CareerList)



def gameInitSequence():
    # Create the directory
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Specify the nested directory structure
    nested_directory = ["/actors","/actors/memory","/actors/career","/skills","/talents","/armoury",
                        "/armoury/weapons","/armoury/weapons/ranged","/armoury/weapons/melee","/armoury/armour","/armoury/items"
                        ,"/player","/player/actor","/player/actor/memory","/player/equipment","/player/equipment/melee","/player/equipment/ranged","/player/equipment/item"]
    
    for each in nested_directory:
        # Create nested directories
        try:
            os.makedirs(directory_name+each)
            print(f"Nested directories '{directory_name+each}' created successfully.")
        except FileExistsError:
            print(f"One or more directories in '{directory_name+each}' already exist.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name+each}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Game Files Allocated")

def getCareerDictionary():
    Dict = {}
    Data = gameInitCareer()
    for i in Data:
        temp = i.__dict__
        id = temp["career_id"]
        del temp["career_id"]
        #print(id)
        #print(temp)
        Dict[id] = temp
    return Dict

def getWeaponDictionary():
    Dict = {}
    Data = gameInitWeapons()
    for i in Data:
        temp = i.__dict__
        id = temp["item_id"]
        del temp["item_id"]
        #print(id)
        #print(temp)
        Dict[id] = temp
    return Dict

def getTalentDictionary():
    Dict = {}
    Data = gameInitTalents()
    for i in Data:
        temp = i.__dict__
        id = temp["talent_id"]
        del temp["talent_id"]
        #print(id)
        #print(temp)
        Dict[id] = temp
    return Dict

def getEffectDictionary():
    Dict = {}
    Data = gameInitEffect()
    for i in Data:
        temp = i.__dict__
        id = temp["effect_id"]
        del temp["effect_id"]
        #print(id)
        #print(temp)
        Dict[id] = temp
    return Dict

def getSkillDictionary():
    Dict = {}
    Data = gameInitSkills()
    for i in Data:
        temp = i.__dict__
        id = temp["skill_id"]
        del temp["skill_id"]
        #print(id)
        #print(temp)
        Dict[id] = temp
    return Dict

#print(getCareerDictionary())
#print(getWeaponDictionary())
#print(getTalentDictionary())
#print(getEffectDictionary())
#print(getSkillDictionary())

#with open("fantasyoldworlddata/actors/career/Careers.json", "w+") as f:
#    json.dump(Dictionary, f)
