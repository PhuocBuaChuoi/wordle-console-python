import copy
import random
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.output import ColorDepth
wordle_style = Style.from_dict({
    "none": "bg:#787c7e #ffffff",
    "nothere": "bg:#b59f3b #ffffff",
    "correct": "bg:#538d4e #ffffff"
})
list_={}
wordict={}
m=900000
with open("wordlist.txt","r") as reader:
    while m!=0:
        try:
            n = reader.readline()
            n=n.strip(" \n")
            if n=="":
                break
            if not n.isalpha():
                continue
            n=n.lower()
            if len(n) in list_:
                list_[len(n)].append(copy.deepcopy(n))
            else:
                list_[len(n)]=[copy.deepcopy(n)]
            wordict[copy.deepcopy(n)]=None
        except:
            break
        m-=1
with open("words_alpha.txt","r") as reader:
    while m!=0:
        try:
            n = reader.readline()
            n=n.strip(" \n")
            if n=="":
                break
            if not n.isalpha():
                continue
            wordict[copy.deepcopy(n)]=None
        except:
            break
        m-=1
def five_word(n):
    return len(n)==5 and n in wordict
validate = Validator.from_callable(five_word, error_message='Character length not five or that worrd not in dictionary!')
randchooseword = random.choice(list_[5])
charmap = [0]*26
for x in randchooseword:
    charmap[ord(x)-ord("a")]+=1
turnleft = 6
win=False
while turnleft!=0:
    word_user_guess = prompt("Guess the word: ",validator=validate,validate_while_typing=True)
    user_word_char_map=[0]*26
    for x in word_user_guess:
        user_word_char_map[ord(x) - ord("a")] += 1
    same_word_map = [0]*26
    for x in range(26):
        same_word_map[x]=min(user_word_char_map[x],charmap[x])
    state=[0]*5
    correct_char=0
    for x in range(5):
        if randchooseword[x]==word_user_guess[x]:
            correct_char+=1
            state[x]=2
            same_word_map[ord(randchooseword[x])-ord("a")]-=1
    for x in range(5):
        if same_word_map[ord(word_user_guess[x])-ord("a")] >0:
            state[x]=1
            same_word_map[ord(word_user_guess[x]) - ord("a")]-=1
    printstring="Information about relation between your guessed word and ourr word: "
    for x in range(5):
        match state[x]:
            case 0:
                printstring+=f"<none>{word_user_guess[x]}</none>"
            case 1:
                printstring += f"<nothere>{word_user_guess[x]}</nothere>"
            case 2:
                printstring += f"<correct>{word_user_guess[x]}</correct>"
    print_formatted_text(HTML(printstring),style=wordle_style,color_depth=ColorDepth.TRUE_COLOR)
    if correct_char==5:
        win=True
        break
    turnleft-=1
if win:
    print("You guess right! Congratulation!")
else:
    print(f"Sad for you :<. The correct word is: {randchooseword}")


