from typing import List, Optional
from dataclasses import dataclass

@dataclass
class SamsungACTimers:
    on_hours: float
    off_hours: float

@dataclass
class SamsungACState:
    power: bool
    power_str: str
    mode: int
    mode_str: str
    temp: int
    fan: int
    fan_str: str
    timers: Optional[SamsungACTimers]

def _decode_timers(bytes_arr: List[int]) -> Optional[SamsungACTimers]:
    """
    Decodes the On and Off timers from a 21-byte Samsung Air Conditioner IR payload.
    
    Args:
        bytes_arr (List[int]): An array of 21 integers representing the raw IR bytes.
        
    Returns:
        Optional[SamsungACTimers]: An object containing 'on_hours' and 'off_hours' as floats.
                                   Returns None if the payload length is invalid.
    """
    if len(bytes_arr) < 21:
        return None

    timer_15m_units = bytes_arr[12]

    # 1. Extract Off-Timer
    off_val = ((bytes_arr[10] & 0x0F) << 4) + (bytes_arr[9] >> 4)
    off_hours = 0.0
    if bytes_arr[8] == 0xB2 and timer_15m_units > 0:
        off_hours = timer_15m_units / 4.0
    elif off_val > 0:
        off_hours = (off_val // 8) + (0.5 if off_val % 8 == 3 else 0.0)

    # 2. Extract On-Timer
    on_val = ((bytes_arr[11] & 0x0F) << 4) + (bytes_arr[10] >> 4)
    on_hours = 0.0
    if bytes_arr[8] == 0xA2 and timer_15m_units > 0:
        on_hours = timer_15m_units / 4.0
    elif on_val > 0:
        on_hours = (on_val // 8) + (0.5 if on_val % 8 == 3 else 0.0)

    return SamsungACTimers(on_hours=on_hours, off_hours=off_hours)

MODE_LABELS = {0: "Auto", 1: "Cool", 2: "Dry", 3: "Fan", 4: "Heat", 8: "Auto (Legacy)"}
FAN_LABELS = {0: "Auto", 2: "Low", 4: "Med", 5: "High"}

def decode(bytes_arr: List[int]) -> Optional[SamsungACState]:
    """
    Decodes the full state (power, mode, temp, fan, timers) from a Samsung AC IR payload.
    
    Args:
        bytes_arr (List[int]): An array of integers representing the raw IR bytes.
        
    Returns:
        Optional[SamsungACState]: An object containing the decoded state.
    """
    if len(bytes_arr) < 14:
        return None
        
    data_idx = len(bytes_arr) - 7
    temp = ((bytes_arr[data_idx + 4] >> 4) & 0x0F) + 16
    fan = (bytes_arr[data_idx + 5] >> 1) & 0x07
    mode = (bytes_arr[data_idx + 5] >> 4) & 0x07
    power = (bytes_arr[data_idx + 6] >> 4) & 0x03
    
    state = SamsungACState(
        power=power == 3,
        power_str={"0": "OFF", "3": "ON"}.get(str(power), f"Unknown({power})"),
        mode=mode,
        mode_str=MODE_LABELS.get(mode, str(mode)),
        temp=temp,
        fan=fan,
        fan_str=FAN_LABELS.get(fan, str(fan)),
        timers=None
    )
    
    if len(bytes_arr) >= 21:
        state.timers = _decode_timers(bytes_arr)
        
    return state

