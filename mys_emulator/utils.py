def uint16_to_bit_array(value: int) -> list[int]:
    """ Small tool to help decoding received values"""
    if not (0 <= value <= 0xFFFF):  # Ensure it's a uint16
        raise ValueError("Value must be a 16-bit unsigned integer")

    return [(value >> i) & 1 for i in range(15, -1, -1)]  # Extract bits


def bit_array_to_uint16(bit_array: list[int]) -> int:
    if len(bit_array) != 16 or any(b not in (0, 1) for b in bit_array):
        raise ValueError("Input must be a list of 16 bits (0 or 1)")

    return sum(b << (15 - i) for i, b in enumerate(bit_array))
