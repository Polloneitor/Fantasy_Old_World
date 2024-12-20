from flask_restplus import Resource, fields, marshal_with
import json
import random
from schema import Schema, And, Use, Optional, SchemaError

class GameSchema(Schema):
    pass

class EmptySchema(GameSchema):
    pass


#==================================================================#
# Classes and Game World
#==================================================================#

# Career Template. All Career Entries & Exits are foreign keys for the primary key of the career itself.
# All skills and talents target IDs of the skills & talents table.
# Selectable Skills are Talents are built as {{skillID,SkillID},{SkillID,SkillID}}
# It means for the logistical function that a character to be able to advance to another career, must have at least 1 of these skills.
# Some careers maybe have only 1 case of different skills to be picked, others may not have any as NULL.
class CareerSchema(GameSchema):
    career_id = fields.Integer(required= True),
    career_title = fields.String(required= True),
    career_desc = fields.String,
    career_ws = fields.Integer(required= True),
    career_bs = fields.Integer(required= True),
    career_s = fields.Integer(required= True),
    career_t =  fields.Integer(required= True),
    career_ag =  fields.Integer(required= True),
    career_int = fields.Integer(required= True),
    career_wp = fields.Integer(required= True),
    career_fel = fields.Integer(required= True),
    career_a = fields.Integer(required= True),
    career_w = fields.Integer(required= True),
    career_m = fields.Integer(required= True),
    career_mag = fields.Integer(required= True),
    career_mandatory_skills = fields.List(fields.Integer(required= True)),
    career_selectable_skills = fields.List(fields.Integer),
    career_mandatory_talents = fields.List(fields.Integer(required= True)),
    career_selectable_talents = fields.List(fields.List(fields.Integer)),
    career_entries = fields.List(fields.Integer),
    career_exits = fields.List(fields.Integer)

# Race Table is only for the purposes of generating a character by the user or system. Each characteristic has a base number that will use the rolling function.
# Race wounds and fate points rolls will be based on the race id, which normally would be as: 1 = human, 2 = dwarf, 3 = halfling, 4 = elf.
# These 2 will be compared in the function. 

class RaceSchema(GameSchema):
    race_id = fields.Integer(required= True),
    race_name = fields.String(required= True),
    race_ws = fields.Integer(required= True),
    race_bs = fields.Integer(required= True),
    race_s = fields.Integer(required= True),
    race_t =  fields.Integer(required= True),
    race_ag =  fields.Integer(required= True),
    race_int = fields.Integer(required= True),
    race_wp = fields.Integer(required= True),
    race_fel = fields.Integer(required= True),
    race_m = fields.Integer(required= True),
    race_skills = fields.List(fields.Integer(required= True)),
    race_talents = fields.List(fields.Integer(required= True))

# Skills & Talents. Skills are self-defined by the corebook standard.
# Talents must have an effect attached in the case an actor's characteristic is affected by it.
# Talents' effects may be null or 0 if they are not required to be applied.
class SkillsSchema(GameSchema):
    skill_id = fields.Integer(required = True),
    skill_desc = fields.String

class TalentsSchema(GameSchema):
    talent_id = fields.Integer(required = True),
    talent_desc = fields.String,
    talent_effect = fields.Integer

# An Actor is a Character that can be managed by a player or by the AI built-in the game.
# Actors can be generated randomly, as well can be made by an user.
class ActorSchema(GameSchema):
    actor_id = fields.Integer(required= True),
    race_id = fields.Integer(required= True),
    actor_name = fields.String(required= True),
    actor_current_career = fields.Integer(required= True),
    actor_previous_career = fields.List(fields.Integer),
    actor_ws = fields.Integer(required= True),
    actor_bs = fields.Integer(required= True),
    actor_s = fields.Integer(required= True),
    actor_t = fields.Integer(required= True),
    actor_ag = fields.Integer(required= True),
    actor_int = fields.Integer(required= True),
    actor_wp = fields.Integer(required= True),
    actor_fel = fields.Integer(required= True),
    actor_a = fields.Integer(required= True),
    actor_w = fields.Integer(required= True),
    actor_m = fields.Integer(required= True),
    actor_mag = fields.Integer(required= True),
    actor_ip = fields.Integer(required= True),
    actor_fp = fields.Integer(required= True),
    actor_skills = fields.List(fields.List(fields.Integer(required= True))),
    actor_talents = fields.List(fields.Integer(required= True)),
    actor_experience = fields.Integer,
    actor_advancements = fields.Integer



# Memory is part of an Actor actual progress of advancements. This will check if someone is able to advance
# If only the career's table allows it by comparing values.
class ActorMemorySchema (GameSchema):
    actor_id = fields.Integer(required=True),
    memory_ws = fields.Integer,
    memory_bs = fields.Integer,
    memory_s = fields.Integer,
    memory_t = fields.Integer,
    memory_ag = fields.Integer,
    memory_int = fields.Integer,
    memory_wp = fields.Integer,
    memory_fel = fields.Integer,
    memory_a = fields.Integer,
    memory_w = fields.Integer,
    memory_m = fields.Integer,
    memory_mag = fields.Integer

