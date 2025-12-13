from AgentBase import AgentBase
from groq import Groq
import os

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Router(AgentBase):
    def __init__(self, agent_names: list[str], model="llama-3.1-8b-instant"):
        names_str = ", ".join(agent_names)
        system_prompt = (
            f"You are a council moderator. The member are: [{names_str}]. \n"
            f"Read the conversation history and decide who should speak next. \n"
            f"CRITICAL: Output only the name of the agent. Do not say 'The next speaker is... \n'"
            f"Rules:\n"
            f"1. If the plan is complete and approved, output 'TERMINATE'.\n"
            f"2. If the feedback is given, choose the person who needs to fix it\n"
        )


        super().__init__(name="Router", system_prompt=system_prompt)
        self.model = model


    def speak(self, conversation_history: list) -> str:
        # copy history for the router to see the context without polluting the conversation script
        messages = [{"role": "system", "content": self.system_prompt}]

        messages.extend(conversation_history)
        completion = groq_client.chat.completions.create(
            model = self.model,
            messages=messages, # pyright: ignore[reportArgumentType]
            temperature=0.0 #strict logic
        )

        return completion.choices[0].message.content.strip()  # type: ignore
