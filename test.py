for i in range(1, 11):
    DIR = "./tcpFileReturn/serverFile/"
    f = open(DIR+str(i)+'.txt', 'w')
    f.write(f"testFile number{i}\n")
    f.write(f"This file name is {i}.txt\n")
    f.write(f"testing")
    f.close()