#!/usr/bin/env python3
"""
Student ID: B123245017
Name: 王心妤
Assignment 4.2
Copyright (c) 2026 王心妤. All rights reserved.
"""

from __future__ import annotations

import argparse
from typing import List, Tuple, Dict, Any


# tables from the simplified DES paper (0-indexed positions)

P10 = (2, 4, 1, 6, 3, 9, 0, 8, 7, 5)
P8 = (5, 2, 6, 3, 7, 4, 9, 8)

IP = (1, 5, 2, 0, 3, 7, 4, 6)
IP_INV = (3, 0, 2, 4, 6, 1, 7, 5)

"""
EP from the paper's T-map diagram:
output rows are [n7 n4 n5 n6] and [n5 n6 n7 n4]
so EP on (n4 n5 n6 n7) => (n7 n4 n5 n6 n5 n6 n7 n4)
in local 4-bit indexing [0,1,2,3], that becomes:
"""
EP = (3, 0, 1, 2, 1, 2, 3, 0)

P4 = (1, 3, 2, 0)

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2],
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3],
]

# validate that bits is a binary string of expected length
def validate_bitstring(bits: str, expected_len: int, name: str) -> None:
    if len(bits) != expected_len:
        raise ValueError(f"{name} must be exactly {expected_len} bits, got {len(bits)} bits.")
    if any(b not in "01" for b in bits):
        raise ValueError(f"{name} must contain only '0' or '1'.")


def permute(bits: str, table: Tuple[int, ...]) -> str:
    return "".join(bits[i] for i in table)


def left_shift(bits: str, n: int) -> str:
    n %= len(bits)
    return bits[n:] + bits[:n]

# bitwise XOR of two equal-length bit strings
def xor_bits(a: str, b: str) -> str:
    if len(a) != len(b):
        raise ValueError("xor_bits requires equal-length bit strings.")
    return "".join("1" if x != y else "0" for x, y in zip(a, b))


def split_in_half(bits: str) -> Tuple[str, str]:
    if len(bits) % 2 != 0:
        raise ValueError("Bit string length must be even.")
    mid = len(bits) // 2
    return bits[:mid], bits[mid:]


def sbox_lookup(sbox: List[List[int]], bits4: str) -> str:
    """
    S-box lookup for a 4-bit input.
    row = first and fourth bits.
    column = second and third bits.
    output = 2-bit binary string.
    """
    if len(bits4) != 4:
        raise ValueError("sbox_lookup expects exactly 4 bits.")

    row = int(bits4[0] + bits4[3], 2)
    col = int(bits4[1] + bits4[2], 2)
    value = sbox[row][col]
    return format(value, "02b")

# Theta map: switch first four bits with last four bits
def switch_halves(bits8: str) -> str:
    validate_bitstring(bits8, 8, "8-bit block")
    left, right = split_in_half(bits8)
    return right + left


# Key schedule

def generate_subkeys(key10: str) -> Tuple[str, str]:
    """
    generate K1 and K2 from a 10-bit key
    - P10
    - LS-1 on each half -> P8 = K1
    - LS-2 on each half (from previous state) -> P8 = K2
    """
    validate_bitstring(key10, 10, "Key")

    p10 = permute(key10, P10)
    left, right = split_in_half(p10)

    left1 = left_shift(left, 1)
    right1 = left_shift(right, 1)
    k1 = permute(left1 + right1, P8)

    left2 = left_shift(left1, 2)
    right2 = left_shift(right1, 2)
    k2 = permute(left2 + right2, P8)

    return k1, k2


# round function fk

