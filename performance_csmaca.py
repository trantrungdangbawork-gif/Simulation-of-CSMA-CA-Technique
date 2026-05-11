import matplotlib.pyplot as plt

filename = 'dactuyen.txt'

V = []
I = []

with open(filename, 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()

    # bỏ header
    if line.startswith('vc') or line == '':
        continue

    parts = line.split()

    if len(parts) == 2:
        try:
            v = float(parts[0])
            i_val = float(parts[1])
            V.append(v)
            I.append(i_val)
        except:
            pass

# ===== VẼ =====
plt.figure()

plt.plot(V, I, 'r', linewidth=2)

plt.xlabel('V_CE (V)')
plt.ylabel('I_C (A)')
plt.title('Output characteristic of BJT 2N2222 (Ib = 5uA)')
plt.grid(True)

plt.legend(['Ib = 5uA'])

plt.show()