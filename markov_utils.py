import numpy as np
import re
import random


def generate_pdf(event_list):
    'Probability Density Funtion (PDF), for condensing transition tables'

    events, counts = np.unique(event_list, return_counts=True, axis=0)

    # Tuples can be used for high dimensionality sequences, but for
    # now it just breaks up my chord strings which I don't like...
    # events=[tuple(x) for x in events]

    pdf = counts/float(sum(counts))
    return events, pdf


def create_pdf_with_complexity(events, pdf, desired_complexity):

    closeness_arr = []
    max_score = 7

    for e in events:
        closeness = abs(int(e[1]) - desired_complexity)
        # now we need to invert this score so that a higher value in the pdf is better
        score = max_score - closeness
        score = score * 1000
        closeness_arr.append(score)

    c = [closeness_arr[i] * pdf[i] for i in range(len(pdf))]

    # normalize array
    norm = [float(i)/sum(c) for i in c]
    return norm


def select_event_from_pdf(events, pdf, desired_complexity):
    'Given the next available events and their probabilities, choose one'

    complexity_pdf = create_pdf_with_complexity(
        events, pdf, desired_complexity)

    event_indexes = range(len(events))
    complexity_pdf[-1] = 1 - np.sum(complexity_pdf[0:-1])
    choice = events[np.random.choice(event_indexes, 1, p=complexity_pdf)[0]]
    return choice


def chord_complexity(chord_str):
    '''
    Returns an int corresponding to chord complexity.
    For simplicity, complexity can be evaluated as the number of notes in the chord
    '''
    complexity = 1
    chord_extensions = re.findall('\d+', chord_str)
    for i in chord_extensions:
        num = int(i)
        if num > 7:
            # this way, 9 and 11 and 13 and so on are more complex
            complexity += int((num - 7) / 2)
        else:
            complexity += 1

    # slashes are for chords like C/E
    slashes = re.findall('\/', chord_str)
    if slashes is not None:
        complexity += 1

    return complexity


def add_complexity_to_seq(input_seq):
    'Finds complexity and creates a tuple'
    new_seq = []

    for chord_str in input_seq:
        complexity = chord_complexity(chord_str)
        new_seq.append((chord_str, complexity))

    return new_seq
