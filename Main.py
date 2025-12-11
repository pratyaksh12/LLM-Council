from dotenv import load_dotenv
load_dotenv() 

from Judge import Judge
from Debater import Debater 

def product_strategy_meeting(app_idea):
    # PROJECT LEAD (Synthesizer) -> Llama 3.3 70B (Judge)
    project_lead = Judge(
        name="Project Lead",
        system_prompt="""You are an Agile Project Lead. 
        Your goal is to create a 'Project Initiation Document' (PID).
        Listen to the PM and Engineer.
        Output a structured plan:
        1. Core Features (MVP)
        2. Tech Stack Decisions
        3. Potential Risks"""
    )
    
    # 2 PRODUCT MANAGER (Visionary) -> Llama 3.1 8B (Debater)
    product_manager = Debater(
        name="Product Manager",
        system_prompt="""You are a visionary Product Manager.
        Focus on User Experience (UX), "Wow" features, and market fit.
        You don't care about technical difficulty, you care about user value.
        Describe the dream version of the app."""
    )

    # 3 LEAD ENGINEER (Pragmatist) -> Llama 3.1 8B (Debater)
    lead_engineer = Debater(
        name="Lead Engineer",
        system_prompt="""You are a Pragmatic Lead Engineer.
        Your job is to ground the PM's dreams in reality.
        Suggest specific stacks (e.g., React, Python, Postgres).
        Point out expense/complexity/timeline risks.
        Offer technical alternatives."""
    )

    history = []
    print(f"===== KICKOFF MEETING: {app_idea} =====\n")

    # --- PHASE 1: PM PITCHES THE VISION ---
    history.append({"role": "user", "content": f"The client wants: {app_idea}. PM, pitch us the vision."})
    
    pm_pitch = product_manager.speak(history)
    history.append({"role": "assistant", "content": f"PM_PITCH: {pm_pitch}"}) 
    print(f"[PRODUCT MANAGER]:\n{pm_pitch}\n")

    # --- PHASE 2: ENGINEER FEASIBILITY CHECK ---
    history.append({"role": "user", "content": "Engineer, what is the best stack for this? What are the hard parts?"})
    
    eng_response = lead_engineer.speak(history)
    history.append({"role": "assistant", "content": f"ENG_RESPONSE: {eng_response}"})
    print(f"[LEAD ENGINEER]:\n{eng_response}\n")

    # --- PHASE 3: NEGOTIATION (THE "DISCUSSION" PART) ---
    #force the PM to respond to the Engineer's constraints
    history.append({"role": "user", "content": "PM, the Engineer raised some constraints. Update the scope to be an MVP."})
    
    pm_mvp_adjustment = product_manager.speak(history)
    history.append({"role": "assistant", "content": f"PM_REVSIION: {pm_mvp_adjustment}"})
    print(f"[PRODUCT MANAGER (MVP ADJUSTMENT)]:\n{pm_mvp_adjustment}\n")

    # --- PHASE 4: FINAL PLAN ---
    final_prompt = "Based on the discussion above, generate the Project Initiation Document."
    
    history_for_judge = history.copy()
    history_for_judge.append({"role": "user", "content": final_prompt})
    
    final_plan = project_lead.speak(history_for_judge)
    print(f"[PROJECT LEAD - FINAL PLAN]:\n{final_plan}")

if __name__ == "__main__":
    product_strategy_meeting("I want a way to for my macbook to communicate with my iphone such that when I bring my iphoone to a suitable distance my macbook wakes up from sleep and when I move away It goes back to sleep")