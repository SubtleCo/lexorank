import math

from cipher import decipher, recipher


def pad_original_ranks(low, high):
    padded_high = high
    padded_low = low
    while len(padded_low) > len(padded_high):
        padded_high = padded_high + [0]
    while len(padded_low) < len(padded_high):
        padded_low = padded_low + [0]
    return padded_low, padded_high


def numericize(item: list[int]) -> int:
    """ Convert a list of base64 integer elements to a single base10 integer """
    numerical_rank = 0
    for i, number in enumerate(item):
        n = len(item) - i - 1
        x = number * 26**n
        numerical_rank += x
    return numerical_rank


def find_mean(high, low):
    """ Find the mean between two base10 numbers """
    floored_mean = math.floor((high + low)/2)
    return floored_mean


def rebase(number: int, cipher_length: int) -> list[int]:
    """ Convert a single base10 integer to a list of base64 integer elements """
    rebased_number = []
    n = cipher_length - 1
    for i in range(cipher_length):
        x = math.floor(number/26**n % 26)
        rebased_number.append(x)
        n -= 1
    return rebased_number


def validate_rank(low, high, new):
    """ Ensure the new rank is available. If not, tack on 'n' """
    if new not in (low, high):
        return new
    return new + 'n'


if __name__ == '__main__':

    low_rank = 'aaabbs'
    high_rank = 'aaabbt'

    print(f"{low_rank=}")
    print(f"{high_rank=}")

    cipher_length = len(low_rank) if len(low_rank) >= len(high_rank) else len(high_rank)
    print(f"{cipher_length=}")

    deciphered_low = decipher(low_rank, cipher_length)
    print(f"{deciphered_low}")
    deciphered_high = decipher(high_rank, cipher_length)
    print(f"{deciphered_high}")

    padded_low, padded_high = pad_original_ranks(deciphered_low, deciphered_high)
    print(f"{padded_low=}")
    print(f"{padded_high=}")

    numerical_low = numericize(padded_low)
    print(f"{numerical_low=}")
    numerical_high = numericize(padded_high)
    print(f"{numerical_high=}")

    mean = find_mean(numerical_high, numerical_low)
    print(f"{mean=}")

    rebased_number = rebase(mean, cipher_length)
    print(f"{rebased_number=}")

    new_rank = recipher(rebased_number)
    print(f"{new_rank=}")

    valid_rank = validate_rank(low_rank, high_rank, new_rank)
    print(f"{valid_rank=}")
