# app.py
import streamlit as st
import random, json, os, uuid, time
from datetime import datetime

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(page_title="Interview Preparation Platform",
                   layout="wide", initial_sidebar_state="expanded")

# ---------------------------
# Default Question Bank placeholder
# ---------------------------
DEFAULT_BANK = {
    "Practice": {  # Aptitude Questions
        "Easy": [
            {"q": "If 5x + 3 = 18, what is x?", "a": "3", "options": ["2","3","4","5"]},
            {"q": "What is 15% of 200?", "a": "30", "options": ["20","25","30","35"]},
            {"q": "If a train travels 60 km in 1 hour, what is its speed?", "a": "60 km/h", "options": ["50 km/h","60 km/h","70 km/h","80 km/h"]},
            {"q": "Find the missing number: 2, 4, 8, 16, ?", "a": "32", "options": ["24","30","32","36"]},
            {"q": "If a:b = 2:3 and b:c = 4:5, find a:c", "a": "8:15", "options": ["2:5","8:15","4:5","6:7"]},
            {"q": "What is 25% of 240?", "a": "60", "options": ["50","55","60","65"]},
            {"q": "Solve: 8 + x = 15", "a": "7", "options": ["5","6","7","8"]},
            {"q": "If a = 3 and b = 4, find a^2 + b^2", "a": "25", "options": ["12","16","25","7"]},
            {"q": "What is the square root of 144?", "a": "12", "options": ["10","11","12","13"]},
            {"q": "Next in series: 5, 10, 15, 20, ?", "a": "25", "options": ["20","25","30","35"]},
            {"q": "If a:b = 1:2, b:c = 3:4, find a:c", "a": "3:8", "options": ["1:4","2:3","3:8","1:2"]},
            {"q": "What is 10% of 500?", "a": "50", "options": ["40","45","50","55"]},
            {"q": "If 7x = 21, what is x?", "a": "3", "options": ["2","3","4","5"]},
            {"q": "If a car travels 90 km in 1.5 hours, find speed", "a": "60 km/h", "options": ["50 km/h","55 km/h","60 km/h","65 km/h"]},
            {"q": "Sum of first 10 natural numbers?", "a": "55", "options": ["50","55","60","65"]}
        ],
        "Medium": [
            {"q": "Probability of picking red ball from bag with 5R,3B,2G?", "a": "1/2", "options": ["1/3","1/2","1/5","2/5"]},
            {"q": "Simplify: (12*3 + 18)/6", "a": "8", "options": ["6","7","8","9"]},
            {"q": "A man can do a job in 10 days, work done in 5 days?", "a": "50%", "options": ["40%","50%","60%","70%"]},
            {"q": "Next in series: 7, 14, 28, 56, ?", "a": "112", "options": ["100","110","112","120"]},
            {"q": "4 pencils cost $2, 10 pencils cost?", "a": "$5", "options": ["$4","$5","$6","$8"]},
            {"q": "Solve: 2x + 5 = 15", "a": "5", "options": ["4","5","6","7"]},
            {"q": "Sum of first 20 natural numbers?", "a": "210", "options": ["200","205","210","215"]},
            {"q": "If x^2 - 9 = 0, find x", "a": "3 or -3", "options": ["3 or -3","4 or -4","2 or -2","1 or -1"]},
            {"q": "Train 120 m long passes pole in 12 sec, speed?", "a": "36 km/h", "options": ["30 km/h","36 km/h","40 km/h","42 km/h"]},
            {"q": "If 3x - 7 = 8, x?", "a": "5", "options": ["4","5","6","7"]},
            {"q": "Next in series: 2, 6, 12, 20, ?", "a": "30", "options": ["28","30","32","34"]},
            {"q": "If a:b = 3:4, b:c = 2:3, find a:c", "a": "1:2", "options": ["1:2","2:3","3:4","3:5"]},
            {"q": "Percentage of 45 out of 60?", "a": "75%", "options": ["70%","72%","75%","80%"]},
            {"q": "If a+b=15, a-b=3, find a", "a": "9", "options": ["6","8","9","10"]},
            {"q": "A man runs 20 km in 4 hours, speed?", "a": "5 km/h", "options": ["4 km/h","5 km/h","6 km/h","7 km/h"]}
        ],
        "Hard": [
            {"q": "Solve: 3(x-2) + 4 = 19", "a": "5", "options": ["4","5","6","7"]},
            {"q": "5 men do work in 20 days, 10 men do in?", "a": "10 days", "options": ["8 days","10 days","12 days","15 days"]},
            {"q": "Train 120 m passes pole in 12 sec, speed?", "a": "36 km/h", "options": ["30 km/h","36 km/h","40 km/h","42 km/h"]},
            {"q": "Sum of first 20 natural numbers?", "a": "210", "options": ["200","210","220","230"]},
            {"q": "x^2 - 5x + 6 = 0, x?", "a": "2 or 3", "options": ["1 or 6","2 or 3","3 or 4","4 or 5"]},
            {"q": "Solve: 4x + 7 = 23", "a": "4", "options": ["4","5","6","7"]},
            {"q": "If a:b = 5:6 and b:c = 2:3, find a:c", "a": "5:9", "options": ["5:8","5:9","6:11","4:7"]},
            {"q": "If a car travels 120 km in 2 hours, speed?", "a": "60 km/h", "options": ["50 km/h","55 km/h","60 km/h","65 km/h"]},
            {"q": "Find x: 2x + 3 = 11", "a": "4", "options": ["3","4","5","6"]},
            {"q": "Next in series: 3, 6, 12, 24, ?", "a": "48", "options": ["42","44","46","48"]},
            {"q": "If a:b = 3:5 and b:c = 4:7, find a:c", "a": "12:35", "options": ["12:30","12:35","14:35","15:36"]},
            {"q": "Percentage of 80 out of 200?", "a": "40%", "options": ["35%","40%","45%","50%"]},
            {"q": "Solve: 7x - 14 = 21", "a": "5", "options": ["4","5","6","7"]},
            {"q": "Sum of first 50 natural numbers?", "a": "1275", "options": ["1250","1260","1275","1280"]},
            {"q": "If x^2 - 16 = 0, x?", "a": "4 or -4", "options": ["3 or -3","4 or -4","5 or -5","6 or -6"]}
        ]
    },
    "Mock Interview": {  # Technical + HR
        "Easy": [
            {"q": "What is Python?", "a": "Programming Language", "options":["Snake","Programming Language","Game","OS"]},
            {"q": "Explain OOP in simple terms", "a": "Object Oriented Programming", "options":["Operating Option Programming","Object Oriented Programming","Output Oriented Program","None"]},
            {"q": "What is your greatest strength?", "a": "Adaptability", "options":["Adaptability","Patience","Confidence","Skill"]},
            {"q": "Why do you want to work with us?", "a": "Company aligned with my goals", "options":["Salary","Company aligned with my goals","Peers","Location"]},
            {"q": "Difference between list and tuple?", "a": "List mutable, tuple immutable", "options":["Both mutable","Both immutable","List mutable, tuple immutable","Tuple mutable, list immutable"]},
            {"q": "What is variable in Python?", "a": "Storage to hold value", "options":["Function","Loop","Storage to hold value","Exception"]},
            {"q": "What is a function?", "a": "Block of code performing task", "options":["Variable","Block of code performing task","Loop","Class"]},
            {"q": "What is an IDE?", "a": "Integrated Development Environment", "options":["Interpreter","Compiler","Integrated Development Environment","None"]},
            {"q": "What is a list in Python?", "a": "Mutable collection", "options":["Immutable collection","Mutable collection","Tuple","Set"]},
            {"q": "What is a tuple in Python?", "a": "Immutable collection", "options":["Mutable collection","Immutable collection","List","Set"]},
            {"q": "What is a loop?", "a": "Repeating block of code", "options":["Conditional block","Repeating block of code","Function","Class"]},
            {"q": "Difference between break and continue?", "a": "Break exits loop, continue skips iteration", "options":["Break skips iteration","Break exits loop, continue skips iteration","Both same","None"]},
            {"q": "What is string slicing?", "a": "Access substring using indices", "options":["Access element","Access substring using indices","Change string","None"]},
            {"q": "What is if-else?", "a": "Conditional statement", "options":["Loop","Conditional statement","Function","Exception"]},
            {"q": "What is inheritance?", "a": "Child class derives parent properties", "options":["Parent inherits child","Child class derives parent properties","No inheritance","Multiple inheritance"]}
        ],
        "Medium": [
            {"q": "Explain inheritance in OOP", "a": "Child inherits parent properties", "options":["Parent inherits child","Child inherits parent properties","No inheritance","Multiple inheritance only"]},
            {"q": "What is recursion?", "a": "Function calling itself", "options":["Looping","Function calling itself","If else logic","None"]},
            {"q": "Describe a challenging situation and resolution", "a": "Explain experience", "options":["Avoided","Explained experience","Ignored","Delegated"]},
            {"q": "Difference between stack and queue", "a": "Stack LIFO, Queue FIFO", "options":["Both FIFO","Stack FIFO, Queue LIFO","Stack LIFO, Queue FIFO","Both LIFO"]},
            {"q": "Explain Python decorators", "a": "Function modifying other function", "options":["Decorator class","Function modifying other function","Variable","None"]},
            {"q": "Explain Python generators", "a": "Yield values one at a time", "options":["Return all","Yield values one at a time","Create function","Loop"]},
            {"q": "What is exception handling?", "a": "Catch runtime errors", "options":["Compile error","Catch runtime errors","Loop error","Variable error"]},
            {"q": "Explain Python modules", "a": "Files containing Python code", "options":["Files containing Python code","Function","Class","Loop"]},
            {"q": "Explain pass statement", "a": "Do nothing placeholder", "options":["Skip","Do nothing placeholder","Break loop","Continue"]},
            {"q": "What is list comprehension?", "a": "Create list in one line", "options":["Loop","Function","Create list in one line","Class"]},
            {"q": "What is map() function?", "a": "Apply function to all items", "options":["Loop","Apply function to all items","Conditional","Exception"]},
            {"q": "Explain filter() function", "a": "Filter items based on condition", "options":["Loop","Filter items based on condition","Change value","None"]},
            {"q": "Explain Python lambda", "a": "Anonymous function", "options":["Named function","Anonymous function","Class","Variable"]},
            {"q": "Explain Python set", "a": "Unordered unique elements", "options":["Ordered duplicate","Unordered unique elements","Mutable list","Tuple"]},
            {"q": "What is Python dictionary?", "a": "Key-value pairs", "options":["List","Tuple","Key-value pairs","Set"]}
        ],
        "Hard": [
            {"q": "Explain multithreading vs multiprocessing", "a": "Threads share memory; processes don't", "options":["Threads separate memory","Threads share memory; processes don't","Processes share memory","Both same"]},
            {"q": "Write Python code to check palindrome", "a": "s==s[::-1]", "options":["s=s[::-1]","s==s[::-1]","s!=s[::-1]","None"]},
            {"q": "Tell about a conflict at work and resolution", "a": "Explain scenario", "options":["Ignored","Explained scenario","Complained","Left job"]},
            {"q": "Explain Python GIL", "a": "Global Interpreter Lock", "options":["Global Instance Loop","Global Interpreter Lock","Global Index List","None"]},
            {"q": "What motivates you?", "a": "Growth and learning", "options":["Money","Growth and learning","Recognition","Peers"]},
            {"q": "Explain Python context manager", "a": "Manage resources with with", "options":["Loop","Manage resources with with","Function","Class"]},
            {"q": "Explain Python metaclass", "a": "Class of a class", "options":["Class instance","Class of a class","Loop","Function"]},
            {"q": "Explain Python descriptors", "a": "Manage attribute access", "options":["Manage attribute access","Loop","Function","Class"]},
            {"q": "Explain monkey patching", "a": "Modify class at runtime", "options":["Static change","Modify class at runtime","Delete class","None"]},
            {"q": "Explain Python MRO", "a": "Method resolution order", "options":["Memory order","Method resolution order","Loop order","Class order"]},
            {"q": "Explain Python async/await", "a": "Asynchronous programming", "options":["Synchronous","Asynchronous programming","Threading","Loop"]},
            {"q": "Explain Python property", "a": "Access methods like attribute", "options":["Attribute","Access methods like attribute","Function","Class"]},
            {"q": "Explain Python iterator", "a": "Object for iteration", "options":["Function","Object for iteration","Class","Loop"]},
            {"q": "Explain Python comprehension set", "a": "Create set in one line", "options":["Loop","Create set in one line","Class","Function"]},
            {"q": "Explain Python weakref", "a": "Reference that doesn't increase ref count", "options":["Strong reference","Reference that doesn't increase ref count","Loop","None"]}
        ]
    },
    "MCQ Quiz": {  # Programming/General MCQs
        "Easy": [
            {"q": "Which language is used for AI?", "a": "Python", "options":["Python","C","Java","HTML"]},
            {"q": "HTML stands for?", "a": "HyperText Markup Language", "options":["HyperText Markup Language","HighText Machine Language","Hyper Trainer Marking Language","None"]},
            {"q": "CSS is used for?", "a": "Styling web pages", "options":["Functionality","Database","Styling web pages","Backend"]},
            {"q": "Which is mutable in Python?", "a": "List", "options":["Tuple","String","List","Integer"]},
            {"q": "Which is immutable?", "a": "Tuple", "options":["List","Tuple","Set","Dictionary"]},
            {"q": "Python extension file?", "a": ".py", "options":[".java",".py",".txt",".exe"]},
            {"q": "Java is ___ typed?", "a": "Statically", "options":["Dynamically","Statically","Weakly","None"]},
            {"q": "Python function keyword?", "a": "def", "options":["function","def","func","declare"]},
            {"q": "Which loop runs at least once?", "a": "do-while", "options":["for","while","do-while","None"]},
            {"q": "Python comment symbol?", "a": "#", "options":["//","#","/*","$"]},
            {"q": "Which is used to store key-value?", "a": "Dictionary", "options":["List","Tuple","Dictionary","Set"]},
            {"q": "Python boolean values?", "a": "True/False", "options":["Yes/No","1/0","True/False","On/Off"]},
            {"q": "Which operator is for exponent?", "a": "**", "options":["^","*","**","%"]},
            {"q": "Which keyword exits a loop?", "a": "break", "options":["exit","break","continue","pass"]},
            {"q": "Python package installer?", "a": "pip", "options":["npm","pip","apt","yum"]}
        ],
        "Medium": [
            {"q": "What does len() do in Python?", "a": "Returns length", "options":["Returns max","Returns length","Returns value","None"]},
            {"q": "Difference between list and set?", "a": "Set unique, list duplicates", "options":["Both same","Set unique, list duplicates","List unique, set duplicates","None"]},
            {"q": "Python multiple inheritance supported?", "a": "Yes", "options":["No","Yes","Partially","Depends"]},
            {"q": "What is pickling?", "a": "Serialize object", "options":["Deserialize object","Serialize object","Copy object","Delete object"]},
            {"q": "What is slicing in Python?", "a": "Extract subset", "options":["Add elements","Extract subset","Delete elements","None"]},
            {"q": "Python dictionary keys must be?", "a": "Immutable", "options":["Mutable","Immutable","String only","Integer only"]},
            {"q": "What is PEP8?", "a": "Python style guide", "options":["Python guide","Python style guide","Python library","Framework"]},
            {"q": "Python function returning nothing?", "a": "None", "options":["0","None","Null","Empty"]},
            {"q": "Difference between == and is?", "a": "== compares value, is compares object", "options":["== compares object, is value","== compares value, is object","Same","None"]},
            {"q": "Python module vs package?", "a": "Package contains modules", "options":["Module contains packages","Package contains modules","Both same","None"]},
            {"q": "What is Python virtual environment?", "a": "Isolated environment", "options":["Global environment","Isolated environment","Memory space","Interpreter"]},
            {"q": "Python map() returns?", "a": "Iterator", "options":["List","Set","Iterator","Dictionary"]},
            {"q": "Python lambda can have?", "a": "Single expression", "options":["Multiple expressions","Single expression","No expression","Loop"]},
            {"q": "Difference between shallow & deep copy?", "a": "Deep copies nested objects", "options":["Shallow copies nested","Deep copies nested","Both same","None"]},
            {"q": "Python with statement?", "a": "Context manager", "options":["Function","Context manager","Class","Exception"]}
        ],
        "Hard": [
            {"q": "Explain Python metaclass", "a": "Class of a class", "options":["Instance","Class of a class","Function","Loop"]},
            {"q": "Difference between classmethod and staticmethod?", "a": "Classmethod takes cls, staticmethod takes none", "options":["Both take self","Both take cls","Classmethod takes cls, staticmethod takes none","None"]},
            {"q": "Explain Python descriptor", "a": "Manage attribute access", "options":["Function","Manage attribute access","Loop","Class"]},
            {"q": "Python GIL stands for?", "a": "Global Interpreter Lock", "options":["Global Instance Lock","Global Interpreter Lock","Global Index List","None"]},
            {"q": "Explain Python async/await", "a": "Asynchronous programming", "options":["Synchronous","Asynchronous programming","Threading","Loop"]},
            {"q": "Difference between multiprocessing & threading?", "a": "Processes separate memory, threads share memory", "options":["Both share memory","Processes separate memory, threads share memory","Both separate","None"]},
            {"q": "Python weakref usage?", "a": "Reference without increasing ref count", "options":["Strong reference","Reference without increasing ref count","Loop","Class"]},
            {"q": "Explain Python contextlib", "a": "Utilities for context managers", "options":["Function","Utilities for context managers","Class","Loop"]},
            {"q": "Explain Python __slots__", "a": "Restrict attributes", "options":["Allow all attributes","Restrict attributes","None","Loop"]},
            {"q": "Python property decorator?", "a": "Access methods like attribute", "options":["Loop","Access methods like attribute","Class","Function"]},
            {"q": "Difference between deepcopy & copy?", "a": "Deepcopy copies nested objects", "options":["Shallow copies nested","Deepcopy copies nested objects","Same","None"]},
            {"q": "Explain Python importlib", "a": "Import modules programmatically", "options":["Function","Import modules programmatically","Class","Loop"]},
            {"q": "Python memoryview usage?", "a": "Access buffer without copying", "options":["Copy buffer","Access buffer without copying","Loop","Function"]},
            {"q": "Explain Python functools.partial", "a": "Fix some function arguments", "options":["Loop","Fix some function arguments","Class","Decorator"]},
            {"q": "Python dataclass usage?", "a": "Simplify class creation", "options":["Loop","Simplify class creation","Function","Module"]}
        ]
    },
        "Pseudocode": {  # Pseudocode questions
        "Easy": [
            {"q": "Write pseudocode to find max of two numbers", "a": "If a>b then max=a else max=b", "options":["max=a+b","If a>b then max=a else max=b","max=a*b","None"]},
            {"q": "Print numbers 1 to 10", "a": "For i=1 to 10 print i", "options":["For i=1 to 10 print i","Print 1 to 10","Loop i print i","None"]},
            {"q": "Check if number is even", "a": "If n mod 2 = 0 then even else odd", "options":["If n%2=0 then even else odd","n%2==1 then odd","Check n/2","None"]},
            {"q": "Calculate factorial", "a": "fact=1 For i=1 to n fact=fact*i", "options":["fact=1 For i=1 to n fact=fact*i","fact=n!","Loop i multiply","None"]},
            {"q": "Sum of first n numbers", "a": "sum=0 For i=1 to n sum=sum+i", "options":["sum=0 For i=1 to n sum=sum+i","sum=n*(n+1)/2","Loop sum i","None"]},
            {"q": "Find smallest in array", "a": "min=a[0] For each element if element<min min=element", "options":["Loop check","min=a[0] For each element if element<min min=element","Sort array","None"]},
            {"q": "Swap two numbers", "a": "temp=a a=b b=temp", "options":["temp=a a=b b=temp","a,b=b,a","swap(a,b)","None"]},
            {"q": "Check prime number", "a": "If n<2 not prime For i=2 to n-1 if n%i=0 not prime else prime", "options":["Check manually","Use formula","If n<2 not prime For i=2 to n-1 if n%i=0 not prime else prime","None"]},
            {"q": "Reverse a string", "a": "For i=length downto 1 print char[i]", "options":["For i=length downto 1 print char[i]","Reverse manually","Loop i print","None"]},
            {"q": "Find average of numbers", "a": "sum=0 For each num sum+=num avg=sum/n", "options":["sum=0 For each num sum+=num avg=sum/n","avg=sum/len","Loop sum avg","None"]},
            {"q": "Check leap year", "a": "If year divisible by 4 and (not divisible by 100 or divisible by 400) then leap", "options":["Check divisible 4","Use library","If year divisible by 4 and (not divisible by 100 or divisible by 400) then leap","None"]},
            {"q": "Count digits in number", "a": "count=0 while n>0 n=n/10 count++", "options":["count=0 while n>0 n=n/10 count++","Convert to string","Loop digits","None"]},
            {"q": "Print multiplication table", "a": "For i=1 to 10 print n*i", "options":["For i=1 to 10 print n*i","Loop multiply","Print n*i","None"]},
            {"q": "Check palindrome", "a": "Reverse string compare with original", "options":["Reverse string compare with original","Loop compare","Check manually","None"]},
            {"q": "Find power a^b", "a": "result=1 For i=1 to b result*=a", "options":["result=1 For i=1 to b result*=a","Use pow","Loop multiply","None"]}
        ],
        "Medium": [
            {"q": "Sort array using bubble sort", "a": "For i=1 to n For j=1 to n-i if a[j]>a[j+1] swap", "options":["Bubble sort logic","For i=1 to n For j=1 to n-i if a[j]>a[j+1] swap","Sort manually","None"]},
            {"q": "Find GCD of two numbers", "a": "While b!=0 t=b b=a%b a=t return a", "options":["Euclid","While b!=0 t=b b=a%b a=t return a","Loop subtract","None"]},
            {"q": "Binary search in array", "a": "low=0 high=n-1 while low<=high mid=(low+high)/2 check arr[mid]", "options":["Binary search logic","low=0 high=n-1 while low<=high mid=(low+high)/2 check arr[mid]","Linear search","None"]},
            {"q": "Find second largest element", "a": "max1=max2=-inf for each element update max1,max2", "options":["Sort array","Use heap","max1=max2=-inf for each element update max1,max2","None"]},
            {"q": "Remove duplicates from array", "a": "Use hash or set to track elements", "options":["Sort and check","Use hash or set to track elements","Loop check","None"]},
            {"q": "Check armstrong number", "a": "Sum cubes of digits compare with number", "options":["Loop sum","Sum cubes of digits compare with number","Check formula","None"]},
            {"q": "Transpose matrix", "a": "For i,j swap arr[i][j] with arr[j][i]", "options":["Loop swap","For i,j swap arr[i][j] with arr[j][i]","Use library","None"]},
            {"q": "Find missing number in 1..n", "a": "Sum formula or XOR method", "options":["Sum formula or XOR method","Loop check","Sort then check","None"]},
            {"q": "Reverse linked list", "a": "Iterate and reverse pointers", "options":["Recursive","Iterate and reverse pointers","Swap values","None"]},
            {"q": "Detect cycle in linked list", "a": "Floyd's cycle detection", "options":["Hash set","Floyd's cycle detection","Loop check","None"]},
            {"q": "Count vowels in string", "a": "Iterate and count a,e,i,o,u", "options":["Use regex","Iterate and count a,e,i,o,u","Loop check","None"]},
            {"q": "Find intersection of two arrays", "a": "Use set intersection", "options":["Nested loop","Use set intersection","Sort and compare","None"]},
            {"q": "Find missing element in array", "a": "Use XOR or sum", "options":["Sort","Use XOR or sum","Loop check","None"]},
            {"q": "Find leader elements in array", "a": "Scan from right track max", "options":["Nested loop","Scan from right track max","Sort array","None"]},
            {"q": "Find longest common prefix", "a": "Compare char by char across strings", "options":["Use trie","Compare char by char across strings","Sort strings","None"]}
        ],
        "Hard": [
            {"q": "Implement merge sort", "a": "Divide, merge recursively", "options":["Divide, merge recursively","Quick sort","Bubble sort","None"]},
            {"q": "Implement quicksort", "a": "Partition and recursive sort", "options":["Partition and recursive sort","Merge sort","Heap sort","None"]},
            {"q": "Find shortest path in graph", "a": "Dijkstra or BFS", "options":["DFS","Dijkstra or BFS","Greedy","None"]},
            {"q": "Detect cycle in graph", "a": "DFS with visited", "options":["DFS with visited","BFS","Union-find","None"]},
            {"q": "Topological sort", "a": "DFS post-order or Kahn's", "options":["DFS post-order or Kahn's","BFS","Sort","None"]},
            {"q": "Implement LRU cache", "a": "Use linked list+hashmap", "options":["Linked list only","Use linked list+hashmap","Array","None"]},
            {"q": "Implement trie insert/search", "a": "Node children and recursive insert/search", "options":["Recursive insert/search","Node children and recursive insert/search","Array","None"]},
            {"q": "Find longest increasing subsequence", "a": "DP approach", "options":["Greedy","DP approach","Recursion","None"]},
            {"q": "Knapsack 0/1 problem", "a": "DP table solution", "options":["Greedy","DP table solution","Recursive","None"]},
            {"q": "Word ladder shortest path", "a": "BFS approach", "options":["DFS","BFS approach","DP","None"]},
            {"q": "Edit distance between strings", "a": "DP table computation", "options":["Recursion","DP table computation","Greedy","None"]},
            {"q": "Median of stream", "a": "Use two heaps", "options":["Sort stream","Use two heaps","Queue","None"]},
            {"q": "Serialize/deserialize binary tree", "a": "Preorder traversal with null markers", "options":["Inorder","Preorder traversal with null markers","Postorder","None"]},
            {"q": "Graph coloring problem", "a": "Backtracking approach", "options":["Greedy","Backtracking approach","DP","None"]},
            {"q": "Maximum flow problem", "a": "Ford-Fulkerson method", "options":["Greedy","Ford-Fulkerson method","DP","None"]}
        ]
     }   
}
QUESTION_BANK = DEFAULT_BANK
if os.path.exists("question_bank.json"):
    try:
        with open("question_bank.json", "r", encoding="utf-8") as f:
            QUESTION_BANK = json.load(f)
    except Exception:
        QUESTION_BANK = DEFAULT_BANK

