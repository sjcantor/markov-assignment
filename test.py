from markov_model import Markov_Model

model = Markov_Model()

model.train()

sum1 = 0
for i in range(100):
    sequence = model.generate(5, 2)
    for c in sequence:
        sum1 += c[1]
avg1 = sum1 / float(500)

print(avg1)

sum2 = 0
for i in range(100):
    sequence = model.generate(5, 3)
    for c in sequence:
        sum2 += c[1]
avg2 = sum2 / float(500)

print(avg2)
