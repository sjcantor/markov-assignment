from markov_model import Markov_Model

model = Markov_Model()

model.train()

sequence = model.generate(8)

print(f'sequence: {sequence}')