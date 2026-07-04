def decode_samsung_timers(bytes_arr):
    if len(bytes_arr) < 21:
        print("Invalid payload length.")
        return

    # 1. Extract Off-Timer (Byte 10 Lower Nibble + Byte 9 Upper Nibble)
    off_val = ((bytes_arr[10] & 0x0F) << 4) + (bytes_arr[9] >> 4)
    off_hours = 0.0
    
    if off_val > 0:
        off_hours = (off_val // 8) + (0.5 if off_val % 8 == 3 else 0.0)

    # 2. Extract On-Timer (Byte 11 Lower Nibble + Byte 10 Upper Nibble)
    on_val = ((bytes_arr[11] & 0x0F) << 4) + (bytes_arr[10] >> 4)
    on_hours = 0.0
    
    if on_val > 0:
        on_hours = (on_val // 8) + (0.5 if on_val % 8 == 3 else 0.0)

    # 3. Print Results
    if off_hours > 0 and on_hours > 0:
        print(f"Dual Timer Active: On in {on_hours:.1f}h, Off in {off_hours:.1f}h")
    elif off_hours > 0:
        print(f"Off Timer Active: Off in {off_hours:.1f}h")
    elif on_hours > 0:
        print(f"On Timer Active: On in {on_hours:.1f}h")
    else:
        print("No Active Timers.")

if __name__ == "__main__":
    print("Testing Samsung Dual-Timer Decoder...\n")

    # Example 1: 0.5h Off Timer
    b = [0x00] * 21
    b[8], b[9], b[10], b[11] = 0xA2, 0x3F, 0x00, 0x00
    print("Test 1 (0.5h Off Timer):")
    decode_samsung_timers(b)

    # Example 2: 1.5h Off Timer
    b[8], b[9], b[10], b[11] = 0x92, 0xBF, 0x00, 0x00
    print("\nTest 2 (1.5h Off Timer):")
    decode_samsung_timers(b)

    # Example 3: Dual Timer - On in 0.5h, Off in 1.0h
    b[8], b[9], b[10], b[11] = 0x82, 0x8F, 0x30, 0x00
    print("\nTest 3 (Dual: On 0.5h, Off 1.0h):")
    decode_samsung_timers(b)
