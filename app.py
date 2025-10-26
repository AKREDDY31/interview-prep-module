import streamlit as st
import pandas as pd
import numpy as np
import json, os, uuid, random, time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

# ---- Modern page styling ----
st.set_page_config(
    page_title="Interview Preparation Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.big-title {
    text-align:center;
    color:#5612c6;
    font-weight:800;
    font-size:2.8rem;
    margin-top:24px;
    margin-bottom:8px;
    letter-spacing: 0.03em;
}
.subtitle {
    text-align:center;
    color:#444B5A;
    font-size:1.2rem;
    margin-bottom:22px;
}
.cardy {
    background: linear-gradient(120deg,#f3f5fa 60%, #e4e6fb 100%);
    border-left: 6px solid #5b21b6;
    border-radius: 16px;
    box-shadow: 0 2px 18px #2222;
    padding: 28px 18px 18px 26px;
    margin-bottom: 26px;
}
.cardy-title {
    font-size:1.23rem;
    font-weight:800;
    color:#7c3aed;
    margin-bottom:16px;
}
.cardy-li {
    font-size:1.06rem;
    color:#333;
    margin-bottom:7px !important;
    line-height:1.57em !important;
}
@media (max-width: 800px) {
    .big-title { font-size:2rem; }
    .subtitle { font-size:1.01rem; }
    .cardy { padding: 18px 10px 12px 12px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------- Your QUESTION_BANK goes here! -------------------
# Fill/replace THIS dict and keep the rest of the code as per your requirements.
QUESTION_BANK = {
    "Practice": {
        "Aptitude": {
            "Easy": [
                {"q": "What is 15% of 200?", "a": "30"},
                {"q": "If a train travels 120 km in 3 hours, what is its average speed?", "a": "40 km/hr"},
                {"q": "What is the next number in the series: 2, 4, 6, 8, ?", "a": "10"},
                {"q": "What is 7 squared?", "a": "49"},
                {"q": "If apples cost ₹60 per dozen, what is the cost of 8 apples?", "a": "₹40"},
                {"q": "Sam has 3 pencils, 4 erasers and 2 pens. How many items in total?", "a": "9"},
                {"q": "Find the least common multiple (LCM) of 6 and 8.", "a": "24"},
                {"q": "What is ¼ of 32?", "a": "8"},
                {"q": "Solve for x: x + 5 = 12", "a": "7"},
                {"q": "If you flip a fair coin, what is the probability of heads?", "a": "0.5"},
                {"q": "What is the value of 100 ÷ 4?", "a": "25"},
                {"q": "If you double 9, what do you get?", "a": "18"},
                {"q": "How many days are there in 3 weeks?", "a": "21"},
                {"q": "Subtract 15 from 40.", "a": "25"},
                {"q": "What is 10% of 500?", "a": "50"},
            ],
            "Medium": [
                {"q":"A car travels 60 km/hr for 2.5 hours. How far does it travel?", "a":"150 km"},
                {"q":"Find the smallest prime number greater than 30.", "a":"31"},
                {"q":"If the perimeter of a square is 32 cm, what is the side length?", "a":"8 cm"},
                {"q":"Ram bought a shirt at 20% discount. If marked price was ₹800, what did he pay?", "a":"₹640"},
                {"q":"What is the value of x: 3x + 7 = 22", "a":"5"},
                {"q":"A sum of ₹900 amounts to ₹990 in 1 year at simple interest. Find the rate.", "a":"10%"},
                {"q":"In how many ways can the letters of ‘MATH’ be arranged?", "a":"24"},
                {"q":"What is the greatest common divisor (GCD) of 48 and 180?", "a":"12"},
                {"q":"A goods is sold at 25% profit for ₹250. Find cost price.", "a":"₹200"},
                {"q":"A rectangle has area 60 cm² and width 5 cm. Find its length.", "a":"12 cm"},
                {"q":"How many even numbers between 20 and 50?", "a":"15"},
                {"q":"Rahul bought 5 pens for ₹45. What's the price per pen?", "a":"₹9"},
                {"q":"What number should be divided by 5 to get 13?", "a":"65"},
                {"q":"If 5x = 2x + 27, then x = ?", "a":"9"},
                {"q":"What is the average of 8, 12, 16, and 24?", "a":"15"},
            ],
            "Hard": [
                {"q":"Find x if 2x + 3x = 45.", "a":"9"},
                {"q":"If 40% of a number is 28, what is the number?", "a":"70"},
                {"q":"If compound interest on ₹10,000 in 2 years at 10% per annum is ₹2,100, find the rate.", "a":"10%"},
                {"q":"The sum of three consecutive even numbers is 72. Find largest.", "a":"26"},
                {"q":"If a² – b² = 21, b = 2, a = ?", "a":"5"},
                {"q":"Two pipes can fill a tank in 12 hrs and 15 hrs. Together?", "a":"6.67 hrs"},
                {"q":"The difference of cubes of two numbers is 189, and the numbers differ by 3. What are the numbers?", "a":"4 and 7"},
                {"q":"Simple int. on a sum at 5% per annum for 6 years is ₹480. What is principal?", "a":"₹1,600"},
                {"q":"Square root of 7921?", "a":"89"},
                {"q":"A can finish a work in 10 days, B in 15 days. Work together?", "a":"6 days"},
                {"q":"If 0.4x + 0.32 = 1.52, x = ?", "a":"3"},
                {"q":"What is the remainder when 2^48 is divided by 7?", "a":"4"},
                {"q":"If selling price of 10 items equals cost price of 11, gain %?", "a":"10%"},
                {"q":"100 divided in ratio 2:3, shares?", "a":"40 and 60"},
                {"q":"If mean of 12, 15, 20, x is 20, find x.", "a":"33"},
            ]
        },
        "Logical Reasoning": {
            "Easy": [
                {"q": "If all cats are dogs and all dogs are lions, are all cats lions?", "a": "Yes"},
                {"q": "What comes next: 3, 6, 9, 12, ?", "a": "15"},
                {"q": "If Rita is taller than Sita, and Sita is taller than Gita, who is tallest?", "a": "Rita"},
                {"q": "If Monday is the first day, what is the third day?", "a": "Wednesday"},
                {"q": "If B=2, D=4, F=?,", "a": "6"},
                {"q": "Egg is to bird as puppy is to ____?", "a": "Dog"},
                {"q": "If 2 pencils = 10 Rs, what is cost of 1 pencil?", "a": "5 Rs"},
                {"q": "If today is Thursday, what day will it be after 3 days?", "a": "Sunday"},
                {"q": "Which is odd one: Table, Chair, Sofa, Apple", "a": "Apple"},
                {"q": "Tina was 12 years old 3 years ago. How old now?", "a": "15"},
                {"q": "OPQ:QRS::LMN:___?", "a": "NOP"},
                {"q": "12:144::14:___?", "a": "196"},
                {"q": "Sun:Day::Moon:___?", "a": "Night"},
                {"q": "What comes next: 1,4,9,16,?", "a": "25"},
                {"q": "What is the fourth letter after J?", "a": "N"},
            ],
            "Medium": [
                {"q": "If pen is called paper, paper is called ink, ink is called eraser, what do you write with?", "a":"ink"},
                {"q": "Find the next in: 2, 6, 12, 20, 30, ?", "a":"42"},
                {"q": "If South-East becomes North, what does South-West become?", "a":"East"},
                {"q": "If 4 boys can paint a wall in 6 days, how many boys for 3 days?", "a":"8"},
                {"q": "TOMATO coded as UPNBUP. Encode BANANA.", "a":"CBNBOB"},
                {"q":"Which number is missing: 7, 10, __, 22, 37, 58", "a":"15"},
                {"q":"If ALL = 18, CAT = 24. THEN DOG=?", "a":"28"},
                {"q":"Statements: All apples are red. Some red are sweet. Conclusions: 1) Some apples are sweet. 2) Some sweets are apples.", "a":"Only 1 follows"},
                {"q":"What is the mirror image of 2:45 PM?", "a":"9:15"},
                {"q":"There are five books A,B,C,D,E. D is above C, C is above A, E is below D, B is above E. Which is at the top?", "a":"B"},
                {"q":"Which will be the day on 15th August 2047?", "a":"Thursday"},
                {"q":"Sakshi is 5 years younger than Radha. If Radha is 18, what is Sakshi's age?", "a":"13"},
                {"q":"Which word cannot be formed from: 'INFORMATION'?", "a":"RATION"},
                {"q":"If 3 is coded as 9, 5 as 25, then 7=?", "a":"49"},
                {"q":"If Q=17, J=10, G=?", "a":"7"},
            ],
            "Hard": [
                {"q": "If 'orange' is written as 'mëpksf', how is 'banana' written?", "a":"dbobob"},
                {"q": "If a + b = 12, and a - b = 6, what is a and b?", "a":"a=9, b=3"},
                {"q": "A is twice as fast as B. B finishes a work in 12 days. How long for A and B together?", "a":"4 days"},
                {"q": "Which is 4th to the right of 9th from left in alphabet?", "a":"M"},
                {"q": "Sequence: 2, 6, 12, 20, ?", "a":"30"},
                {"q": "If BEAN = 17, CAKE = 18, what is DEAL?", "a":"18"},
                {"q": "Statements: No pen is book. Some books are pencils. Conclusions: 1) Some pencils are books. 2) All books are pens.", "a":"Only 1 follows"},
                {"q": "Filter the odd one: Circle, Triangle, Rectangle, Pencil", "a": "Pencil"},
                {"q": "Find X: (X+2)*3=21", "a":"5"},
                {"q": "What will be the 17th letter to the left of the 23rd letter from the left end of the English alphabet?", "a":"F"},
                {"q": "If all numbers from 1 to 300 are written, how many 2s?", "a": "120"},
                {"q": "A finishes work in 10 days, B in 15. Together in?", "a":"6"},
                {"q": "If in a certain code, TABLE is written as UBCMF, how is TEACHER written?", "a":"UFBDIFS"},
                {"q": "Mother is twice as old as son. After 10 years, she will be 10 years older. What is son's age?", "a":"10"},
                {"q": "If OIL is coded as 161225, code for INK?", "a":"14911"},
            ]
        },
        "Analytical Reasoning": {
            "Easy": [
                {"q":"If all roses are flowers, and some flowers fade, are all roses fade?", "a":"Cannot say"},
                {"q":"What comes next? 100, 97, 89, 76, ?", "a":"58"},
                {"q":"12 chocolates divided among 4 friends, how many each?", "a":"3"},
                {"q":"6 is to 35 as 7 is to ?", "a":"48"},
                {"q":"If 'circle' means 'square' and 'square' means 'triangle', then what is a four-sided figure?", "a":"Triangle"},
                {"q":"If 2 pencils cost ₹5, what do 4 pencils cost?", "a":"₹10"},
                {"q":"Add 18 and 26.", "a":"44"},
                {"q":"If a boat goes downstream at 15 km/hr and upstream at 10 km/hr, find speed of current.", "a":"2.5 km/hr"},
                {"q":"How many months have 31 days?", "a":"7"},
                {"q":"What is 1/5th of 100?", "a":"20"},
                {"q":"Find missing term: 17, ___, 19, 22, 25 (diff +3)", "a":"16"},
                {"q":"If the cost of 3 books is ₹240, find the cost of 1 book.", "a":"₹80"},
                {"q":"Which is heavier: 1kg iron, 1kg cotton, or both equal?", "a":"Both equal"},
                {"q":"If John's present age is 24, what was his age 8 years ago?", "a":"16"},
                {"q":"How many vowels in 'EXAMINATION'?", "a":"6"}
            ],
            "Medium": [
                {"q":"Ravi invests ₹10k @10% SI p.a. for 3 years. Interest?", "a":"₹3,000"},
                {"q":"If sum of ages of A and B is 42, and A is twice B, ages?", "a":"A=28, B=14"},
                {"q":"If 2:3 means 2 parts to 3, what is 2/5 as ratio?", "a":"2:5"},
                {"q":"If a car covers 240km at 60km/hr, time taken?", "a":"4 hours"},
                {"q":"Which number replaces ?: 3,7,15,31,?", "a":"63"},
                {"q":"What is 8% of 1,250?", "a":"100"},
                {"q":"If a shopkeeper sells at 8% loss on ₹600, find loss.", "a":"₹48"},
                {"q":"If 5x+3=23, x=?", "a":"4"},
                {"q":"If 4 men can build a wall in 10 days, how long for 2 men?", "a":"20 days"},
                {"q":"Which is greater: 2/3 or 3/4?", "a":"3/4"},
                {"q":"If G is taller than H but shorter than I, who is tallest?", "a":"I"},
                {"q":"Which word can't be formed: RAINBOW? (RAIN, BROW, BONE, WIN)", "a":"BONE"},
                {"q":"Find next: 2,6,12,20,?", "a":"30"},
                {"q":"If weight is 54kg after losing 6kg, what was original weight?", "a":"60kg"},
                {"q":"If 5 pens = ₹20, what is cost of 3 pens?", "a":"₹12"},
            ],
            "Hard": [
                {"q":"If triangle's area is 54cm², base 9cm, height?", "a":"12cm"},
                {"q":"In how many ways can 'LEVEL' be arranged?", "a":"30"},
                {"q":"Find HCF of 72, 96, 120.", "a":"24"},
                {"q":"If compound interest on ₹4000 in 2 years is ₹512, rate?", "a":"6%"},
                {"q":"Decode: If MODEL=OMFEM, how is DREAM?", "a":"EREBN"},
                {"q":"If 2x+3x=75, x=?", "a":"15"},
                {"q":"What is the angle sum of a pentagon?", "a":"540°"},
                {"q":"A number divided by 5 gives 8 remainder 4. Number?", "a":"44"},
                {"q":"What is speed if a man walks 120km in 5 days at 8 hrs/day?", "a":"3 km/hr"},
                {"q":"If cost of 1kg sugar is ₹37, what is the cost of 2.5kg?", "a":"₹92.5"},
                {"q":"Add smallest 4-digit and largest 3-digit number.", "a":"1999"},
                {"q":"Find digit: 57*4 divisible by 9.", "a":"2"},
                {"q":"Age of A is double that of B. If B is 25, A+B=?", "a":"75"},
                {"q":"If 2 machines make 4 toys in 2 hrs, how long for 6 toys?", "a":"3 hours"},
                {"q":"If book's price rises from ₹200 to ₹220, percentage increase?", "a":"10%"},
            ]
        }
    },












































   "MCQ Quiz": {
    "Python": {
        "Easy": [
            {"q": "What does print(2**3) output?", "options": ["5", "6", "8", "9"], "a": "8"},
            {"q": "Which of these is NOT a Python data type?", "options": ["tuple", "dict", "list", "arraylist"], "a": "arraylist"},
            {"q": "What is the output of print('Hello World'[:5])?", "options": ["Hello", "World", "Hell", "o W"], "a": "Hello"},
            {"q": "Which keyword is used to define functions?", "options": ["function", "def", "lambda", "fun"], "a": "def"},
            {"q": "Which one is a list in Python?", "options": ["(1,2,3)", "{1,2,3}", "[1,2,3]", "None"], "a": "[1,2,3]"},
            {"q": "What does len([1,2,3,4]) return?", "options": ["3", "4", "5", "Error"], "a": "4"},
            {"q": "Which is used to comment a line?", "options": ["//", "#", "<!--", "--"], "a": "#"},
            {"q": "What is output: print(type('5'))?", "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "Error"], "a": "<class 'str'>"},
            {"q": "Which is used to get input from user?", "options": ["input()", "scan()", "get()", "read()"], "a": "input()"},
            {"q": "Which operator is used for modulus?", "options": ["%", "//", "/", "^"], "a": "%"},
            {"q": "What is output: print(2+3*2)?", "options": ["10", "8", "7", "12"], "a": "8"},
            {"q": "Which keyword is used to end a loop?", "options": ["stop", "exit", "break", "leave"], "a": "break"},
            {"q": "Is Python case sensitive?", "options": ["Yes", "No", "Sometimes", "Can't Say"], "a": "Yes"},
            {"q": "What is the result of 4//3?", "options": ["1", "1.33", "1.0", "Error"], "a": "1"},
            {"q": "Which of these is a tuple?", "options": ["[1,2]", "{1,2}", "(1,2)", "None"], "a": "(1,2)"}
        ],
        "Medium": [
            {"q": "What is the result of 2 == 2.0 in Python?", "options": ["True", "False", "Error", "None"], "a": "True"},
            {"q": "Which operator is used for floor division?", "options": ["/", "//", "%", "**"], "a": "//"},
            {"q": "What type is the result of: 3/2 in Python 3?", "options":["int", "float", "bool", "None"], "a":"float"},
            {"q": "Which method removes the last element from a list?", "options":["pop()","remove()","delete()","discard()"], "a":"pop()"},
            {"q": "What is the result of bool('False')?", "options":["True","False","Error","None"], "a":"True"},
            {"q": "Which keyword is used for exception handling?", "options":["try","except","catch","all"], "a":"except"},
            {"q": "Which of these defines a dict?", "options":["[]","{}","()","//"], "a":"{}"},
            {"q": "What is output: print(0.1+0.2==0.3)?", "options":["True","False","Error","None"], "a":"False"},
            {"q": "How to declare a variable in Python?", "options": ["int x=5", "let x=5", "x=5", "x:int=5"], "a": "x=5"},
            {"q": "How to start a for loop in Python?", "options": ["for x in y:", "for (x in y)", "foreach x in y", "repeat x in y"], "a": "for x in y:"},
            {"q": "What result: 'a' + 'b'*2?", "options": ["ab", "abb", "aab", "Error"], "a": "abb"},
            {"q": "What is used to define block of statements?", "options": ["{}", "()", ":", "[]"], "a": ":"},
            {"q": "Which of these creates a set?", "options": ["{1,2,3}", "(1,2,3)", "[1,2,3]", "set[1,2,3]"], "a": "{1,2,3}"},
            {"q": "Which of the following is a valid variable?", "options": ["1var", "_var", "var-1", "var 1"], "a": "_var"},
            {"q": "What is output: print('5'+'5')?", "options": ["10", "55", "5", "Error"], "a": "55"}
        ],
        "Hard": [
            {"q": "Which method adds elements to a set?", "options": ["append()", "add()", "insert()", "extend()"], "a": "add()"},
            {"q": "Which of these statements is valid for dictionary access?", "options": ["dict->key", "dict.key", "dict['key']", "dict(key)"], "a": "dict['key']"},
            {"q": "Which concept does Python use for inheritance?", "options": ["Composition", "Polymorphism", "Classical Inheritance", "All"], "a": "Classical Inheritance"},
            {"q": "Which of these is a generator expression?", "options": ["[x for x in y]", "(x for x in y)", "{x for x in y}", "None"], "a": "(x for x in y)"},
            {"q": "Which built-in can sort a list in-place?", "options": ["sort()", "sorted()", "order()", "arrange()"], "a": "sort()"},
            {"q": "What does 'with open() as f:' ensure?", "options": ["Auto close", "Faster IO", "Thread Safety", "None"], "a": "Auto close"},
            {"q": "Which of these is NOT mutable?", "options": ["list", "set", "dict", "tuple"], "a": "tuple"},
            {"q": "What is the output: print(list(map(lambda x: x**2, [2,3])))?", "options": ["[4,9]", "[2,3]", "[6,5]", "[4,3]"], "a": "[4,9]"},
            {"q": "What is __init__?", "options":["Constructor","Method","Destructor","Class"], "a":"Constructor"},
            {"q": "Which is not a valid file mode?", "options": ["'r'", "'w'", "'x'", "'b+'"], "a": "'b+'"},
            {"q": "How to import all functions from math?", "options": ["import math.*", "import * from math", "from math import *", "import all math"], "a": "from math import *"},
            {"q": "Which method returns keys for a dict?", "options": ["keys()", "getkeys()", "dict_keys()", "list()"], "a": "keys()"},
            {"q": "Which is not an exception in Python?", "options": ["ValueError", "KeyError", "TypeError", "WrongError"], "a": "WrongError"},
            {"q": "What is output: print([i for i in range(2)])?", "options": ["[2]", "[0,1]", "[1,2]", "[0,1,2]"], "a": "[0,1]"},
            {"q": "Which operator is used for bitwise OR?", "options": ["|", "&", "^", "~"], "a": "|"}
        ]
    },
    "DBMS": {
        "Easy": [
            {"q": "Which is a primary key?", "options": ["Unique identifier", "Duplicate value", "Random key", "None"], "a": "Unique identifier"},
            {"q": "Which of these is a database?", "options": ["MS Word", "MySQL", "Excel", "Photoshop"], "a": "MySQL"},
            {"q": "What is SQL?", "options": ["A programming language", "Query language", "Markup language", "None"], "a": "Query language"},
            {"q": "Which of these is NOT a DBMS?", "options": ["Oracle", "MySQL", "Linux", "SQLite"], "a": "Linux"},
            {"q": "What does DDL stand for?", "options": ["Data Definition Language", "Data Detection Language", "Database Data Language", "None"], "a": "Data Definition Language"},
            {"q": "Which keyword retrieves data?", "options": ["SELECT", "INSERT", "DELETE", "UPDATE"], "a": "SELECT"},
            {"q": "Which uniquely identifies a record?", "options": ["Primary key", "Foreign key", "Composite key", "Candidate key"], "a": "Primary key"},
            {"q": "Which of these is a NoSQL DB?", "options": ["Postgres", "MongoDB", "Oracle", "SQLite"], "a": "MongoDB"},
            {"q": "What data type stores large text?", "options": ["CHAR", "INT", "TEXT", "FLOAT"], "a": "TEXT"},
            {"q": "Which is NOT a valid SQL command?", "options": ["SELECT", "UPDATE", "MODIFY", "DELETE"], "a": "MODIFY"},
            {"q": "Which operation combines two tables?", "options": ["JOIN", "MERGE", "UNION", "APPEND"], "a": "JOIN"},
            {"q": "Which symbol is used for wildcard in SQL LIKE?", "options": ["?", "*", "%", "$"], "a": "%"},
            {"q": "Which is NOT a constraint?", "options": ["PRIMARY KEY", "UNIQUE", "TRIGGER", "CHECK"], "a": "TRIGGER"},
            {"q": "Rows in table are called?", "options": ["Record", "Field", "Column", "Tuple"], "a": "Record"},
            {"q": "Which SQL function counts entries?", "options": ["COUNT()", "SUM()", "MAX()", "MIN()"], "a": "COUNT()"}
        ],
        "Medium": [
            {"q": "What is a foreign key?", "options": ["Unique column", "References another table", "Null value", "None"], "a": "References another table"},
            {"q": "Which of these is a DDL command?", "options": ["SELECT", "INSERT", "CREATE", "UPDATE"], "a": "CREATE"},
            {"q": "Which clause filters records?", "options": ["FROM", "WHERE", "ORDER BY", "GROUP BY"], "a":"WHERE"},
            {"q": "Which command changes table structure?", "options": ["ALERT", "ALTER", "UPDATE", "SET"], "a": "ALTER"},
            {"q": "Which is an aggregate function?", "options": ["WHERE", "SUM", "UPDATE", "LIMIT"], "a": "SUM"},
            {"q": "2NF removes which anomaly?", "options": ["Partial Dependency", "Transitive", "Insertion", "All"], "a":"Partial Dependency"},
            {"q": "What is result of Cartesian join for 3x3 tables?", "options": ["3", "6", "9", "27"], "a":"9"},
            {"q": "Which schedule is conflict serializable?", "options":["Consistent","Serializable","Random","None"],"a":"Serializable"},
            {"q": "Which is not a transaction property (ACID)?", "options":["Atomicity","Consistency","Integrity","Durability"],"a":"Integrity"},
            {"q":"What does SQL 'GRANT' do?", "options":["Insert Data","Rollback","Give Privileges","Drop Table"],"a":"Give Privileges"},
            {"q":"Which join returns matching & non-matching rows?", "options":["Inner Join","Outer Join","Cross Join","Self Join"],"a":"Outer Join"},
            {"q":"Which SQL statement renames a table?", "options":["RENAME","ALTER","MODIFY","CHANGE"],"a":"RENAME"},
            {"q":"Which index increases fetch speed?", "options":["Clustered","Unique","Hash","Bitmap"],"a":"Clustered"},
            {"q":"Which keyword is used for constraints?", "options":["CHECK","LIMIT","ALLOW","VERIFY"],"a":"CHECK"},
            {"q":"Which language is for access control in DBMS?", "options":["DCL","DML","DDL","CFL"],"a":"DCL"}
        ],
        "Hard": [
            {"q": "Which normal form removes transitive dependency?", "options": ["1NF", "2NF", "3NF", "BCNF"], "a": "3NF"},
            {"q": "Which command removes all records from a table but not structure?", "options": ["DELETE", "TRUNCATE", "DROP", "ALTER"], "a": "TRUNCATE"},
            {"q": "Which isolation level is most strict?", "options": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"], "a":"Serializable"},
            {"q": "Which of these is not a valid join?", "options": ["Full Outer Join", "Complete Join", "Left Join", "Right Join"], "a":"Complete Join"},
            {"q": "What is a deadlock?", "options": ["Transaction waits indefinitely", "Page Fault", "Long query", "Backup"], "a":"Transaction waits indefinitely"},
            {"q": "Which is not a valid SQL data type?", "options": ["DATE", "BLOB", "TEXT", "NUMERIC"], "a":"NUMERIC"},
            {"q": "Which operation is used for recursion?", "options": ["WITH", "RECURSIVE", "FOR", "LOOP"], "a":"RECURSIVE"},
            {"q": "Which property ensures transaction completes in full or not at all?", "options": ["Atomicity", "Durability", "Consistency", "Isolation"], "a":"Atomicity"},
            {"q": "What is the minimum number of superkeys for a relation with n attributes?", "options": ["n", "2^n - 1", "1", "0"], "a": "2^n - 1"},
            {"q": "Which constraint prevents null values?", "options": ["NOT NULL", "UNIQUE", "PRIMARY KEY", "FOREIGN KEY"], "a":"NOT NULL"},
            {"q": "Which schedule always avoids deadlock?", "options": ["Serial", "Parallel", "Overlapped", "Random"], "a":"Serial"},
            {"q": "Which is true about BCNF?", "options": ["Every 3NF is BCNF", "BCNF is stricter than 3NF", "No redundancy", "None"], "a":"BCNF is stricter than 3NF"},
            {"q": "Which SQL function gives difference between dates?", "options": ["DATEDIFF()", "TIMEDIF()", "FINDIFF()", "DIF()"], "a":"DATEDIFF()"},
            {"q": "How many NULLs can a unique Key have?", "options":["0","1","Multiple","None"],"a":"Multiple"},
            {"q": "Which trigger runs after data is inserted?", "options": ["AFTER INSERT", "BEFORE INSERT", "ON INSERT", "ON AFTER"], "a":"AFTER INSERT"},
            {"q": "Which log is maintained in DBMS for recovery?", "options": ["Redo", "Undo", "Transaction", "All"], "a":"All"}
        ]
    }
},








"Mock Interview": {
    "Technical": {
        "Easy": [
            {"q": "Explain OOPS concepts with real-world examples.", "a": ""},
            {"q": "What is a function? Give an example.", "a": ""},
            {"q": "Define an array and its uses.", "a": ""},
            {"q": "What is a primary key in a database?", "a": ""},
            {"q": "Explain the difference between list and tuple in Python.", "a": ""},
            {"q": "What is inheritance in OOP?", "a": ""},
            {"q": "Difference between compiler and interpreter?", "a": ""},
            {"q": "What is a variable?", "a": ""},
            {"q": "What are loops? Name types.", "a": ""},
            {"q": "How does a for loop differ from a while loop?", "a": ""},
            {"q": "What is an IDE?", "a": ""},
            {"q": "Define recursion.", "a": ""},
            {"q": "What is a class?", "a": ""},
            {"q": "Give an example of encapsulation.", "a": ""},
            {"q": "What is a constructor in OOP?", "a": ""}
        ],
        "Medium": [
            {"q": "How do you handle memory management in Python?", "a": ""},
            {"q": "Describe the OSI model.", "a": ""},
            {"q": "What is the difference between TCP and UDP?", "a": ""},
            {"q": "How do you debug a large codebase?", "a": ""},
            {"q": "Explain exception handling with examples.", "a": ""},
            {"q": "When would you use stacks over queues?", "a": ""},
            {"q": "What is normalization in databases?", "a": ""},
            {"q": "Compare merge sort vs quicksort.", "a": ""},
            {"q": "How is polymorphism useful?", "a": ""},
            {"q": "What is garbage collection?", "a": ""},
            {"q": "Explain API and its usage.", "a": ""},
            {"q": "How do you optimize slow queries?", "a": ""},
            {"q": "What is multithreading?", "a": ""},
            {"q": "Difference between process and thread.", "a": ""},
            {"q": "What are RESTful web services?", "a": ""}
        ],
        "Hard": [
            {"q": "Describe thread safety in multi-threaded applications.", "a": ""},
            {"q": "How do you resolve deadlocks in concurrent programming?", "a": ""},
            {"q": "Explain CAP theorem with examples.", "a": ""},
            {"q": "How would you design a scalable URL shortening service?", "a": ""},
            {"q": "Describe distributed systems challenges.", "a": ""},
            {"q": "Explain Big O notation of quicksort worst-case.", "a": ""},
            {"q": "Give an approach to design a cache system.", "a": ""},
            {"q": "How to prevent SQL injection?", "a": ""},
            {"q": "What are design patterns? Name two.", "a": ""},
            {"q": "How do you secure REST APIs?", "a": ""},
            {"q": "What are microservices?", "a": ""},
            {"q": "Explain eventual consistency.", "a": ""},
            {"q": "Describe dependency injection.", "a": ""},
            {"q": "What are webhooks? Where to use?", "a": ""},
            {"q": "Discuss ACID properties with examples.", "a": ""}
        ]
    },
    "HR": {
        "Easy": [
            {"q": "Why should we hire you?", "a": ""},
            {"q": "Describe yourself in three words.", "a": ""},
            {"q": "What motivates you?", "a": ""},
            {"q": "What are your strengths?", "a": ""},
            {"q": "Do you prefer team or solo work?", "a": ""},
            {"q": "Tell me about your family.", "a": ""},
            {"q": "How do you handle criticism?", "a": ""},
            {"q": "Why did you leave your last job?", "a": ""},
            {"q": "How do you respond to stress?", "a": ""},
            {"q": "What are your hobbies?", "a": ""},
            {"q": "Where do you see yourself in 5 years?", "a": ""},
            {"q": "Why this company?", "a": ""},
            {"q": "Describe your ideal work environment.", "a": ""},
            {"q": "Are you willing to relocate?", "a": ""},
            {"q": "Have you ever failed? Explain.", "a": ""}
        ],
        "Medium": [
            {"q": "Describe a challenge you faced and how you handled it.", "a": ""},
            {"q": "Tell us about a time you took initiative.", "a": ""},
            {"q": "When did you disagree with a manager? Outcome?", "a": ""},
            {"q": "What would you do if you miss a project deadline?", "a": ""},
            {"q": "How do you balance work and life?", "a": ""},
            {"q": "Describe a difficult colleague situation.", "a": ""},
            {"q": "What's your greatest accomplishment?", "a": ""},
            {"q": "How do you learn new skills?", "a": ""},
            {"q": "Describe a leadership experience.", "a": ""},
            {"q": "Tell us about a situation where you made a mistake.", "a": ""},
            {"q": "How do you prioritize your tasks?", "a": ""},
            {"q": "Give an example of when you went the extra mile.", "a": ""},
            {"q": "Describe how you adapt to change.", "a": ""},
            {"q": "How do you handle confidential information?", "a": ""},
            {"q": "How do you resolve disagreements with peers?", "a": ""}
        ],
        "Hard": [
            {"q": "How do you resolve workplace conflict?", "a": ""},
            {"q": "Describe a time you had to manage an underperforming team member.", "a": ""},
            {"q": "How would you manage an ethical dilemma?", "a": ""},
            {"q": "How would you deliver difficult feedback?", "a": ""},
            {"q": "What would you do if you encountered discrimination at work?", "a": ""},
            {"q": "Describe a time you failed as a leader.", "a": ""},
            {"q": "How would you help a team member struggling emotionally?", "a": ""},
            {"q": "What does integrity mean to you at work?", "a": ""},
            {"q": "Describe a situation where you had to support a bad company policy.", "a": ""},
            {"q": "How would you react if a friend was caught cheating at work?", "a": ""},
            {"q": "Is it ever OK to bend rules for results?", "a": ""},
            {"q": "Describe a time your ethics were tested.", "a": ""},
            {"q": "When did you take an unpopular stance for the right reason?", "a": ""},
            {"q": "How would you turn around a toxic team culture?", "a": ""},
            {"q": "What would you do if you witnessed harassment at work?", "a": ""}
        ]
    },
    "Manager": {
        "Easy": [
            {"q": "How do you manage deadlines in a team project?", "a": ""},
            {"q": "How do you schedule tasks for a team?", "a": ""},
            {"q": "How do you handle team absences?", "a": ""},
            {"q": "Describe your management style.", "a": ""},
            {"q": "How do you conduct a team meeting?", "a": ""},
            {"q": "How do you motivate your team?", "a": ""},
            {"q": "What is important in team communication?", "a": ""},
            {"q": "How do you handle performance reviews?", "a": ""},
            {"q": "How do you welcome new team members?", "a": ""},
            {"q": "How do you resolve minor disputes?", "a": ""},
            {"q": "What tools do you use to track progress?", "a": ""},
            {"q": "How do you prioritize objectives?", "a": ""},
            {"q": "How do you set goals for your team?", "a": ""},
            {"q": "How do you ensure task delegation works?", "a": ""},
            {"q": "What's your approach to conflict resolution?", "a": ""}
        ],
        "Medium": [
            {"q": "How do you delegate tasks?", "a": ""},
            {"q": "Describe a time you managed a large cross-team project.", "a": ""},
            {"q": "How do you adapt strategy when goals change?", "a": ""},
            {"q": "How do you develop your team members?", "a": ""},
            {"q": "How do you identify team strengths & weaknesses?", "a": ""},
            {"q": "Describe solving a bottleneck under deadline.", "a": ""},
            {"q": "Explain a time you improved a process.", "a": ""},
            {"q": "How do you manage remote teams?", "a": ""},
            {"q": "Describe a situation where you handled low morale.", "a": ""},
            {"q": "What criteria do you use to promote employees?", "a": ""},
            {"q": "How do you support a struggling team member?", "a": ""},
            {"q": "Explain a time you disagreed with your boss.", "a": ""},
            {"q": "How do you manage high performers differently?", "a": ""},
            {"q": "What is your hands-off vs hands-on ratio?", "a": ""},
            {"q": "How do you measure success for your team?", "a": ""}
        ],
        "Hard": [
            {"q": "How do you align a team's priorities with company goals?", "a": ""},
            {"q": "Describe handling a major project failure.", "a": ""},
            {"q": "How would you fix a persistent performance drop?", "a": ""},
            {"q": "How do you hire the best talent?", "a": ""},
            {"q": "Describe firing an underperformer.", "a": ""},
            {"q": "How do you manage bias in decision making?", "a": ""},
            {"q": "Describe turning around a demotivated team.", "a": ""},
            {"q": "How do you spot early burnout?", "a": ""},
            {"q": "What lessons did you learn from your worst project?", "a": ""},
            {"q": "How do you deal with conflicting upper management demands?", "a": ""},
            {"q": "Describe a time you changed company culture.", "a": ""},
            {"q": "How do you coach other managers?", "a": ""},
            {"q": "What's your approach to crisis management?", "a": ""},
            {"q": "How do you foster innovation in your team?", "a": ""},
            {"q": "How do you handle succession planning?", "a": ""}
        ]
    },
    "Clint": {
        "Easy": [
            {"q": "Tell us about a time you solved a tough problem quickly.", "a": ""},
            {"q": "Share one example of creative thinking.", "a": ""},
            {"q": "How do you introduce yourself to a new group?", "a": ""},
            {"q": "Describe a skill you're proud of.", "a": ""},
            {"q": "Explain a personal value you hold dear.", "a": ""},
            {"q": "When was your last group project and your role?", "a": ""},
            {"q": "How do you ask for help when stuck?", "a": ""},
            {"q": "Give an example of adapting to change.", "a": ""},
            {"q": "What do you do to build rapport quickly?", "a": ""},
            {"q": "Describe one thing you love to learn.", "a": ""},
            {"q": "Share a tip for public speaking.", "a": ""},
            {"q": "What makes you a good teammate?", "a": ""},
            {"q": "What keeps you positive under pressure?", "a": ""},
            {"q": "What's a fun memory from college or work?", "a": ""},
            {"q": "How do you make friends when new in a place?", "a": ""}
        ],
        "Medium": [
            {"q": "How would you handle a difficult client or customer?", "a": ""},
            {"q": "Describe a time you persuaded someone.", "a": ""},
            {"q": "How do you recover from public mistakes?", "a": ""},
            {"q": "When have you worked across cultures?", "a": ""},
            {"q": "Describe a time you had to apologize at work.", "a": ""},
            {"q": "How do you remain objective in disagreements?", "a": ""},
            {"q": "What do you do when you don’t know an answer?", "a": ""},
            {"q": "Describe a time you had to be assertive.", "a": ""},
            {"q": "How do you keep peace in a heated debate?", "a": ""},
            {"q": "Tell about a time you learned from a peer.", "a": ""},
            {"q": "How do you handle being left out?", "a": ""},
            {"q": "How do you listen actively?", "a": ""},
            {"q": "Give one example of improvising in a crisis.", "a": ""},
            {"q": "How do you resolve group misunderstandings?", "a": ""},
            {"q": "How do you receive tough feedback?", "a": ""}
        ],
        "Hard": [
            {"q": "Describe a time you went against group opinion and why.", "a": ""},
            {"q": "How do you challenge the status quo?", "a": ""},
            {"q": "Share a mistake that changed your world view.", "a": ""},
            {"q": "How do you deal with ethical dilemmas?", "a": ""},
            {"q": "Describe taking an unpopular stand in a team.", "a": ""},
            {"q": "How do you repair broken professional relationships?", "a": ""},
            {"q": "Explain how to give others constructive criticism.", "a": ""},
            {"q": "Describe guiding a group through uncertainty.", "a": ""},
            {"q": "How to motivate others around you facing failure?", "a": ""},
            {"q": "Share a story where you did not fit in.", "a": ""},
            {"q": "Describe a time you broke a stereotype.", "a": ""},
            {"q": "Discuss overcoming imposter syndrome.", "a": ""},
            {"q": "How have you dealt with being misjudged?", "a": ""},
            {"q": "How do you build consensus in a divided team?", "a": ""},
            {"q": "How do you inspire change in conservative groups?", "a": ""}
        ]
    }
},





"Code Runner": {
    "Easy": [
        {"q": "Write a function to return the factorial of a number n.\nTest Case 1: n=5, output=120\nTest Case 2: n=1, output=1", "a": ""},
        {"q": "Write a function to check if a number is even.\nTest Case 1: n=6, output=True\nTest Case 2: n=7, output=False", "a": ""},
        {"q": "Write code to reverse a string.\nTest Case 1: s='abc', output='cba'\nTest Case 2: s='race', output='ecar'", "a": ""},
        {"q": "Find the maximum value in a list.\nTest Case 1: arr=[2,5,1], output=5\nTest Case 2: arr=[-10,0,10], output=10", "a": ""},
        {"q": "Sum all numbers in a list.\nTest Case 1: [1,2,3], output=6\nTest Case 2: [0,5,5], output=10", "a": ""},
        {"q": "Write code to print Fibonacci series up to n terms.\nTest Case 1: n=5, output=[0,1,1,2,3]", "a": ""},
        {"q": "Return the smallest number among three.\nTest Case 1: 2,5,3 output=2\nTest Case 2: 8,1,9 output=1", "a": ""},
        {"q": "Check if a string startswith 'A'.\nTest Case 1: s='Apple', output=True\nTest Case 2: s='Banana', output=False", "a": ""},
        {"q": "Write code to count vowels in a string.\nTest Case 1: s='aeiou', output=5\nTest Case 2: s='xyz', output=0", "a": ""},
        {"q": "Return the absolute difference of two numbers.\nTest Case 1: 5,2 output=3\nTest Case 2: 2,5 output=3", "a": ""},
        {"q": "Return the square of a number.\nTest Case 1: n=3 output=9\nTest Case 2: n=-4 output=16", "a": ""},
        {"q": "Convert Celsius to Fahrenheit.\nTest Case 1: 0 -> 32\nTest Case 2: 100 -> 212", "a": ""},
        {"q": "Find sum of digits in a number.\nTest Case 1: n=123, output=6\nTest Case 2: n=49, output=13", "a": ""},
        {"q": "Find length of a list.\nTest Case 1: [1,2,3,4], output=4\nTest Case 2: [], output=0", "a": ""},
        {"q": "Return True if character is uppercase.\nTest Case 1: 'A', output=True\nTest Case 2: 'b', output=False", "a": ""}
    ],
    "Medium": [
        {"q": "Write a function to check if a string is a palindrome.\nTest Case 1: input='racecar', output=True\nTest Case 2: input='hello', output=False", "a": ""},
        {"q": "Find the second largest number in a list.\nTest: [3,1,4], output=3\n[7,5,5,4], output=5", "a": ""},
        {"q": "Count frequency of each character in a string.\nTest: 'aba', output={'a':2,'b':1}\n'abc', output={'a':1,'b':1,'c':1}", "a": ""},
        {"q": "Check if two strings are anagrams.\nTest: 'listen', 'silent' output=True\n'hello','world' output=False", "a": ""},
        {"q": "Write code to calculate GCD of two numbers.\nTest: 8,12 output=4\n18,27 output=9", "a": ""},
        {"q": "Implement binary search.\nTest: arr=[1,2,3,4], val=3 output=2\narr=[2,4,6], val=5 output=-1", "a": ""},
        {"q": "Remove duplicates from a list.\nTest: [1,2,2,3], output=[1,2,3]\n[3,3,3], output=[3]", "a": ""},
        {"q": "Write code to merge two sorted lists.\nTest: [1,3],[2,4] output=[1,2,3,4]", "a": ""},
        {"q": "Count words in a sentence.\nTest: 'hello world', output=2\n'one two three', output=3", "a": ""},
        {"q": "Implement a basic calculator for +,-,*,/.\nTest: 2,3,'+', output=5\n6,2,'/', output=3", "a": ""},
        {"q": "Return all even numbers from a list.\nTest: [1,2,3,4], output=[2,4]\n[3,5], output=[]", "a": ""},
        {"q": "Check if a given year is leap year.\nTest: 2000, True\n1900, False", "a": ""},
        {"q": "Write code to find common elements in two lists.\nTest: [1,2],[2,3] output=[2]", "a": ""},
        {"q": "Convert Roman numeral to integer.\nTest: 'IV',output=4\n'X',output=10", "a": ""},
        {"q": "Write code to flatten a nested list.\nTest: [[1,2],[3]] output=[1,2,3]", "a": ""}
    ],
    "Hard": [
        {"q": "Write a program to find the longest increasing subsequence in an array.\nTest Case 1: input=[1,2,4,3], output=3\nTest Case 2: input=[5,4,3], output=1", "a": ""},
        {"q": "Write code to solve N-Queen Problem for N=4.", "a": ""},
        {"q": "Find all unique permutations of a given string.\nTest: 'abc' output=['abc','acb','bac','bca','cab','cba']", "a": ""},
        {"q": "Implement a cache with LRU eviction.", "a": ""},
        {"q": "Find the maximum subarray sum (Kadane's Algorithm).\nTest: [-2,1,-3,4,-1,2,1,-5,4] output=6", "a": ""},
        {"q": "Find shortest path in a graph (Dijkstra).", "a": ""},
        {"q": "Detect cycle in a directed graph.", "a": ""},
        {"q": "Implement heapsort.", "a": ""},
        {"q": "Find kth largest element in an array.\nTest: arr=[3,2,1,5,6,4], k=2 output=5", "a": ""},
        {"q": "Rotate a matrix 90 degrees.\nTest: [[1,2],[3,4]] output=[[3,1],[4,2]]", "a": ""},
        {"q": "Reverse a linked list.", "a": ""},
        {"q": "Count islands in a 2D grid (flood fill).", "a": ""},
        {"q": "Implement a trie for string search.", "a": ""},
        {"q": "Write regex matcher for a given pattern.", "a": ""},
        {"q": "Find all palindrome substrings in a string.", "a": ""}
    ]
},








"Pseudocode": {
    "Easy": [
        {
            "q": "Which pseudocode correctly sums first N natural numbers?",
            "options": [
                "sum = 0; for i = 1 to N: sum = sum + i",
                "sum = 0; while i < N: sum = sum + i",
                "sum = N + 1; repeat N times: sum = sum + i",
                "sum = N * N"
            ],
            "a": "sum = 0; for i = 1 to N: sum = sum + i"
        },
        {
            "q": "What is the output of the following pseudocode for N=3?\nresult=1; for i=1 to N: result=result*i; print(result)",
            "options": ["3", "6", "1", "9"],
            "a": "6"
        },
        {
            "q": "Which pseudocode reverses a string S?",
            "options": [
                "for i=len(S) -1 to 0: print S[i]",
                "for i=0 to len(S)-1: print S[i]",
                "print S",
                "for i=0 to len(S): print S[i+1]"
            ],
            "a": "for i=len(S) -1 to 0: print S[i]"
        },
        {
            "q": "How do you check if number x is even?",
            "options": [
                "if x % 2 == 0",
                "if x / 2 == 1",
                "if x % 2 == 1",
                "if x == 2"
            ],
            "a": "if x % 2 == 0"
        },
        {
            "q": "Pseudocode to swap two numbers a, b:",
            "options": [
                "temp=a; a=b; b=temp",
                "a=b; b=a",
                "a=a+b; b=a-b",
                "a=b-a; b=a+b"
            ],
            "a": "temp=a; a=b; b=temp"
        },
        {
            "q": "How to count vowels in word W?",
            "options": [
                "for letter in W: if letter in 'aeiou': count++",
                "for letter in W: count-- if letter not a vowel",
                "count = length(W)",
                "print all consonants"
            ],
            "a": "for letter in W: if letter in 'aeiou': count++"
        },
        {
            "q": "To find max in array arr of size n:",
            "options": [
                "max=arr[0]; for i=1 to n-1: if arr[i]>max: max=arr[i]",
                "max=0; for i=0 to n-1: max=max+arr[i]",
                "sort arr; max = arr[0]",
                "max=arr[n-1]"
            ],
            "a": "max=arr[0]; for i=1 to n-1: if arr[i]>max: max=arr[i]"
        },
        {
            "q": "Which outputs table of n?",
            "options": [
                "for i=1 to 10: print n*i",
                "for i=1 to n: print i*n",
                "for i=1 to n*n: print i",
                "for i=1 to 5: print n"
            ],
            "a": "for i=1 to 10: print n*i"
        },
        {
            "q": "Pseudocode to calculate area of circle r:",
            "options": [
                "area=3.14*r*r",
                "area=2*3.14*r",
                "area=3.14*r",
                "area=r*3.14"
            ],
            "a": "area=3.14*r*r"
        },
        {
            "q": "Convert Celsius C to Fahrenheit F:",
            "options": [
                "F = (C*9/5)+32",
                "F = (C+32)*9/5",
                "F = (32-C)*9/5",
                "F = C-32"
            ],
            "a": "F = (C*9/5)+32"
        },
        {
            "q": "Pseudocode to check anagrams of str1 and str2:",
            "options": [
                "if sorted(str1)==sorted(str2)",
                "if str1 in str2",
                "if len(str1)==len(str2)",
                "if str1==str2"
            ],
            "a": "if sorted(str1)==sorted(str2)"
        },
        {
            "q": "Find length of string S:",
            "options": [
                "len=0; for c in S: len++",
                "len = S[0]",
                "len = sum(S)",
                "len = 1"
            ],
            "a": "len=0; for c in S: len++"
        },
        {
            "q": "Reverse integer N (123 to 321):",
            "options": [
                "rev=0; while N>0: rev=rev*10+N%10; N=floor(N/10)",
                "rev=N*10",
                "rev=N%10",
                "rev=reverse(N)"
            ],
            "a": "rev=0; while N>0: rev=rev*10+N%10; N=floor(N/10)"
        },
        {
            "q": "Sum digits of N:",
            "options": [
                "sum=0; while N>0: sum+=N%10; N=N/10",
                "sum = N*10",
                "sum = N-N%10",
                "sum = sum + N"
            ],
            "a": "sum=0; while N>0: sum+=N%10; N=N/10"
        },
        {
            "q": "Fibonacci up to N terms:",
            "options": [
                "a=0;b=1; print a,b; for i=2 to N: c=a+b;a=b;b=c;print c",
                "for i=1 to N: print i*i",
                "for i=0 to N: print i",
                "print N"
            ],
            "a": "a=0;b=1; print a,b; for i=2 to N: c=a+b;a=b;b=c;print c"
        }
    ],
    "Medium": [
        {
            "q": "Pseudocode for bubble sort:",
            "options": [
                "for i=0 to n-1: for j=0 to n-i-1: if arr[j]>arr[j+1]: swap",
                "for i=0 to n-1: for j=0 to n-1: arr[j]=arr[j-1]",
                "for i=0 to n: for j=0 to n: arr[i]=arr[j]",
                "while arr[j]<arr[j+1]: swap"
            ],
            "a": "for i=0 to n-1: for j=0 to n-i-1: if arr[j]>arr[j+1]: swap"
        },
        {
            "q": "Add two matrices A and B of size n*n:",
            "options": [
                "for i=0 to n-1: for j=0 to n-1: C[i][j]=A[i][j]+B[i][j]",
                "C=A+B",
                "for i=0 to n-1: C[i]=A[i]+B[j]",
                "for i=0 to n: C[i]=A[i]-B[i]"
            ],
            "a": "for i=0 to n-1: for j=0 to n-1: C[i][j]=A[i][j]+B[i][j]"
        },
        {
            "q": "Linear search for val in arr:",
            "options": [
                "for i=0 to n-1: if arr[i]==val: return i",
                "sort arr first, then search",
                "for i=0 to n: arr[i]=val",
                "while arr[i]!=val: i++"
            ],
            "a": "for i=0 to n-1: if arr[i]==val: return i"
        },
        {
            "q": "GCD of two numbers a, b:",
            "options": [
                "while b != 0: temp=b; b=a%b; a=temp",
                "gcd = a*b",
                "if a==b: return a",
                "gcd = a+b"
            ],
            "a": "while b != 0: temp=b; b=a%b; a=temp"
        },
        {
            "q": "Convert decimal to binary.",
            "options": [
                "while n>0: bin = bin + str(n%2); n=n//2",
                "for i=0 to n: print i",
                "bin=n*2",
                "while n<10: n++"
            ],
            "a": "while n>0: bin = bin + str(n%2); n=n//2"
        },
        {
            "q": "Remove duplicates from list arr.",
            "options": [
                "newArr = []; for i in arr: if i not in newArr: newArr.append(i)",
                "sort arr; return arr",
                "for i in arr: if arr[i]==arr[i+1]: skip",
                "return arr"
            ],
            "a": "newArr = []; for i in arr: if i not in newArr: newArr.append(i)"
        },
        {
            "q": "Matrix multiplication for C=A*B:",
            "options": [
                "for i=0 to n-1: for j=0 to n-1: for k=0 to n-1: C[i][j]+=A[i][k]*B[k][j]",
                "C=A+B",
                "for i=0 to n: for k=0 to n: C[i][k]=A[i][k]*B[i][k]",
                "None"
            ],
            "a": "for i=0 to n-1: for j=0 to n-1: for k=0 to n-1: C[i][j]+=A[i][k]*B[k][j]"
        },
        {
            "q": "Check palindrome for S:",
            "options": [
                "if S==reverse(S)",
                "if len(S)%2==0",
                "if S[0]==S[1]",
                "if S==S"
            ],
            "a": "if S==reverse(S)"
        },
        {
            "q": "Selection sort pseudocode:",
            "options": [
                "for i=0 to n-1: min=i; for j=i+1 to n-1: if arr[j]<arr[min]: min=j; swap",
                "for i=0 to n-1: arr[i]=arr[i]-1",
                "sort arr",
                "while arr[i]>arr[j]: swap"
            ],
            "a": "for i=0 to n-1: min=i; for j=i+1 to n-1: if arr[j]<arr[min]: min=j; swap"
        },
        {
            "q": "Circular queue: enqueue operation",
            "options": [
                "rear=(rear+1)%size; if not full, queue[rear]=x",
                "rear=rear+1; queue[rear]=x",
                "queue.append(x)",
                "front=(front+1)%size"
            ],
            "a": "rear=(rear+1)%size; if not full, queue[rear]=x"
        },
        {
            "q": "Merge two sorted lists arr1, arr2.",
            "options": [
                "while arr1 and arr2: if arr1[0]<arr2[0]: result.append(arr1.pop(0)); else: result.append(arr2.pop(0));",
                "arr3 = arr1+arr2",
                "sort(arr1+arr2)",
                "for i in arr1: result.append(i); for j in arr2: result.append(j)"
            ],
            "a": "while arr1 and arr2: if arr1[0]<arr2[0]: result.append(arr1.pop(0)); else: result.append(arr2.pop(0));"
        },
        {
            "q": "Count frequency of each element in list L:",
            "options": [
                "for x in L: freq[x] += 1",
                "freq = L.count(x)",
                "freq = {}",
                "for x in L: freq=L[x]"
            ],
            "a": "for x in L: freq[x] += 1"
        },
        {
            "q": "Insert X in sorted array arr of n elements.",
            "options": [
                "find position i where arr[i]>X; insert X at i",
                "append X to arr",
                "arr[0]=X",
                "reverse arr, then insert"
            ],
            "a": "find position i where arr[i]>X; insert X at i"
        },
        {
            "q": "Left rotate an array arr by 1.",
            "options": [
                "temp=arr[0]; for i=0 to n-2: arr[i]=arr[i+1]; arr[n-1]=temp",
                "arr.reverse()",
                "arr=arr[1:]+arr[0]",
                "None"
            ],
            "a": "temp=arr[0]; for i=0 to n-2: arr[i]=arr[i+1]; arr[n-1]=temp"
        },
        {
            "q": "Binary to decimal conversion.",
            "options": [
                "dec=0; for i=len(bin)-1 to 0: dec+=int(bin[i])*2^(len(bin)-i-1)",
                "dec=bin*2",
                "dec=int(bin)",
                "None"
            ],
            "a": "dec=0; for i=len(bin)-1 to 0: dec+=int(bin[i])*2^(len(bin)-i-1)"
        },
    ],
    "Hard": [
        {
            "q": "Binary search pseudocode on arr for val.",
            "options": [
                "low=0; high=n-1; while low<=high: mid=(low+high)//2; if arr[mid]==val: return mid...",
                "for each x in arr: if x==val: return",
                "arr.sort(); return arr[0]",
                "while low<high: mid=(low-high)//2"
            ],
            "a": "low=0; high=n-1; while low<=high: mid=(low+high)//2; if arr[mid]==val: return mid..."
        },
        {
            "q": "Pseudocode for quicksort.",
            "options": [
                "if low<high: pi=partition(arr,low,high); quicksort(arr,low,pi-1); quicksort(arr,pi+1,high)",
                "for i=high to low: sort(arr)",
                "sort arr",
                "partition arr into halves"
            ],
            "a": "if low<high: pi=partition(arr,low,high); quicksort(arr,low,pi-1); quicksort(arr,pi+1,high)"
        },
        {
            "q": "Find kth smallest in BST.",
            "options": [
                "inorder(BST); return kth element",
                "sort BST; return kth",
                "preorder(BST); return kth",
                "BFS(BST); return kth"
            ],
            "a": "inorder(BST); return kth element"
        },
        {
            "q": "DFS to count islands in matrix.",
            "options": [
                "for each cell: if not visited and is land: call DFS",
                "for each row: for each col: mark visited",
                "check all cells == 0",
                "call BFS on all nodes"
            ],
            "a": "for each cell: if not visited and is land: call DFS"
        },
        {
            "q": "Dijkstra's shortest path pseudocode.",
            "options": [
                "set dist[]; set pq; while pq not empty: u=min dist; relax all edges",
                "for i=0 to n-1: for j=0 to n: check path",
                "relax all edges |V|-1 times",
                "sort all paths"
            ],
            "a": "set dist[]; set pq; while pq not empty: u=min dist; relax all edges"
        },
        {
            "q": "Topological sort using DFS.",
            "options": [
                "for each unvisited node: DFS; push to stack after visiting",
                "sort all nodes by value",
                "DFS from first node only",
                "BFS and sort"
            ],
            "a": "for each unvisited node: DFS; push to stack after visiting"
        },
        {
            "q": "Rabin-Karp pseudocode for pattern matching.",
            "options": [
                "Compute hash of pattern and every substring, compare",
                "Check every char one by one",
                "Sort pattern and string",
                "None"
            ],
            "a": "Compute hash of pattern and every substring, compare"
        },
        {
            "q": "Prim's algorithm for MST.",
            "options": [
                "start with min edge, grow MST by adding min adjacent edge",
                "add all edges to MST",
                "sort nodes and edges",
                "remove max edge each time"
            ],
            "a": "start with min edge, grow MST by adding min adjacent edge"
        },
        {
            "q": "Sudoku backtracking pseudocode.",
            "options": [
                "if cell empty, try 1-9; if valid, move next; else backtrack",
                "fill all cells with 1",
                "check rows only",
                "fill diagonal cells"
            ],
            "a": "if cell empty, try 1-9; if valid, move next; else backtrack"
        },
        {
            "q": "Graph coloring algorithm.",
            "options": [
                "assign smallest possible color to each node, ensuring adjacent nodes differ",
                "color all nodes same",
                "sort nodes, color in order",
                "use BFS"
            ],
            "a": "assign smallest possible color to each node, ensuring adjacent nodes differ"
        },
        {
            "q": "Quicksort space complexity pseudocode.",
            "options": [
                "O(log n) average",
                "O(n^2) always",
                "O(n) always",
                "O(1)"
            ],
            "a": "O(log n) average"
        },
        {
            "q": "LRU cache: which data structure?",
            "options": [
                "Doubly linked list + HashMap",
                "Stack only",
                "Queue only",
                "Tree"
            ],
            "a": "Doubly linked list + HashMap"
        },
        {
            "q": "Merge intervals pseudocode.",
            "options": [
                "Sort intervals by start; merge if overlap",
                "Check all pairs, sum",
                "Sort by end time only",
                "Use only BFS"
            ],
            "a": "Sort intervals by start; merge if overlap"
        },
        {
            "q": "Print preorder of binary tree.",
            "options": [
                "visit node -> left -> right",
                "left -> node -> right",
                "right -> node -> left",
                "left -> right -> node"
            ],
            "a": "visit node -> left -> right"
        },
        {
            "q": "Find strongly connected components in graph.",
            "options": [
                "Kosaraju's or Tarjan's algorithm",
                "Prim's algorithm",
                "Bellman-Ford",
                "BFS only"
            ],
            "a": "Kosaraju's or Tarjan's algorithm"
        }
    ]
}
# ------------------------------------------------------------------------

TOPICS = {
    k: list(v.keys()) for k, v in QUESTION_BANK.items() if isinstance(v, dict)
}

# ----------------------- Utility Functions -------------------------------
def tfidf_similarity(a, b):
    if not a or not b or not a.strip() or not b.strip():
        return 0.0
    try:
        v = TfidfVectorizer()
        tfidf = v.fit_transform([a, b])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return round(min(sim * 100, 100), 2)  # cap at 100
    except:
        return 0.0

def pick_questions(section, topic, diff, count):
    try:
        pool = []
        if section in QUESTION_BANK and topic in QUESTION_BANK[section] and diff in QUESTION_BANK[section][topic]:
            pool = QUESTION_BANK[section][topic][diff].copy()
        random.shuffle(pool)
        while len(pool) < count:
            pool.append(random.choice(pool))
        return pool[:count]
    except Exception:
        return []

def load_history():
    if os.path.exists("history.json"):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(data):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def record_result(section, topic, score, details):
    h = load_history()
    h.append({
        "id": str(uuid.uuid4()),
        "section": section,
        "topic": topic,
        "timestamp": datetime.utcnow().isoformat(),
        "score": round(float(score), 2) if score is not None else 0,
        "details": details
    })
    save_history(h)

# ---------------------- Sidebar Instructions & Tips ----------------------
st.sidebar.markdown("""
<div class="cardy">
<div class="cardy-title">🛠️ Instructions & Tips</div>
<ul style="padding-left:18px;margin-top:-8px;">
<li class="cardy-li">Select section, topic & difficulty, then <b>Start Test</b>.</li>
<li class="cardy-li">Timer begins after you start.</li>
<li class="cardy-li">Stay on this tab (do not switch browser tabs).</li>
<li class="cardy-li">Use Previous/Next/Save.</li>
<li class="cardy-li">Submit Test 🏁 anytime.</li>
<li class="cardy-li">Review analytics after each test.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ---------------------- Session Defaults -----------------------
if "mode" not in st.session_state:
    st.session_state.mode = "main"

# ---------------------- Main Page: Selection Tabs -----------------------
if st.session_state.mode == "main":
    st.markdown("<div class='big-title'>Interview Preparation Platform</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Interactive Interview Practice and Analytics Portal</div>", unsafe_allow_html=True)

    section_tabs = st.tabs([
        "🧠 Practice", "🎤 Mock Interview", "📝 MCQ Quiz", "💻 Code Runner", "📄 Pseudocode",
        "📈 Results", "📊 Analytics", "🕓 History"
    ])

    # ---------- Practice Section ----------
    with section_tabs[0]:
        if "Practice" in TOPICS:
            topic = st.selectbox("Select Topic", TOPICS["Practice"], key="practice_topic")
            diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="practice_diff")
            count = st.slider("Number of Questions", 1, 15, 5, key="practice_count")
            if st.button("▶ Start Practice", key="practice_start"):
                qs = pick_questions("Practice", topic, diff, count)
                st.session_state.exam = {
                    "section": "Practice",
                    "topic": topic,
                    "diff": diff,
                    "qs": qs,
                    "answers": [""]*len(qs),
                    "idx": 0,
                    "start": time.time()
                }
                st.session_state.mode = "exam"
                st.experimental_rerun()
        else:
            st.info("No topics available for Practice. Please fill the QUESTION_BANK.")

    # ---------- Mock Interview Section ----------
    with section_tabs[1]:
        if "Mock Interview" in TOPICS:
            topic = st.selectbox("Interview Type", TOPICS["Mock Interview"], key="mock_type")
            diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], key="mock_diff")
            count = st.slider("Number of Questions", 1, 15, 5, key="mock_count")
            if st.button("▶ Start Mock Interview", key="mock_start"):
                qs = pick_questions("Mock Interview", topic, diff, count)
                st.session_state.exam = {
                    "section":"Mock Interview",
                    "topic":topic,
                    "diff":diff,
                    "qs":qs,
                    "answers":[""]*len(qs),
                    "idx":0,
                    "start":time.time()
                }
                st.session_state.mode = "exam"
                st.experimental_rerun()
        else:
            st.info("No topics available for Mock Interview. Please fill the QUESTION_BANK.")

    # ---------- MCQ Quiz ----------
    with section_tabs[2]:
        if "MCQ Quiz" in TOPICS:
            topic = st.selectbox("Quiz Topic", TOPICS["MCQ Quiz"], key="mcq_topic")
            diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="mcq_diff")
            count = st.slider("Number of MCQs", 1, 15, 5, key="mcq_count")
            if st.button("▶ Start MCQ Quiz", key="mcq_start"):
                qs = pick_questions("MCQ Quiz", topic, diff, count)
                st.session_state.exam = {
                    "section":"MCQ Quiz",
                    "topic":topic,
                    "diff":diff,
                    "qs":qs,
                    "answers":[""]*len(qs),
                    "idx":0,
                    "start":time.time()
                }
                st.session_state.mode = "exam"
                st.experimental_rerun()
        else:
            st.info("No topics available for MCQ Quiz. Please fill the QUESTION_BANK.")

    # ---------- Code Runner ----------
    with section_tabs[3]:
        if "Code Runner" in TOPICS:
            topic = TOPICS["Code Runner"][0] if TOPICS["Code Runner"] else ""
            diff = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="code_diff")
            count = st.slider("Number of Code Questions", 1, 15, 5, key="code_count")
            if st.button("▶ Start Code Practice", key="code_start"):
                qs = pick_questions("Code Runner", topic, diff, count)
                st.session_state.exam = {
                    "section":"Code Runner",
                    "topic":topic,
                    "diff":diff,
                    "qs":qs,
                    "answers":[""]*len(qs),
                    "idx":0,
                    "start":time.time()
                }
                st.session_state.mode = "exam"
                st.experimental_rerun()
        else:
            st.info("No questions available for Code Runner. Please fill the QUESTION_BANK.")

    # ---------- Pseudocode ----------
    with section_tabs[4]:
        if "Pseudocode" in TOPICS:
            topic = TOPICS["Pseudocode"][0] if TOPICS["Pseudocode"] else ""
            diff = st.selectbox("Difficulty", ["Easy","Medium","Hard"], key="pseudo_diff")
            count = st.slider("Number of Pseudocode Questions", 1, 15, 5, key="pseudo_count")
            if st.button("▶ Start Pseudocode", key="pseudo_start"):
                qs = pick_questions("Pseudocode", topic, diff, count)
                st.session_state.exam = {
                    "section":"Pseudocode",
                    "topic":topic,
                    "diff":diff,
                    "qs":qs,
                    "answers":[""]*len(qs),
                    "idx":0,
                    "start":time.time()
                }
                st.session_state.mode = "exam"
                st.experimental_rerun()
        else:
            st.info("No questions available for Pseudocode. Please fill the QUESTION_BANK.")

    # ---------- Results ----------
    with section_tabs[5]:
        st.subheader("📈 Results")
        h = load_history()
        if not h:
            st.info("No test results found.")
        else:
            df = pd.DataFrame(h)
            st.dataframe(df[["section","topic","timestamp","score"]])

    # ---------- Analytics ----------
    with section_tabs[6]:
        st.subheader("📊 Analytics")
        h = load_history()
        if not h:
            st.info("No data to analyze.")
        else:
            df = pd.DataFrame(h)
            if "score" in df.columns:
                fig = px.bar(df, x="section", y="score", color="section", title="Score per Section", text_auto=True)
                st.plotly_chart(fig, use_container_width=True)
                avg_scores = df.groupby("section")["score"].mean().reset_index()
                fig2 = px.pie(avg_scores, names="section", values="score", title="Strength vs Weakness")
                st.plotly_chart(fig2, use_container_width=True)

    # ---------- History ----------
    with section_tabs[7]:
        st.subheader("🕓 History")
        h = load_history()
        if not h:
            st.info("No history found.")
        else:
            for rec in h[::-1]:
                st.markdown(f"**Section:** {rec['section']} | **Topic:** {rec.get('topic','-')} | **Timestamp:** {rec['timestamp']} | **Score:** {rec['score']}")
                if st.button(f"View Details", key=rec['id']):
                    for d in rec.get("details", []):
                        st.write(f"Q: {d['q']} — Score: {d.get('score', 'N/A')}")

# ---------------------- Exam Page: Unified Logic for All Sections -----------------
elif st.session_state.mode == "exam":
    ex = st.session_state.get("exam", None)
    if not ex:
        st.error("No active test.")
        if st.button("Return Home"):
            st.session_state.mode = "main"
            st.experimental_rerun()
    else:
        st.markdown(f"<h2 style='color:#4B0082;'>{ex['section']} — {ex['topic']} — Difficulty: {ex['diff']}</h2>", unsafe_allow_html=True)
        total_time = 30 * 60
        # --- Real-time timer update ---
        if "timer" not in st.session_state:
            st.session_state.timer = time.time()
        elapsed = int(time.time() - ex["start"])
        remaining = max(total_time - elapsed, 0)
        m, s = divmod(remaining, 60)

        colT1, colT2 = st.columns([7, 1])
        timer_placeholder = colT1.empty()
        def timer_update():
            nonlocal remaining, timer_placeholder
            timer_placeholder.markdown(
                f"<span style='color:{'red' if remaining <= 300 else 'green'};font-weight:bold;'>⏱ Time Left: {m:02}:{s:02}</span>",
                unsafe_allow_html=True
            )

        timer_update()
        time.sleep(1)
        if remaining > 0:
            st.experimental_rerun()
        else:
            # Only auto-submit if not already at submission
            st.warning("⏰ Time over! Submitting...")
            details = []
            if ex["section"] in ["Practice"]:
                scores = [tfidf_similarity(a, q["a"]) for a, q in zip(ex["answers"], ex["qs"])]
                avg = np.mean(scores) if scores else 0
                details = [{"q": q["q"], "score": round(s, 2)} for q, s in zip(ex["qs"], scores)]
            elif ex["section"] == "MCQ Quiz":
                scores = []
                for a, q in zip(ex["answers"], ex["qs"]):
                    s = 1 if a == q["a"] else 0
                    scores.append(s)
                    details.append({"q": q["q"], "selected": a, "correct": q["a"], "score": s})
                avg = sum(scores)
            elif ex["section"] in ["Mock Interview","Pseudocode","Code Runner"]:
                scores = []
                for a, q in zip(ex["answers"], ex["qs"]):
                    s = tfidf_similarity(a, q["a"]) if ex["section"] != "Mock Interview" else 0.0
                    scores.append(s)
                    details.append({"q": q["q"], "answer": a, "score": s})
                avg = np.mean(scores) if scores else 0
            else:
                avg = 0
                details = [{"q": q["q"], "score": 0} for q in ex["qs"]]
            record_result(ex["section"], ex.get("topic",""), avg, details)
            del st.session_state.exam
            st.session_state.mode = "main"
            st.experimental_rerun()

        with colT2:
            if st.button("🏁 Submit Test"):
                details = []
                if ex["section"] in ["Practice"]:
                    scores = [tfidf_similarity(a, q["a"]) for a, q in zip(ex["answers"], ex["qs"])]
                    avg = np.mean(scores) if scores else 0
                    details = [{"q": q["q"], "score": round(s, 2)} for q, s in zip(ex["qs"], scores)]
                elif ex["section"] == "MCQ Quiz":
                    scores = []
                    for a, q in zip(ex["answers"], ex["qs"]):
                        s = 1 if a == q["a"] else 0
                        scores.append(s)
                        details.append({"q": q["q"], "selected": a, "correct": q["a"], "score": s})
                    avg = sum(scores)
                elif ex["section"] in ["Mock Interview","Pseudocode","Code Runner"]:
                    scores = []
                    for a, q in zip(ex["answers"], ex["qs"]):
                        s = tfidf_similarity(a, q["a"]) if ex["section"] != "Mock Interview" else 0.0
                        scores.append(s)
                        details.append({"q": q["q"], "answer": a, "score": s})
                    avg = np.mean(scores) if scores else 0
                else:
                    avg = 0
                    details = [{"q": q["q"], "score": 0} for q in ex["qs"]]
                record_result(ex["section"], ex.get("topic",""), avg, details)
                del st.session_state.exam
                st.session_state.mode = "main"
                st.experimental_rerun()

        idx = ex["idx"]
        q = ex["qs"][idx]
        st.markdown(
            f"<div style='background-color:#f9f7ff;color:#1a0441;padding:22px 15px 16px 18px;border-radius:11px;margin-bottom:12px;font-size:17.5px;font-weight:500;'><b>Q{idx+1}. {q.get('q','')}</b></div>",
            unsafe_allow_html=True
        )

        # Dynamic question rendering for MCQs/Pseudocode MCQs
        if ex["section"] == "MCQ Quiz" or (ex["section"] == "Pseudocode" and 'options' in q):
            opts = q.get("options", [])
            selected = st.radio("Select Option:", opts, index=opts.index(ex["answers"][idx]) if ex["answers"][idx] in opts else 0, key=f"ans{idx}")
            ex["answers"][idx] = selected
        elif ex["section"] == "Code Runner":
            lang = st.selectbox("Language:", ["Python","Java","C++"], key=f"lang{idx}")
            code = st.text_area("Write your code here:", value=ex["answers"][idx], height=150, key=f"ans{idx}")
            st.info("Test Cases Example:\n" + "\n".join([line for line in q["q"].splitlines() if line.lower().startswith("test case")]))
            ex["answers"][idx] = code
        else:
            ans = st.text_area("Your answer:", value=ex["answers"][idx], height=120, key=f"ans{idx}")
            ex["answers"][idx] = ans

        st.session_state.exam = ex

        f1, f2, f3 = st.columns([1, 1, 1])
        if f1.button("⬅ Previous"):
            if idx > 0:
                ex["idx"] -= 1
                st.session_state.exam = ex
                st.experimental_rerun()
        if f2.button("Next ➡"):
            if idx < len(ex["qs"]) - 1:
                ex["idx"] += 1
                st.session_state.exam = ex
                st.experimental_rerun()
        if f3.button("💾 Save Answer"):
            st.success("Answer saved ✅")

        st.progress((idx + 1) / len(ex["qs"]))
        st.caption(f"Question {idx+1}/{len(ex['qs'])}")

# --- Footer ---
st.markdown("<div style='text-align:center;padding:10px;color:#5612c6;font-weight:bold;'>Developed by Anil & Team</div>", unsafe_allow_html=True)
