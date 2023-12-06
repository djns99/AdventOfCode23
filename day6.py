import math

def part1(lines):
    time = lines[0].split(":")[1].strip().split(" ")
    distance = lines[1].split(":")[1].strip().split(" ")
    time = list(map(int, filter(None,  time)))
    distance = list(map(int, filter(None,distance)))

    result = 1
    for t, d in zip(time, distance):
        passes = 0
        for i in range(t):
            if i * (t - i) > d:
                passes += 1
        print(passes, '/', t)
        result *= passes
    print(result)


def part2(lines):
    time = int("".join(lines[0].split(":")[1].strip().split(" ")))
    distance = int("".join(lines[1].split(":")[1].strip().split(" ")))
    # Solution x(t-x) = d
    result1 = math.ceil((-time + math.sqrt(time*time - 4 * distance)) / 2)
    result2 = math.ceil((-time - math.sqrt(time*time - 4 * distance)) / 2)
    print(result1 - result2)

def main(input):
    part1(input.strip().split("\n"))
    part2(input.strip().split("\n"))

input = """
Time:        59     79     65     75
Distance:   597   1234   1032   1328
"""
main(input)