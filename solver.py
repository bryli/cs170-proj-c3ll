from parse import read_input_file, write_output_file
import os
from random import random, shuffle, seed, sample
from math import exp
from multiprocessing import Pool, current_process
import itertools
from prepare_submission import processOutput

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
        score += task.get_late_benefit(time - task.get_deadline())
    return score

def solve(tasks, prScore=False):
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
    STEPS = 1000000
    for i in range(STEPS):
        # if i % (STEPS // 10) == 0:
        #     print(str(i / (STEPS // 10) * 10) + "%")
        volatility = temp(1 - (i + 1)/STEPS, SIZE)
        swaps = iter(sample(range(0, SIZE), int(volatility // 2 * 2)))
        for swap1, swap2 in zip(swaps, swaps):
            newtasks[swap1], newtasks[swap2] = newtasks[swap2], newtasks[swap1]
            newScore = score(newtasks)
            exponent = (newScore - curScore)/volatility
            if exponent > 0 or exp(exponent) > random():
                tasks = newtasks.copy()
                curScore = newScore
            else:
                newtasks = tasks.copy()
    if prScore:
        print(prScore + str(curScore))
    return output_str(tasks)


def process(input_tuple):
    input_file = input_tuple[0]
    size = input_tuple[1]
    if size not in input_file:
        return
    input_path = 'inputs/{}/{}'.format(size, input_file)
    output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
    #if not os.path.exists(output_path):
    tasks = read_input_file(input_path)
    print(input_file[:-3] + ":\tSolving...\t" + current_process().name)
    output = solve(tasks, input_file[:-3] + ":\t")
    write_output_file(output_path, output)
    #else:
    #    pass #print(input_file[:-3] + " skipped: " + output_path + " exists!")

# Here's an example of how to run your solver.
if __name__ == '__main__':
    #TEST_SINGLE = "small/small-1.in"
    TEST_SINGLE = ""
    if TEST_SINGLE:
        input_path = 'inputs/{}'.format(TEST_SINGLE)
        output_path = 'outputs/{}.out'.format(TEST_SINGLE[:-3])
        tasks = read_input_file(input_path)
        output = solve(tasks, True)
        write_output_file(output_path, output)
    else:
        for size in sorted(os.listdir('inputs/')):
            pool = Pool()
            if size not in ['small', 'medium', 'large']:
                continue
            processed = [x[:-4] for x in os.listdir('outputs/{}/'.format(size))]
            pool.map(process, zip([input_file for input_file in os.listdir('inputs/{}/'.format(size)) if input_file[:-3] not in processed], itertools.repeat(size)))
        processOutput()
            # for input_file in os.listdir('inputs/{}/'.format(size)):
            #     if size not in input_file:
            #         continue
            #     input_path = 'inputs/{}/{}'.format(size, input_file)
            #     output_path = 'outputs/{}/{}.out'.format(size, input_file[:-3])
            #     print(input_path, output_path)
            #     tasks = read_input_file(input_path)
            #     print("Solving...")
            #     output = solve(tasks)
            #     print("Completed")
            #     write_output_file(output_path, output)
