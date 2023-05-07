for i in range(1, 11):
    DIR = "./assignment/serverFile/"
    f = open(DIR+str(i)+'.txt', 'w')
    f.write("testFile\n")
    f.write(f"number{i}\n")
    f.write("this file is for testing purpose")
    f.close()