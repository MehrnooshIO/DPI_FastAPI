courseDetails = [
    {'field1': 'value1'},
    {'field2': 'value2'}
]

new = []

for c in courseDetails:
    temp = list(c.items())
    k = temp[0][0]
    v = temp[0][1]
    new.append((k, v))


print(new)