# Similar to the Memory above, however, it nests skill ranks in the case it can progress in the next career.
# If a current career the user has the option to upgrade a skill, then it must be nested as {skillID, skillRank}
# Skill rank are as follow. 0 = Not Learned, 1 = Learned, 2 = actor characteristic + 10, 3 = actor's characteristic + 20.
# Any futher value if a new career can be applied above 3, will be considered already "mastered" by standard Corebook.
class ActorMemorySkillsTalentsSchema(GameSchema):
    actor_id = fields.Integer(required=True),
    memory_skills = fields.List(fields.List(fields.Integer)),
    memory_talents = fields.List(fields.Integer)

# Users Tables and Classes. Each Instance of a profile may be able to create one singular actor until they must replace it by the occurance of playing and meeting
# Certain game overs screens.
class UserProfileSchema(GameSchema):
    user_id = fields.Integer(required=True),
    user_name = fields.String(required=True),
    created_at = fields.DateTime(dt_format='rfc822')


def  CreateActor(race_id):
    #Human
    if race_id == 1:
        #Stats Bases are 20
        ws = 20 + random.randint(2, 20)
        bs = 20 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 20 + random.randint(2, 20)
        ag = 20 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 20 + random.randint(2, 20) 
        #Skill List to be made

        #Until Here
        check = False
        talent1 = 0
        talent2 = 0
        while(check != True):
            if(talent1 == 0):
                talent1 = random.randint(2, 20)
                talent2 = random.randint(2, 20) #Talent List to be made
            if(talent1 != talent2):
                check = True
            else:
                talent2 = random.randint(2, 20)
        print(1)
    #Dwarf
    elif race_id == 2:
        ws = 30 + random.randint(2, 20)
        bs = 20 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 30 + random.randint(2, 20)
        ag = 10 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 10 + random.randint(2, 20)
        print(1)
    #Halfling
    elif race_id == 3:
        ws = 10 + random.randint(2, 20)
        bs = 30 + random.randint(2, 20)
        s = 10 + random.randint(2, 20)
        t = 10 + random.randint(2, 20)
        ag = 30 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 30 + random.randint(2, 20)
        print(1)
    #Elf
    else:
        ws = 20 + random.randint(2, 20)
        bs = 30 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 20 + random.randint(2, 20)
        ag = 30 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 20 + random.randint(2, 20)
        print(1)
    return 1

