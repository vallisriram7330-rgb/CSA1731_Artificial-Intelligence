rooms={"A":"Dirty","B":"Dirty"}
location="A"; steps=0
while "Dirty" in rooms.values():
    print("Location:",location,"| Status:",rooms)
    if rooms[location]=="Dirty":
        rooms[location]="Clean"; print("Action: Suck")
    else:
        location="B" if location=="A" else "A"
        print("Action: Move")
    steps+=1
print("Final status:",rooms)
print("Total actions:",steps)


Output:
Location: A | Status: {'A': 'Dirty', 'B': 'Dirty'}
Action: Suck
Location: A | Status: {'A': 'Clean', 'B': 'Dirty'}
Action: Move
Location: B | Status: {'A': 'Clean', 'B': 'Dirty'}
Action: Suck
Final status: {'A': 'Clean', 'B': 'Clean'}
Total actions: 3
