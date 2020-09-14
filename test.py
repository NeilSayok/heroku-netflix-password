with open("selenium_netflix.py", 'r') as pyfi:
    l = pyfi.readlines()

with open("selenium_netflix2.py", 'w') as pyf:
    for i in l:
        pyf.write(i)
        if i != '\n':
            i = i.replace("'", '"')
            i = i.replace("\n", "")
            pyf.write(f"{(len(i) - len(i.lstrip()))*' '}print('{i}')\n")
    pyf.close()

s = 'server.starttls()'

