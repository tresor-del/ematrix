due_date='12 12 2344'
values = due_date.split(' ')
print(values)
print(len(values))
print(range(len(values)))
dict = []
for value in values:
    for i in range(1, len(values)):
        dict[i] = value
print(dict)