# ---------------------------
# History helpers
# ---------------------------
HISTORY_FILE = "history.json"

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, default=str)

def append_history(record):
    h = load_history()
    h.append(record)
    save_history(h)

# ---------------------------
# Utility helpers
# ---------------------------
def normalize_text(x):
    if x is None: return ""
    return str(x).strip().casefold()

def is_correct(user_ans, correct_ans):
    return normalize_text(user_ans) == normalize_text(correct_ans)

# ---------------------------
# CSS for UI
# ---------------------------
st.markdown("""
<style>
.stButton>button {
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 16px;
  background: linear-gradient(90deg,#4b6cb7,#182848);
  color: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.q-card {
  background: #f7fbff;
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.stRadio > div { padding: 6px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar instructions
# ---------------------------
with st.sidebar:
    st.header("📝 Instructions")
    st.write("""
- Select a section and difficulty.
- Click **Start Test** to begin.
- Navigate using **Prev / Next**.
- Click **Save Answer** to auto-save.
- Timer runs automatically; test will auto-submit when time is up.
- Do not refresh the page during a test.
    """)

# ---------------------------
# Header & tagline
# ---------------------------
st.markdown("<h1 style='text-align:center;color:#0b4f6c'>Interview Preparation Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:#0b4f6c'>Practice, Mock Interviews, MCQ Quizzes and Pseudocode exercises — fast and clean UI</h4>", unsafe_allow_html=True)
st.write("---")

# ---------------------------
# Tabs
# ---------------------------
tabs = st.tabs(["🧠 Practice", "🎤 Mock Interview", "📝 MCQ Quiz",
                "💡 Pseudocode", "📈 Results", "📊 Analytics", "🕓 History"])
tab_names = ["Practice", "Mock Interview", "MCQ Quiz", "Pseudocode", "Results", "Analytics", "History"]

# ---------------------------
# Session state
# ---------------------------
if "exam" not in st.session_state:
    st.session_state.exam = None
if "active_section" not in st.session_state:
    st.session_state.active_section = None

# ---------------------------
# Start exam function
# ---------------------------
def start_exam(section, difficulty, count, total_time_minutes=30):
    qs_pool = QUESTION_BANK.get(section, {}).get(difficulty, []).copy()
    if not qs_pool:
        st.warning("No questions available for chosen section/difficulty.")
        return
    random.shuffle(qs_pool)
    qs = qs_pool[:count] if len(qs_pool) >= count else (qs_pool * ((count // len(qs_pool)) + 1))[:count]
    st.session_state.exam = {
        "section": section,
        "difficulty": difficulty,
        "qs": qs,
        "answers": ["" for _ in qs],
        "idx": 0,
        "start_time": time.time(),
        "duration": int(total_time_minutes * 60)
    }
    st.session_state.active_section = section
    st.rerun()

# ---------------------------
# Auto-refresh helper
# ---------------------------
def auto_refresh(seconds=1):
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    now = time.time()
    if now - st.session_state.last_refresh >= seconds:
        st.session_state.last_refresh = now
        st.experimental_rerun()

# ---------------------------
# Render section tabs (Practice / Mock / MCQ / Pseudocode)
# ---------------------------
def render_section_ui(section, tab_index):
    with tabs[tab_index]:
        st.header(f"{section}")
        levels = list(QUESTION_BANK.get(section, {}).keys())
        if not levels:
            st.info("No levels found for this section.")
            return
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            level = st.selectbox("Difficulty", levels, key=f"{section}_level")
        with col2:
            max_q = len(QUESTION_BANK.get(section, {}).get(level, []))
            max_q = max(1, max_q)
            count = st.slider("Number of Questions", 1, min(30, max_q), min(10, max_q), key=f"{section}_count")
        with col3:
            start_btn = st.button("▶ Start Test", key=f"{section}_start")
        st.write("---")
        st.write("Tips: Use the navigation buttons during the test. Do not refresh the page while an attempt is active.")
        if start_btn:
            start_exam(section, level, count, total_time_minutes=30)

for sec, idx in zip(tab_names[:4], range(4)):
    render_section_ui(sec, idx)

# ---------------------------
# Results tab
# ---------------------------
with tabs[4]:
    st.header("📈 Recent Results")
    hist = load_history()
    if not hist:
        st.info("No results yet. Take a test to see results here.")
    else:
        for rec in hist[-10:][::-1]:
            sec = rec.get("section","-")
            diff = rec.get("difficulty","-")
            score = rec.get("score",0)
            ts = rec.get("timestamp","-")
            st.markdown(f"**{sec}** — {diff} | Score: **{score}** | Time: {ts}")
            if st.button(f"View details {rec.get('id')}", key=f"view_{rec.get('id')}"):
                for d in rec.get("details", []):
                    st.write(f"- Q: {d.get('q','-')} | Ans: {d.get('selected','-')} | Correct: {d.get('correct','-')} | Score: {d.get('score',0)}")

# ---------------------------
# Analytics tab
# ---------------------------
with tabs[5]:
    st.header("📊 Analytics")
    hist = load_history()
    if not hist:
        st.info("No data to analyze yet.")
    else:
        from collections import defaultdict
        agg = defaultdict(list)
        for r in hist:
            score = r.get("score")
            if score is not None:
                agg[r.get("section","-")].append(score)
        cols = st.columns(len(agg))
        for c, (sec, scores) in zip(cols, agg.items()):
            with c:
                avg = sum(scores)/len(scores) if scores else 0
                st.metric(label=sec, value=f"{avg:.1f}")

# ---------------------------
# History tab
# ---------------------------
with tabs[6]:
    st.header("🕓 Full History")
    h = load_history()
    if not h:
        st.info("No attempts recorded.")
    else:
        for rec in h[::-1]:
            sec = rec.get("section","-")
            diff = rec.get("difficulty","-")
            score = rec.get("score",0)
            ts = rec.get("timestamp","-")
            st.markdown(f"**{sec}** — {diff} | Score: **{score}** | {ts}")

# ---------------------------
# Exam rendering
# ---------------------------
if st.session_state.exam:
    auto_refresh(1)  # live refresh
    ex = st.session_state.exam

    # Exam card
    st.markdown(f"<div style='padding:10px;border-radius:8px;background:#eef7ff'><b>Exam in progress:</b> {ex['section']} — {ex['difficulty']}</div>", unsafe_allow_html=True)

    # Timer
    elapsed = int(time.time() - ex["start_time"])
    remaining = max(ex["duration"] - elapsed, 0)
    m, s = divmod(remaining, 60)
    st.markdown(f"⏱ Time left: **{m:02}:{s:02}**")
    progress_val = min(1.0, (elapsed / ex["duration"]) if ex["duration"] > 0 else 0)
    st.progress(progress_val)

    # Auto-submit when time's up
    if remaining == 0:
        st.warning("Time's up — auto-submitting your answers.")
        should_submit = True
    else:
        should_submit = False

    # Question
    idx = ex["idx"]
    q = ex["qs"][idx]
    st.markdown(f"<div class='q-card'><b>Q{idx+1}. {q['q']}</b></div>", unsafe_allow_html=True)

    # Options or text answer
    user_key = f"answer_{idx}"
    if "options" in q and q["options"]:
        choice = st.radio("Choose an option:", q["options"], index=(q["options"].index(ex["answers"][idx]) if ex["answers"][idx] in q["options"] else 0), key=user_key)
        ex["answers"][idx] = choice
    else:
        ans = st.text_area("Your answer:", value=ex["answers"][idx], key=user_key, height=140)
        ex["answers"][idx] = ans

    # Navigation
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        if st.button("⬅ Previous"):
            if idx > 0:
                ex["idx"] -= 1
                st.session_state.exam = ex
                st.rerun()
    with c2:
        if st.button("Next ➡"):
            if idx < len(ex["qs"]) - 1:
                ex["idx"] += 1
                st.session_state.exam = ex
                st.rerun()
    with c3:
        if st.button("💾 Save Answer"):
            st.success("Answer saved ✅")
    with c4:
        if st.button("🏁 Submit Test"):
            should_submit = True

    if should_submit:
        correct_count = 0
        details = []
        for i_q, qobj in enumerate(ex["qs"]):
            user_ans = ex["answers"][i_q]
            correct_ans = qobj.get("a", "")
            correct = is_correct(user_ans, correct_ans)
            details.append({
                "q": qobj.get("q"),
                "selected": user_ans,
                "correct": correct_ans,
                "score": 1 if correct else 0
            })
            if correct:
                correct_count += 1
        score = correct_count
        rec = {
            "id": str(uuid.uuid4()),
            "section": ex["section"],
            "difficulty": ex["difficulty"],
            "timestamp": datetime.utcnow().isoformat(),
            "score": score,
            "details": details
        }
        append_history(rec)
        st.success(f"Submitted ✅ — Score: {score} / {len(ex['qs'])}")
        if score == len(ex['qs']):
            st.balloons()
        st.session_state.exam = None
        st.rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align:center;padding:8px;color:#0b4f6c;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