"""
Old Code
WF_Career_Fields = {
    'career_id': fields.Integer(required= True),
    'career_title': fields.String(required= True),
    'career_desc': fields.String,
    'career_ws': fields.Integer(required= True),
    'career_bs': fields.Integer(required= True),
    'career_s': fields.Integer(required= True),
    'career_t': fields.Integer(required= True),
    'career_ag': fields.Integer(required= True),
    'career_int': fields.Integer(required= True),
    'career_wp': fields.Integer(required= True),
    'career_fel': fields.Integer(required= True),
    'career_a': fields.Integer(required= True),
    'career_w': fields.Integer(required= True),
    'career_m': fields.Integer(required= True),
    'career_mag': fields.Integer(required= True),
    'career_mandatory_skills': fields.List(fields.Integer(required= True)),
    'career_selectable_skills': fields.List(fields.Integer),
    'career_mandatory_talents': fields.List(fields.Integer(required= True)),
    'career_selectable_talents': fields.List(fields.List(fields.Integer)),
    'career_entries': fields.List(fields.Integer),
    'career_exits': fields.List(fields.Integer) 
}

# Race Table is only for the purposes of generating a character by the user or system. Each characteristic has a base number that will use the rolling function.
# Race wounds and fate points rolls will be based on the race id, which normally would be as: 1 = human, 2 = dwarf, 3 = halfling, 4 = elf.
# These 2 will be compared in the function. 

WF_Race_Fields = {
    'race_id' : fields.Integer(required= True),
    'race_name' : fields.String(required= True),
    'race_ws': fields.Integer(required= True),
    'race_bs': fields.Integer(required= True),
    'race_s': fields.Integer(required= True),
    'race_t': fields.Integer(required= True),
    'race_ag': fields.Integer(required= True),
    'race_int': fields.Integer(required= True),
    'race_wp': fields.Integer(required= True),
    'race_fel': fields.Integer(required= True),
    'race_m' : fields.Integer(required = True)
}

# Skills & Talents. Skills are self-defined by the corebook standard.
# Talents must have an effect attached in the case an actor's characteristic is affected by it.
# Talents' effects may be null or 0 if they are not required to be applied.
WF_Skills_Fields ={
    'skill_id' : fields.Integer(required= True),
    'skill_desc' : fields.String
}

WF_Talents_Fields ={
    'talent_id' : fields.Integer(required= True),
    'talent_desc' : fields.String,
    'talent_effect' : fields.Integer
}

# An Actor is a Character that can be managed by a player or by the AI built-in the game.
# Actors can be generated randomly, as well can be made by an user.
WF_Actor_Fields = {
    'actor_id': fields.Integer(required= True),
    'race_id' : fields.Integer(required= True),
    'actor_name': fields.String(required= True),
    'actor_current_career': fields.Integer(required= True),
    'actor_previous_career': fields.List(fields.Integer),
    'actor_ws': fields.Integer(required= True),
    'actor_bs': fields.Integer(required= True),
    'actor_s': fields.Integer(required= True),
    'actor_t': fields.Integer(required= True),
    'actor_ag': fields.Integer(required= True),
    'actor_int': fields.Integer(required= True),
    'actor_wp': fields.Integer(required= True),
    'actor_fel': fields.Integer(required= True),
    'actor_a': fields.Integer(required= True),
    'actor_w': fields.Integer(required= True),
    'actor_sb': fields.Integer(required= True),
    'actor_tb': fields.Integer(required= True),
    'actor_m': fields.Integer(required= True),
    'actor_mag': fields.Integer(required= True),
    'actor_ip': fields.Integer(required= True),
    'actor_fp': fields.Integer(required= True),
    'actor_skills': fields.List(fields.List(fields.Integer(required= True))),
    'actor_talents': fields.List(fields.Integer(required= True)),
    'actor_experience' : fields.Integer,
    'actor_advancements' : fields.Integer
}

# Memory is part of an Actor actual progress of advancements. This will check if someone is able to advance
# If only the career's table allows it by comparing values.
WF_Actor_Memory_Fields = {
    'actor_id': fields.Integer(required= True),
    'memory_ws': fields.Integer,
    'memory_bs': fields.Integer,
    'memory_s': fields.Integer,
    'memory_t': fields.Integer,
    'memory_ag': fields.Integer,
    'memory_int': fields.Integer,
    'memory_wp': fields.Integer,
    'memory_fel': fields.Integer,
    'memory_a': fields.Integer,
    'memory_w': fields.Integer,
    'memory_sb': fields.Integer,
    'memory_tb': fields.Integer,
    'memory_m': fields.Integer,
    'memory_mag': fields.Integer
}
# Similar to the Memory above, however, it nests skill ranks in the case it can progress in the next career.
# If a current career the user has the option to upgrade a skill, then it must be nested as {skillID, skillRank}
# Skill rank are as follow. 0 = Not Learned, 1 = Learned, 2 = actor characteristic + 10, 3 = actor's characteristic + 20.
# Any futher value if a new career can be applied above 3, will be considered already "mastered" by standard Corebook.
WF_Actor_Memory_Skills_Talents_Fields = {
    'actor_id': fields.Integer(required= True),
    'memory_skills' : fields.List(fields.List(fields.Integer)),
    'memory_talents': fields.List(fields.Integer)
}

# Users Tables and Classes. Each Instance of a profile may be able to create one singular actor until they must replace it by the occurance of playing and meeting
# Certain game overs screens.

WF_UserProfile = {
    'user_id' : fields.Integer(required= True),
    'user_name' : fields.String(required=True),
    'created_at' : fields.DateTime(dt_format='rfc822')
}

def  CreateActor(race_id):
    #Human
    if race_id == 1:
        #Stats Bases are 20
        ws = 20 + random.randint(2, 20)
        bs = 20 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 20 + random.randint(2, 20)
        ag = 20 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 20 + random.randint(2, 20) 
        #Skill List to be made

        #Until Here
        check = False
        talent1 = 0
        talent2 = 0
        while(check != True):
            if(talent1 == 0):
                talent1 = random.randint(2, 20)
                talent2 = random.randint(2, 20) #Talent List to be made
            if(talent1 != talent2):
                check = True
            else:
                talent2 = random.randint(2, 20)
        print(1)
    #Dwarf
    elif race_id == 2:
        ws = 30 + random.randint(2, 20)
        bs = 20 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 30 + random.randint(2, 20)
        ag = 10 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 10 + random.randint(2, 20)
        print(1)
    #Halfling
    elif race_id == 3:
        ws = 10 + random.randint(2, 20)
        bs = 30 + random.randint(2, 20)
        s = 10 + random.randint(2, 20)
        t = 10 + random.randint(2, 20)
        ag = 30 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 30 + random.randint(2, 20)
        print(1)
    #Elf
    else:
        ws = 20 + random.randint(2, 20)
        bs = 30 + random.randint(2, 20)
        s = 20 + random.randint(2, 20)
        t = 20 + random.randint(2, 20)
        ag = 30 + random.randint(2, 20)
        int = 20 + random.randint(2, 20)
        wp = 20 + random.randint(2, 20)
        fel = 20 + random.randint(2, 20)
        print(1)
    return 1


"""