

filename = '../stoke/examples/montmul_from_fxn_dot_s.log'

i = 0
lines = []
with open(filename) as f:
    for line in f:
        if line.startswith('[['):
            if i == 1:
                break
            i += 1
        lines.append(line)

print(len(lines))

with open('montmul.log', 'w') as f:
    for line in lines:
        f.write(line)

