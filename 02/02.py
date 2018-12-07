#!/usr/bin/env python3

def group_by_letter(input):
    """ aabccc -> {'a': 2, 'b': 1, 'c': 3} """
    patterns = {}
    for letter in input:
        patterns[letter] = patterns.get(letter, 0) + 1
    return patterns

def is_id_valid(input):
    values = group_by_letter(input)
    return (2 in values.values(), 3 in values.values())

def remove_letter_from_string(string, i):
    return string[:i] + string[i+1:]

def generate_sublists(l, i):
    return list(map(lambda str: remove_letter_from_string(str, i), l))

input = [s[:-1] for s in open('input.txt').readlines()]

for i in range(len(input[0])):
    sublist_input = generate_sublists(input, i)
    if len(set(sublist_input)) == len(sublist_input):
        continue
    for k, v in group_by_letter(sublist_input).items():
        if v == 2:
            print(k)
            break