def f_function(right4: str, subkey8: str, debug: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    compute the S-DES F-function on the right 4 bits with an 8-bit subkey
    Returns:
        p4_output (4 bits), debug_info
    """
    validate_bitstring(right4, 4, "Right half")
    validate_bitstring(subkey8, 8, "Subkey")

    expanded = permute(right4, EP)
    xored = xor_bits(expanded, subkey8)

    left4, right4_x = split_in_half(xored)

    s0_out = sbox_lookup(S0, left4)
    s1_out = sbox_lookup(S1, right4_x)

    combined = s0_out + s1_out
    p4_out = permute(combined, P4)

    debug_info = {
        "right_input": right4,
        "expanded": expanded,
        "xored_with_subkey": xored,
        "left4_to_S0": left4,
        "right4_to_S1": right4_x,
        "S0_out": s0_out,
        "S1_out": s1_out,
        "combined_sbox_out": combined,
        "p4_out": p4_out,
    }

    return p4_out, debug_info


def fk(bits8: str, subkey8: str, debug: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    S-DES fk function:
    - split 8 bits into left/right 4 bits
    - apply F to right half
    - XOR result into left half
    - return new_left + original_right
    """
    validate_bitstring(bits8, 8, "8-bit block")
    validate_bitstring(subkey8, 8, "Subkey")

    left, right = split_in_half(bits8)
    f_out, f_debug = f_function(right, subkey8, debug=debug)
    new_left = xor_bits(left, f_out)
    out = new_left + right

    debug_info = {
        "input": bits8,
        "left": left,
        "right": right,
        "f_debug": f_debug,
        "new_left": new_left,
        "output": out,
    }

    return out, debug_info


# encrypt / decrypt

def encrypt(plaintext8: str, key10: str, debug: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    encrypt one 8-bit block using S-DES

    encryption:
        IP -> fk(K1) -> switch -> fk(K2) -> IP^-1
    """
    validate_bitstring(plaintext8, 8, "Plaintext")
    validate_bitstring(key10, 10, "Key")

    k1, k2 = generate_subkeys(key10)

    ip = permute(plaintext8, IP)
    round1, round1_debug = fk(ip, k1, debug=debug)
    switched = switch_halves(round1)
    round2, round2_debug = fk(switched, k2, debug=debug)
    ciphertext = permute(round2, IP_INV)

    debug_info = {
        "k1": k1,
        "k2": k2,
        "ip": ip,
        "after_fk_k1": round1,
        "after_switch": switched,
        "after_fk_k2": round2,
        "ciphertext": ciphertext,
        "round1_debug": round1_debug,
        "round2_debug": round2_debug,
    }

    return ciphertext, debug_info


def decrypt(ciphertext8: str, key10: str, debug: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    decrypt one 8-bit block using S-DES

    decryption:
        IP -> fk(K2) -> switch -> fk(K1) -> IP^-1
    """
    validate_bitstring(ciphertext8, 8, "Ciphertext")
    validate_bitstring(key10, 10, "Key")

    k1, k2 = generate_subkeys(key10)

    ip = permute(ciphertext8, IP)
    round1, round1_debug = fk(ip, k2, debug=debug)
    switched = switch_halves(round1)
    round2, round2_debug = fk(switched, k1, debug=debug)
    plaintext = permute(round2, IP_INV)

    debug_info = {
        "k1": k1,
        "k2": k2,
        "ip": ip,
        "after_fk_k2": round1,
        "after_switch": switched,
        "after_fk_k1": round2,
        "plaintext": plaintext,
        "round1_debug": round1_debug,
        "round2_debug": round2_debug,
    }

    return plaintext, debug_info


# CLI (just for the verification test case)

def run_assignment_check() -> None:
    """
    verification case:
      Key:        0111111101
      Ciphertext: 10100010
      Midway:     after switch during decryption must be 00010011
      Plaintext:  11101010
    """
    key = "0111111101"
    ciphertext = "10100010"
    expected_switch = "00010011"
    expected_plaintext = "11101010"

    plaintext, info = decrypt(ciphertext, key, debug=True)

    print("=== Verification Case ===")
    print(f"Key                 : {key}")
    print(f"Ciphertext          : {ciphertext}")
    print(f"Generated K1        : {info['k1']}")
    print(f"Generated K2        : {info['k2']}")
    print(f"After IP            : {info['ip']}")
    print(f"After fk(K2)        : {info['after_fk_k2']}")
    print(f"After switch (Theta): {info['after_switch']}")
    print(f"After fk(K1)        : {info['after_fk_k1']}")
    print(f"Recovered plaintext : {plaintext}")
    print()

    if info["after_switch"] != expected_switch:
        raise AssertionError(
            f"Midway check failed: expected {expected_switch}, got {info['after_switch']}"
        )

    if plaintext != expected_plaintext:
        raise AssertionError(
            f"Plaintext check failed: expected {expected_plaintext}, got {plaintext}"
        )

    print("Verification PASSED.")


def main() -> None:
    parser = argparse.ArgumentParser(description="S-DES encrypt/decrypt")
    parser.add_argument("mode", choices=["encrypt", "decrypt", "check"], help="Mode")
    parser.add_argument("--key", help="10-bit key")
    parser.add_argument("--text", help="8-bit plaintext or ciphertext")
    parser.add_argument("--debug", action="store_true", help="Print intermediate steps")

    args = parser.parse_args()

    if args.mode == "check":
        run_assignment_check()
        return

    # error if missing key or text
    if args.key is None or args.text is None:
        parser.error("encrypt/decrypt mode requires --key and --text")

    if args.mode == "encrypt":
        result, info = encrypt(args.text, args.key, debug=args.debug)
        if args.debug:
            print("K1:", info["k1"])
            print("K2:", info["k2"])
            print("After IP:", info["ip"])
            print("After fk(K1):", info["after_fk_k1"])
            print("After switch:", info["after_switch"])
            print("After fk(K2):", info["after_fk_k2"])
        print(result)

    elif args.mode == "decrypt":
        result, info = decrypt(args.text, args.key, debug=args.debug)
        if args.debug:
            print("K1:", info["k1"])
            print("K2:", info["k2"])
            print("After IP:", info["ip"])
            print("After fk(K2):", info["after_fk_k2"])
            print("After switch:", info["after_switch"])
            print("After fk(K1):", info["after_fk_k1"])
        print(result)


if __name__ == "__main__":
    main()