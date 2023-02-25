import numpy as np

def generate_pdf(event_list):
    'Probability Density Funtion (PDF), for condensing transition tables'
    events, counts = np.unique(event_list, return_counts=True, axis=0)

    # Tuples can be used for high dimensionality sequences, but for
    # now it just breaks up my chord strings which I don't like...
    # events=[tuple(x) for x in events]

    pdf=counts/sum(counts)
    return events, pdf

def select_event_from_pdf (events, pdf):
    'Given the next available events and their probabilities, choose one'
    event_indexes=range(len(events))
    choice = events[np.random.choice(event_indexes, 1, p=pdf)[0]]
    # print(f'choice: {choice}')
    return choice