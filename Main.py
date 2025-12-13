from dotenv import load_dotenv
load_dotenv()

from Judge import Judge
from Debater import Debater
from Router import Router
import time


def run_council(topic):
    # Define the team
    pm= Debater("Product Manager", "Visionary Project Manager. Focus on user value and features.")
    eng = Debater("Lead Engineer", "Pragmatic Engineer. Focus on feasability and constraints")
    
    # Judge as the product lead
    lead = Judge("Project Lead", "Agile Lead. Create the PID. Approve the plan")

    agents = {
        "Product Manager" : pm,
        "Lead Engineer" : eng,
        "Project Lead" : lead
    }

    router =  Router(list(agents.keys()))

    history = [{"role": "user", "content":f"Topic: {topic}. PM, start us off"}]

    print(f"======== DYNAMIC COUNCIL: {topic} ===========\n")

    # let me figure this out in peace

    while True:
        next_speaker = router.speak(history)
        # debuggin...
        print(f"\n[ROUTER SELECTS]: {next_speaker}")

        if "TERMINATE" in next_speaker:
            print("-----END OF CONVERSATION-----")
            break

        # i forgot that llms are stupid
        if next_speaker not in agents:
            print(f"Error: Router selected '{next_speaker}' I guess Router is High")
            next_speaker = "Project Lead"


        current_agent = agents[next_speaker]
        response = current_agent.speak(history)


        print(f"[{next_speaker.upper()}]:\n {response[:200]}...\n")

        history.append({
            "role": "assistant",
            "content": f"{next_speaker}:{response}" 
        })

        time.sleep(2)



if __name__ == "__main__":
    run_council("I want a way to for my macbook to communicate with my iphone such that when I bring my iphone to a suitable distance my macbook wakes up from sleep and when I move away It goes back to sleep")

