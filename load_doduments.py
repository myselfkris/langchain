file=open('krish.txt','r')
data=file.read()
print(data)
# it reads the file and prints the content and closes the file
with open('krish.txt','rb') as file:
    data=file.read()  
    print(data) 

#it convets the file into a list of lines and prints the list
with open("krish.txt", "r") as file:
    lines = file.readlines()

print(lines)  