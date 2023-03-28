for i in range(1, 11):
    DIR = "./fileReturn/serverFile/"
    f = open(DIR+str(i)+'.txt', 'w')
    f.write(f"testFile number{i}")
    f.close()