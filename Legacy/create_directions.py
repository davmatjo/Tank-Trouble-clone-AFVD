from maths import degcos, degsin
directions = []

for i in range(0, 360, 4):
    directions.append([degcos(i), -degsin(i)])

print(directions)