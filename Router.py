from AgentBase import AgentBase
from groq import Groq
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Router(AgentBase):
    def __init__(self, agent_names: list[str], model="llama-3.1-8b-instant"):
        self.names = agent_names
        names_str = ", ".join(agent_names)
        system_prompt = (
            f"You are the Council Moderator.\n"
            f"The available agents are: [{names_str}].\n"
            f"Read the conversation history and decide who should speak next.\n"
            f"INSTRUCTIONS:\n"
            f"1. Output ONLY the name of the agent (e.g. 'Product Manager').\n"
            f"2. Do NOT output any reasoning or punctuation.\n"
            f"3. If the conversation is finished/agreed, output 'TERMINATE'.\n"
        )
        super().__init__(name="Router", system_prompt=system_prompt)
        self.model = model

    def speak(self, conversation_history: list) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history)
        
        # Add a gentle nudge at the end to force a name
        messages.append({"role": "user", "content": f"Who speaks next? Choose from [{', '.join(self.names)}] or TERMINATE."})

        completion = groq_client.chat.completions.create(
            model=self.model,
            messages=messages, # pyright: ignore[reportArgumentType]
            temperature=0.0 
        )

        raw_decision = completion.choices[0].message.content.strip()
        
        # FIX!!!!!!!
        clean_decision = raw_decision.replace(".", "").replace('"', "").replace("'", "").strip()
        
        if not clean_decision:
            return "Project Lead" #default
            
        return clean_decision
