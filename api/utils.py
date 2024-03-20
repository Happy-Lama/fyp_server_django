def binary_to_float_ieee754(bytes):
        
        sign = -1 if bytes[0] & 0b10000000 else 1  # Checking the sign bit
        exponent = ((bytes[0] & 0b01111111) << 1) | (bytes[1] >> 7)  # Extracting the exponent
        
        # Extracting the mantissa
        mantissa = ((bytes[1] & 0b01111111) << 16) | (bytes[2] << 8) | bytes[3]
        
        if exponent == 0 and mantissa == 0:
            return 0  # Handling special case for zero
        
        float_value = pow(2, exponent - 127) * (1 + mantissa / pow(2, 23))
        
        return sign * float_value


def decode_uplink(input_str):
    input_bytes = bytearray.fromhex(input_str)
    float_values = []
    for i in range(0, len(input_bytes) - 1, 4):
        float_values.append(binary_to_float_ieee754(input_bytes[i:i+4]))
        
    decoded_payload = {
        "line_to_neutral": float_values[0:3],
        "phase_current": float_values[3:6],
        "active_power_per_phase": float_values[6:9],
        "apparent_power_per_phase": float_values[9:12],
        "reactive_power_per_phase": float_values[12:15],
        "power_factor_per_phase": float_values[15:18],
        "frequency":float_values[-1],
        "status": int(input_bytes[-1])
    } 
    
    return decoded_payload


