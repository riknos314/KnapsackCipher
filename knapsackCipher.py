"""Knapsack cryptosystem"""
#!/usr/bin/env python3
#encoding: UTF-8

import random
from math import gcd


def are_coprime(a,b):
    return gcd(a,b) == 1


def find_coprime(num):
    coprimeLst = [i for i in range(num) if are_coprime(i, num)]
    return coprimeLst[random.randint(0, len(coprimeLst))]
        

def find_modular_inverse(r,q):
    for i in range(q):
        if (i*r) % q == 1:
            return i


def generate_superincreasing_knapsack(size):
    knapsack = []

    count = 0
    for i in range(size):
        newNum = 0
        while newNum <= count:
            newNum = random.randint(count+1, (255+count))

        count += newNum
        knapsack.append(newNum)

    return knapsack


def generate_general_knapsack(knapsack):

    nVal = sum(knapsack) + 1
    r = find_coprime(nVal)
    inverse = find_modular_inverse(r, nVal)

    return [(i*r)%nVal for i in knapsack],inverse


def generate_knapsacks(m_value, size):
    """Generate superincreasing and general knapsacks of the specified length"""
    knapsack_general = []
    knapsack_super = []
    inverse = 1

    knapsack_super = generate_superincreasing_knapsack(size)
    knapsack_general,inverse = generate_general_knapsack(knapsack_super)

    return knapsack_general, knapsack_super, inverse


def encrypt(letter_plain, knapsack_general):
    """Encrypt a single character"""
    secret = 0
    binLetter = '0' + bin(ord(letter_plain))[2:]

    for i, digit in enumerate(binLetter):
        if digit == '1':
            secret += knapsack_general[i]

    return secret


def decrypt(letter_cipher, knapsack_super, n_value, inverse):
    """Decrypt a single character"""
    plain = ['0' for i in range(8)] 
    inverseCount = (letter_cipher*inverse) % n_value
    for i, val in reversed(list(enumerate(knapsack_super))):
        if val <= inverseCount:
            plain[i] = '1'
            inverseCount -= val
    return ''.join(plain)


def main():
    """Main function"""
    # Generate knapsacks of length 8. Chosen m is 2017
    knapsack_general, knapsack_super, inverse = generate_knapsacks(2017, 8)

    n_value = sum(knapsack_super) + 1
    message = "L"
    cipher = encrypt(message, knapsack_general)
    print("Cipher is {}".format(cipher))
    plain = decrypt(cipher, knapsack_super, n_value, inverse)
    # Expected output: 76 = L
    print("{} = {}".format(int(plain, 2), chr(int(plain, 2))))


if __name__ == '__main__':
    main()
