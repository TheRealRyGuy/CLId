import api
import json
import random
import sys
from rich import print
from rich.prompt import Prompt
from objects import Question, SolvedQuestion, QuestionEncoder
import os 

class CLId: 
    def __init__(self, base, apikey, log_solves): 
        self.base = base 
        self.apikey = apikey 
        self.log_solves = log_solves
        if log_solves: 
            print("[bright_green]We are logging solves![/bright_green]")
        else: 
            print("[bright_red]We are not logging solves![/bright_red]")
    
    def preload(self): 
        api.base = self.base
        api.api_key = self.apikey

        if not os.path.exists("solves.json"): 
            with open("solves.json", "w") as file: file.write("[]") 
            self.solves = list() 
        else: 
            with open("solves.json", "r") as file: self.solves = json.loads(file.read().strip())

        try:
            results = json.loads(api.get_challenges().text)['data']
        except: 
            print("[bright_red]Error grabbing basic data! Please double check your config file![/bright_red]")
            sys.exit(0) 
        print(f"Grabbed {len(results)} questions!")
        unsolved = list(filter(lambda obj: not obj["solved_by_me"], results))
        self.unsolved = unsolved
        print(f"Grabbed {len(unsolved)} unsolved questions!") 
        categories = list(set(map(lambda obj: obj["category"], unsolved)))
        categories.sort()
        self.categories = categories 
        print(f"Found {len(categories)} unique categories to pull from!\n")
    
    def categories_prompt(self): 
        for category in self.categories: 
            print(f"{self.categories.index(category)} - {category}")
        print(f"{len(self.categories)} - All Categories")
        choices = ["q"]
        choices = [str(x) for x in range(0, len(self.categories)+1)]
        choices.append("q")
        cat = Prompt.ask(f"Type in [cyan1]any number[/cyan1] to get your set of PE's to do, or [cyan1]quit[/cyan1] to quit", default="0", choices=choices)
        if cat.lower() == "q" or cat.lower() == "quit": 
                print("Goodbye!")
                self.save()
                return
        catNum = int(cat) 
        if catNum != len(self.categories): 
                chosenCat = self.categories[catNum]
                questions = list(filter(lambda obj: obj["category"] == chosenCat, self.unsolved))
                if(len(questions) == 0): 
                    print(f"You have solved every question in this category!")
                else: 
                    self.runQuestions(questions)
        else: 
            self.runQuestions(self.unsolved)

    def runQuestions(self, questions): 
        print(f"\nFound [bright_yellow]{len(questions)}[/bright_yellow] questions for your category!")
        while True:
            randQuestion = random.choice(questions)
            randQuestionId = randQuestion["id"]
            questions.remove(randQuestion)
            question = Question(api.get_challenge(randQuestionId))
            if not self.tryQuestion(question): break 
            if len(questions) == 0: 
                print("[dark_goldenrod]You have ran out of questions in this category![/dark_goldenrod]")
                break 
        self.categories_prompt() 

    #Return true if we want to move to a new question, False if we're done with this category 
    def tryQuestion(self, question: Question) -> bool: 
        question.send()
        while True:
            print('Write your [bright_yellow]Answer[/bright_yellow], [bright_yellow]n[/bright_yellow] for a new question, [bright_yellow]q[/bright_yellow] to quit this category, or [bright_yellow]quit[/bright_yellow] to quit the program')
            answer = Prompt.ask("Answer")
            if(answer.lower() == "q"): 
                print("[dark_goldenrod]Moving to a new Category[/dark_goldenrod]")
                return False
            elif(answer.lower() == "quit"):
                print("[bright_green]Goodbye![/bright_green]")
                self.save() 
                sys.exit(0)
            elif(answer.lower() == "n"): 
                print("[dark_goldenrod]Moving to a new question[/dark_goldenrod]")
                return True 
            api.attempt_challenge(question.id, answer)
            if(self.check_solved(question.id)): 
                print("[bright_green]You got it right! Moving to a new question[/bright_green]")
                self.solves.append(SolvedQuestion(question, answer))
                return True 
            else: 
                print("[bright_red]You did not get the question correct, try again![/bright_red]")
                if(question.max_attempts != 0): 
                    if(question.max_attempts == question.attempts+1): 
                        print("[red]You are at maximum attempts! Choosing a new question![/red]") 
                        return True 
                    else: 
                        print(f"[red]You have {int(question.max_attempts) - int(question.attempts)} attempts left[/red]")
                else: 
                    print("[orange_red1]Good news! You have unlimited attempts![/orange_red1]")

    def check_solved(self, id): 
        return Question(api.get_challenge(id)).solved
    
    def save(self): 
        if(self.log_solves):
            with open("solves.json", "w+") as file: 
                file.write(json.dumps(self.solves, indent=4, cls=QuestionEncoder))