import pyfiglet
import json 
from rich import print 
from clid import CLId 
from objects import File 
import sys 

# A simple instantiation to return your base `CLId` object to start
def __init__() -> CLId: 
    # Send headers
    print(f'[cyan]{pyfiglet.figlet_format("CLId", font="slant")}[/cyan]')
    print('[cyan1]CLId: A CTFd CLI implementation\n[/cyan1]'.center(15))
    # Instantiate Config Properly
    config = File("answers.json") 
    config = File("config.json")
    if(len(config.read()) == 0):
        print("You do not have a config file! Creating one and exiting the program")
        base = '{"base": "myctfd.com", "api_key": "apikey123", "log_solves": True}'
        config.write(base) 
        return
    config_obj = json.loads(config.read())
    # Return our object for ease of use when loading 
    return CLId(config_obj["base"], config_obj["api_key"], config_obj["log_solves"] == "True")

try:
    cli = __init__() 
    cli.preload() 
    cli.categories_prompt()
except KeyboardInterrupt: 
    cli.save()
    print("\nYou have CTRL+C'd to exit, goodbye!")