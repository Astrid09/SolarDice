"""Dice functionality and Classes.

Example:
    foo = get_roll_from_message("dd12+3")
"""

from random import randint
from enum import Enum, auto
from dataclasses import dataclass

class RollType(Enum):
    """Type of roll (Normal, Advantage, Disadvantage)."""
    NORMAL = auto()
    ADVANTAGE = auto()
    DISADVANTAGE = auto()


class ModifierDie(Enum):
    """Advantage/Disadvantage die type."""
    D6 = auto()
    D8 = auto()
    D10 = auto()


class HopeDie(Enum):
    """Type of the hope die to be rolled."""
    D12 = auto()
    D20 = auto()


@dataclass
class _RollData:
    """Dataclass of a roll and all of it's fields."""
    base_modifier: int
    roll_type: RollType
    hope_die: HopeDie
    modifier_die: ModifierDie
    amount: int


@dataclass
class _RollResult:
    """Dataclass of the results of a roll."""
    hope_value: int
    fear_value: int
    hope_die: HopeDie
    modifier_value: int
    modifier_die: ModifierDie
    base_modifier: int

    def __str__(self) -> str:
        roll_aligment: str
        if self.hope_value == self.fear_value:
            result: int = self.hope_value + self.fear_value

            return (f"`Rolagem Crítica!` (**{result}**) ⟵ [**{self.hope_value}**] Esperança "
                    f"(d{self.hope_value}) = [**{self.fear_value}**] Medo (d12)")
        elif self.hope_value > self.fear_value:
            roll_aligment = "Esperança"
        else:
            roll_aligment = "Medo"

        roll_value: int = (
            self.fear_value + self.hope_value + self.modifier_value + self.base_modifier
        )
        roll_text: str = (f"`{roll_value} com {roll_aligment}` "
                        f"⟵ [**{self.hope_value}**] Esperança (d{self.hope_die}) + "
                        f"[**{self.fear_value}**] Medo (d12)")

        if self.modifier_value > 0:
            roll_text += f" + [**{self.modifier_value}**] Vantagem (d{self.modifier_die})"
        elif self.modifier_value < 0:
            roll_text += f" - [**{abs(self.modifier_value)}**] Desvantagem (d{self.modifier_die})"

        if self.base_modifier > 0:
            roll_text += f" + **{self.base_modifier}**"
        elif self.base_modifier < 0:
            roll_text += f" - **{abs(self.base_modifier)}**"

        return roll_text


def _roll_duality(roll: _RollData) -> _RollResult:
    """Roll duality dice and returns a result string.

    Args:
        roll (RollData): The data for the roll.

    Raises:
        ValueError: If hope dice type doesn't exist.
        ValueError: If modifier dice type doesn't exist.
        ValueError: If roll type doesn't exist.

    Returns:
        RollResult: The result of the roll to be parsed.
    """

    fear_roll: int = randint(1, 12)

    hope_die_value: int
    match roll.hope_die:
        case HopeDie.D12:
            hope_die_value = 12

        case HopeDie.D20:
            hope_die_value = 20

        case _:
            raise ValueError("Hope dice type doesn't exist.")

    hope_roll: int = randint(1, hope_die_value)

    modifier_die_type: int
    match roll.modifier_die:
        case ModifierDie.D6:
            modifier_die_type = 6

        case ModifierDie.D8:
            modifier_die_type = 8

        case ModifierDie.D10:
            modifier_die_type = 10

        case _:
            raise ValueError("Modifier dice type doesn't exist.")

    modifier_value: int
    match roll.roll_type:
        case RollType.ADVANTAGE:
            modifier_value = randint(1, modifier_die_type)

        case RollType.DISADVANTAGE:
            modifier_value = -randint(1, modifier_die_type)

        case RollType.NORMAL:
            modifier_value = 0

        case _:
            raise ValueError("Roll type doesn't exist.")

    return _RollResult(
        hope_value=hope_roll,
        fear_value=fear_roll,
        hope_die=roll.hope_die,
        modifier_value=modifier_value,
        modifier_die=roll.modifier_die,
        base_modifier=roll.base_modifier,
    )


def _roll_data_from_message(message: str) -> _RollData | None:
    """Creates a RollData from a message

    Args:
        message (str): The message to be turned into a roll.

    Returns:
        RollData|None: The RollData or None if the message was not a roll.
    """
    modifier: int = 0
    hope_die: HopeDie
    roll_type: RollType = RollType.NORMAL
    modifier_die: ModifierDie = ModifierDie.D6

    raw_message = message.lower().strip().replace(" ", "")

    if raw_message == "dd":
        # return roll_duality(0, RollTypes.NORMAL.value, HopeDice.D12.value, ModifierDice.D6.value)
        return _RollData(
            base_modifier=0,
            roll_type=RollType.NORMAL,
            hope_die=HopeDie.D12,
            modifier_die=ModifierDie.D6,
            amount=1,
        )

    if raw_message[0:2] != "dd":
        return None

    sliced_message: list[str] = raw_message.split("#")

    roll_number: int
    if sliced_message[0].isdecimal():
        roll_number = int(sliced_message[0].split("#")[0])
    else:
        roll_number = 1

    if len(sliced_message) != 1:
        raw_message = sliced_message[1]

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
    return _RollData(
        base_modifier=modifier,
        roll_type=roll_type,
        hope_die=hope_die,
        modifier_die=modifier_die,
        amount=roll_number,
    )


def _roll_multiple(roll: _RollData) -> list[_RollResult]:
    """Rolls duality based on RollData, can support mutiple rolls.

    Args:
        roll (RollData): The roll arguments data.

    Returns:
        list[RollResult]: The list of results of the rolls.
    """
    rolls: list[_RollResult] = []

    for _ in range(roll.amount):
        rolls.append(_roll_duality(roll))

    return rolls

def get_roll_from_message(message: str) -> str | None:
    """Returns the message to be printed based on a roll message.

    Args:
        message (str): The message to be turned into a roll.

    Returns:
        str|None: The message to be printed of the roll.
    """
    roll_data: _RollData | None = _roll_data_from_message(message)

    if not roll_data:
        return None

    if roll_data.amount == 1:
        return str(_roll_duality(roll_data))

    rolls = _roll_multiple(roll_data)

    result: str = ""
    for i, roll in enumerate(rolls):
        result += f"{i}. {roll}"

    return result


if __name__ == "__main__":
    print(get_roll_from_message("dd"))
