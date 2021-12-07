from parse import read_input_file, write_output_file
import os
from random import random, shuffle, seed, sample
from math import exp

def output_str(tasks):
    out = []
    time = 0
    for task in tasks:
        time += task.get_duration()
        if time <= 1440:
            out.append(task.get_task_id())
    return out

def temp(x, size):
    return (1/(1+exp(-4*(x-1)))) * size


def score(tasks):
    time = 0
    score = 0
    for task in tasks:
        time += task.get_duration()
        if time > 1440:
            return score
        score += task.get_late_benefit(task.get_deadline() - time)
    return score

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    # seed(285303794)
    newtasks = tasks.copy()
    shuffle(newtasks)
    curScore = score(tasks)
    newScore = score(newtasks)
    if newScore > curScore:
        tasks = newtasks.copy()
        curScore = newScore
    else:
        newtasks = tasks.copy()
    SIZE = len(tasks)
    STEPS = 100000
    for i in range(STEPS):
        if i % (STEPS // 100) == 0:
            print(str(i / (STEPS // 100)) + "%")
        volatility = temp(1 - (i + 1)/STEPS, SIZE)
        swaps = iter(sample(range(0, SIZE), int(volatility // 2 * 2)))
        for swap1, swap2 in zip(swaps, swaps):
            newtasks[swap1], newtasks[swap2] = newtasks[swap2], newtasks[swap1]
            newScore = score(newtasks)
            exponent = (curScore - newScore)/volatility
            if exponent <= 0 and exp(exponent) < random():
                tasks = newtasks.copy()
                curScore = newScore
            else:
                newtasks = tasks.copy()
    return output_str(tasks)


# Here's an example of how to run your solver.
if __name__ == '__main__':
    TEST_SINGLE = "small/small-1.in"
    # TEST_SINGLE = ""
    if TEST_SINGLE:
        input_path = 'inputs/{}'.format(TEST_SINGLE)
        output_path = 'outputs/{}.out'.format(TEST_SINGLE[:-3])
        tasks = read_input_file(input_path)
        output = solve(tasks)
        write_output_file(output_path, output)
    else:
        for size in os.listdir('inputs/'):
            if size not in ['small']:
                continue
            for input_file in os.listdir('inputs/{}/'.format(size)):
                if size not in input_file:
                    continue
                input_path = 'inputs/{}/{}'.format(size, input_file)
                output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
                print(input_path, output_path)
                tasks = read_input_file(input_path)
                print("Solving...")
                output = solve(tasks)
                print("Completed")
                write_output_file(output_path, output)
