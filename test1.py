data = "e\\ndsfsdafas\\n."
data = data.replace("\\n", '\n')
lines = data.split("\n")
for line in lines:
    print(line)