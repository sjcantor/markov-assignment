import numpy as np
import random

from markov_utils import *

# Chord notation:
# * Chords are assumed to be major unless specified with 'm'
# * Extensions are assumed to be flat 7 unless 'maj' is used
training_data = ['C', 'E7', 'F', 'C', 'Dm7', 'G', 'C', 'C',
                 'F', 'E7', 'Am', 'Gm', 'C7', 'F', 'Em', 'Dm7', 'G7', 'C']


class Markov_Model:
    def __init__(self):
        self.trained_pdf = None

    def train(self, input_seq=training_data):
        'Mostly from the colab, creates "trained" PDF dictionary'
        self.observed_transitions = {}
        for i in range(len(input_seq)-1):
            if input_seq[i] in self.observed_transitions:
                self.observed_transitions[input_seq[i]].append(input_seq[i+1])
            else:
                self.observed_transitions[input_seq[i]] = [input_seq[i+1]]

        pdf_dict = {}
        for key in self.observed_transitions:
            pdf_dict[key] = [generate_pdf(self.observed_transitions[key])]

        self.trained_pdf = pdf_dict
        return pdf_dict

    def generate(self, seq_len=6):
        'Generates a sequence based on the trained PDF dictionary'

        if self.trained_pdf is None:
            print('Error: need to train markov model before generating sequnces.')
            return -1
            # exit(1)

        output_sequence = []
        now = random.choice(list(self.trained_pdf.keys()))
        output_sequence.append(now)

        for x in range(seq_len-1):
            next_events, next_pdf = self.trained_pdf[now][0]

            next = select_event_from_pdf(next_events, next_pdf)
            now = next
            output_sequence.append(now)

        return output_sequence
