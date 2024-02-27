import os.path
from rich.console import Console
from rich.markdown import Markdown
from rich import print
from json import JSONEncoder

class File: 
    """This is just a simple wrapper for basic File operations, letting me be a little lazier"""
    def __init__(self, file): 
        self.file = file 
    
    def write(self, content: str) -> None: 
        """A simple write method to write directly to files"""
        with open(self.file, "w") as f: 
            f.write(content)
    
    def read(self) -> str: 
        """A simple read method, returning a string of all files"""
        if(not os.path.isfile(self.file)): 
            return ""
        with(open(self.file, "r")) as f: 
            return f.read()

class SolvedQuestion: 
    """Represents a simple Solved Question, purely for ease of use when encoding / decoding your `solves.json`"""
    def __init__(self, question, answer): 
        self.id = question.id 
        self.question = question.question 
        self.answer = answer

class QuestionEncoder(JSONEncoder): 
    """A base encoder, just allowing you to quickly encode what you need to encode"""
    def default(self, o): 
        return o.__dict__ 

class Question: 
    """A question wrapper, decoding the GET Response into a convenient form for ease of use """
    def __init__(self, obj): 
        self.id = obj["id"]
        self.question = obj["description"] 
        self.title = obj["name"]
        self.points = obj["value"] 
        self.max_attempts = obj["max_attempts"]
        self.attempts = obj["attempts"]
        self.type = obj["type"] 
        self.solved = obj["solved_by_me"]

    def send(self): 
        """Sends question information to the terminal in a pretty way"""
        print(f"[dark_goldenrod]{self.title}[/dark_goldenrod] - ([bright_yellow]{self.attempts}[/bright_yellow]/[bright_yellow]{self.max_attempts}[/bright_yellow])")
        Console().print(Markdown(self.question))


