# S-DES Design Document

## 1. Objective

This project implements the Simplified Data Encryption Standard (S-DES) algorithm.

The program supports:
- Encryption of 8-bit plaintext using a 10-bit key
- Decryption of 8-bit ciphertext using the same key
- Verification using a predefined test case

The implementation follows the official S-DES specification.

---

## 2. System Overview

S-DES is a simplified version of DES that operates on:
- 8-bit data blocks
- 10-bit keys

The encryption structure is:

IP → fk(K1) → Switch → fk(K2) → IP⁻¹

The decryption structure is identical, except that subkeys are applied in reverse order.

---

## 3. Key Generation (Key Schedule)

The 10-bit key is used to generate two subkeys: K1 and K2.

Steps:
1. Apply permutation P10
2. Split into left and right halves (5 bits each)
3. Perform left shift (LS-1) on both halves
4. Apply P8 → generate K1
5. Perform left shift (LS-2) on both halves
6. Apply P8 → generate K2

This ensures that different round keys are used in each round.

---

## 4. Encryption Process

### Step 1: Initial Permutation (IP)
Rearranges the input bits according to a fixed table.

### Step 2: First Round (fk with K1)
- Split into left (L) and right (R)
- Apply F-function on R using K1
- XOR result with L
- Combine new left with original right

### Step 3: Switch Function (Theta)
Swap left and right halves.

### Step 4: Second Round (fk with K2)
Repeat the same process using K2.

### Step 5: Inverse Initial Permutation (IP⁻¹)
Produces final ciphertext.

---

## 5. F-function Details

The F-function is the core of S-DES and consists of:

1. Expansion Permutation (EP)
   - Expands 4-bit input to 8 bits

2. XOR with subkey
   - Mixes key with data

3. S-box substitution
   - S0 and S1 convert 4-bit inputs into 2-bit outputs
   - Introduces non-linearity

4. P4 permutation
   - Rearranges bits to improve diffusion

---

## 6. Decryption Process

Decryption follows the same structure as encryption:

IP → fk(K2) → Switch → fk(K1) → IP⁻¹

Key point:
- Subkeys are applied in reverse order (K2 → K1)

This works because S-DES uses a Feistel structure.

---

## 7. Implementation Structure

The program is implemented in a modular way:

- `permute()` → handles all permutations
- `left_shift()` → circular shifts for key schedule
- `xor_bits()` → bitwise XOR
- `sbox_lookup()` → S-box computation
- `generate_subkeys()` → produces K1 and K2
- `fk()` → round function
- `encrypt()` → performs full encryption
- `decrypt()` → performs full decryption

The program is executed via command-line interface.

---

## 8. Input / Output Design

The program uses CLI arguments:

- Encrypt:

```sh
python src/sdes.py encrypt --key <10-bit> --text <8-bit>
```

- Decrypt:

```sh
python src/sdes.py decrypt --key <10-bit> --text <8-bit>
```

- Verification:

```sh
python src/sdes.py check
```

Input validation ensures:
- Key is 10-bit binary string
- Text is 8-bit binary string

---

## 9. Verification Case

The implementation is verified using the provided test case:

- Key: 0111111101
- Ciphertext: 10100010
- Midway (after switch): 00010011
- Final plaintext: 11101010

The program produces the correct result.

---

## 10. Design Considerations

- All tables follow the official S-DES specification
- Bit indexing strictly uses 0-based indexing
- No hardcoded file paths are used
- No external libraries are required
- Implementation supports automated testing

---

## 11. Conclusion

This implementation correctly follows the S-DES algorithm, including:
- Key generation
- Encryption and decryption
- Feistel structure
