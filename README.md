# S-DES Implementation

## Environment
- Python version: Python 3.8+
- No external libraries required (only standard library)

## Run

### Input Format
- Key: 10-bit binary string (e.g., 0111111101)
- Text: 8-bit binary string (plaintext or ciphertext)

Invalid input will raise an error.

---

### Encrypt
```sh
python sdes.py encrypt --key 0111111101 --text 11101010
```
or add `--debug` to see the process

### Decrypt
```sh
python sdes.py decrypt --key 0111111101 --text 10100010
```
or add `--debug` to see the process

### Verification
```sh
python sdes.py check
```

## Verification Case (provided by professor)
- Key: 0111111101
- Ciphertext: 10100010
- Midway after Theta during decryption: 00010011
- Final plaintext: 11101010

## Other Cases
Just simply put different value/text after `--key` and `--text`
```sh
python sdes.py encrypt --key 0000011111 --text 10101010
```
and then
```sh
python sdes.py decrypt --key 0000011111 --text <ciphertext>
```
should get the original plaintext

## Core idea
> plaintext → encrypt → ciphertext → decrypt → plaintext
