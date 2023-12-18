
def hash_algorithm(input: str):
    current_value = 0
    for c in input:
        assert c != "\n"
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

print(hash_algorithm("HASH"))

# input_lines = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(",")

f = open("day15-input.txt")
input_lines = f.readlines()[0].split(",")

result = 0
for line in input_lines:
    print(line)
    result += hash_algorithm(line.strip())

print(result)