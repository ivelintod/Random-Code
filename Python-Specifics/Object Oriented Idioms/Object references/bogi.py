inp = input('NIZ: ')
numbers = []
number = ''
i = 0
while i < len(inp):
    j = i
    if inp[i].isdigit():
        if inp[i - 1] == '-':
            number += '-'
        number += inp[i]
        j = i + 1
        while j < len(inp) and inp[j].isdigit():
            number += inp[j]
            j += 1
        numbers.append(number)
        number = ''
    i = j + 1

numbers = [int(x) for x in numbers]
print(sum(numbers))
