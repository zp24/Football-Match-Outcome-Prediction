'testing'
'test123'
myList = ['one', 'six','ten']
str = "one two three four five"
if any(x in str for x in myList):
    print (f"Found a match{str}")
else:
    print ("Not a match")