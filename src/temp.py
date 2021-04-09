with open('temp.txt') as f:
    text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i][:-1]
    print(set(text))