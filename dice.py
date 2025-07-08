from random import randint
from enum import Enum, auto
from typing import Optional
from dataclasses import dataclass


class RollType(Enum):
    NORMAL = auto()
    ADVANTAGE = auto()
    DISADVANTAGE = auto()


class ModifierDie(Enum):
    D6 = auto()
    D8 = auto()
    D10 = auto()


class HopeDie(Enum):
    D12 = auto()
    D20 = auto()


@dataclass
class RollData:
    base_modifier: int
    roll_type: RollType
    hope_die: HopeDie
    modifier_die: ModifierDie
    amount: int


def roll_duality(base_modifier: int, roll_type: RollType, hope_die: HopeDie, modifier_die: ModifierDie) -> str:    
    fear_roll: int = randint(1, 12)

    hope_die_value: int
    match hope_die:
        case HopeDie.D12:
            hope_die_value = 12
            
        case HopeDie.D20:
            hope_die_value = 20
            
        case _:
            raise ValueError("Hope dice type doesn't exist.")
    
    hope_roll: int = randint(1, hope_die_value)
    
    modifier_die_type: int
    match modifier_die:
        case ModifierDie.D6:
            modifier_die_type = 6
            
        case ModifierDie.D8:
            modifier_die_type = 8
            
        case ModifierDie.D10:
            modifier_die_type = 10
        
        case _:
            raise ValueError("Modifier dice type doesn't exist.")
    
    modifier_type: int
    match roll_type:
        case RollType.ADVANTAGE:
            modifier_type = randint(1, modifier_die_type)
            
        case RollType.DISADVANTAGE:
            modifier_type = -randint(1, modifier_die_type)
            
        case RollType.NORMAL:
            modifier_type = 0
        
        case _:
            raise ValueError("Roll type doesn't exist.")
            
    roll_aligment: str
    if hope_roll == fear_roll:
        return (f"`Rolagem Crítica!` (**{hope_roll + fear_roll}**) ⟵ [**{hope_roll}**] Esperança "
                f"(d{hope_die_value}) = [**{fear_roll}**] Medo (d12)")
    elif hope_roll > fear_roll:
        roll_aligment = "Esperança"
    else:
        roll_aligment = "Medo"
    
    roll_value: int = fear_roll + hope_roll + modifier_type + base_modifier
    roll_text: str = (f"`{roll_value} com {roll_aligment}` ⟵ [**{hope_roll}**] Esperança (d{hope_die_value}) + "
                      f"[**{fear_roll}**] Medo (d12)")
    
    if modifier_type > 0:
        roll_text += f" + [**{modifier_type}**] Vantagem (d{modifier_die_type})"
    elif modifier_type < 0:
        roll_text += f" - [**{abs(modifier_type)}**] Desvantagem (d{modifier_die_type})"
    
    if base_modifier > 0:
        roll_text += f" + **{base_modifier}**"
    elif base_modifier < 0:
        roll_text += f" - **{abs(base_modifier)}**"
    
    return roll_text


def message_dict(message: str) -> Optional[RollData]:
    modifier: int = 0
    hope_die: HopeDie
    roll_type: RollType = RollType.NORMAL
    modifier_die: ModifierDie = ModifierDie.D6
    
    raw_message = message.lower().strip().replace(" ", "")
    
    if raw_message == "dd":
        # return roll_duality(0, RollTypes.NORMAL.value, HopeDice.D12.value, ModifierDice.D6.value)
        return RollData(
            base_modifier=0,
            roll_type=RollType.NORMAL,
            hope_die=HopeDie.D12,
            modifier_die=ModifierDie.D6,
            amount=1,
        )
    
    sliced_message: list[str] = raw_message.split("#")
    
    roll_number: int
    if sliced_message[0].isdecimal():
        roll_number = int(sliced_message[0].split("#")[0])
    else:
        roll_number = 1
    
    if len(sliced_message) != 1:  
        raw_message = sliced_message[1]
    
    if raw_message[0:2] != "dd":
        return None
    
    match raw_message[2:4]:
        case "12":
            hope_die = HopeDie.D12
        
        case "20":
            hope_die = HopeDie.D20
            
        case _:
            hope_die = HopeDie.D12
    
    vantage_num: int = 0
    for i, char in enumerate(raw_message[2:]):
        match char:
            case 'v':
                vantage_num += 1
                
                match vantage_num:
                    case 1:
                        roll_type = RollType.ADVANTAGE
                    case 2:
                        modifier_die = ModifierDie.D8
                    case _:
                        modifier_die = ModifierDie.D10
            
            case 'i':
                vantage_num += 1
                
                match vantage_num:
                    case 1:
                        roll_type = RollType.DISADVANTAGE
                    case 2:
                        modifier_die = ModifierDie.D8
                    case _:
                        modifier_die = ModifierDie.D10
            
            case '+' | '-':
                try:
                    modifier: int = int(raw_message[i+2:])
                except ValueError:
                    return None
            
            case _:
                pass
    
    # return roll_multiple(modifier, roll_type, hope_die, modifier_die, roll_number)
    return RollData(
        base_modifier=modifier,
        roll_type=roll_type,
        hope_die=hope_die,
        modifier_die=modifier_die,
        amount=roll_number,
    )


def roll_dice(roll: RollData) -> str:
    roll_message: str = ""
    
    if roll.amount == 1:
        return roll_duality(roll.base_modifier, roll.roll_type, roll.hope_die, roll.modifier_die)
    
    
    for i in range(roll.amount):
        roll_message += f"{i+1}. {roll_duality(roll.base_modifier, roll.roll_type, roll.hope_die, roll.modifier_die)}\n"
    
    return roll_message
 

if __name__ == "__main__":
    pass