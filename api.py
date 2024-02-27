import requests

# Just a static storage for the API bases pulled from Config 
api_key = "this is a key"
base = "this is an ip"

# A wrapped method to be able to send GET requests to specific endpoints on the CTFd server 
def get(endpoint: str) -> requests.Response: 
    return requests.get(f"{base}{endpoint}", headers={"Content-Type":"application/json", "Authorization": f"Token {api_key}"})

# A wrapped method to send a POST request to specific endpoints on the CTFd server
def post(endpoint: str, obj: dict) -> requests.Response: 
    return requests.post(f"{base}{endpoint}", json = obj, headers={"Content-Type":"application/json", "Authorization": f"Token {api_key}"})

# Pulls a list of challenges from the server
def get_challenges() -> requests.Response: 
    return get("/api/v1/challenges")

# Gets specific information from the challenge 
def get_challenge(id: int) -> requests.Response: 
    return get(f"/api/v1/challenges/{id}").json()["data"]

# Sends a challenge attempt to the server 
def attempt_challenge(id: int, submission: str) -> requests.Response: 
    return post("/api/v1/challenges/attempt", {"submission": submission, "challenge_id": id})