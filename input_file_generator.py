import random
import sys
def input_generator(no_of_input,x_range_min, x_range_max, y_range_min, y_range_max):
    x_y = []
    for i in range(0,no_of_input):
        x= random.randint(x_range_min,x_range_max)
        y= random.randint(y_range_min,y_range_max)
        x_y.append((x,y))

    # print(x_y)

    try:
        file = open("inputfile.txt", "w")
    except:
        print("File open error")
        return

    try:
        file.write(str(no_of_input)+"\n")
        for id, value in enumerate(x_y,1):
            temp = str(id)+' '+str(value[0])+' '+str(value[1])
            temp = temp +'\n'
            file.writelines(temp)
        file.close()
    except:
        file.close()
        print("write error")
        return

# input_generator(50000,-5000000000,5000000000,-5000000000,5000000000)
# input_generator(1000,-500000000,500000000,-500000000,500000000)
# def main(argv):
#     input_generator(1000,-100,100,-100,100)

def main(argv):
	no_of_points = input("\n\tEnter number of inputs for file generation:")
	input_generator(int(no_of_points), -5000000000, 5000000000, -5000000000, 5000000000)

if __name__ == '__main__':
    main(sys.argv)