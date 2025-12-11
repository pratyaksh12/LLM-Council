import os
from AgentBase import AgentBase
from groq import Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Debater(AgentBase):
    def __init__(self, name, system_prompt, model="llama-3.1-8b-instant"):
        super().__init__(name, system_prompt)
        self.model = model

    def speak(self, conversation_history: list):
        # Groq needs the whole list of dicts to maintain a lean flow conversation
        messages = [{"role" : "system", "content" : self.system_prompt}]
        messages.extend(conversation_history)

        completion = groq_client.chat.completions.create(
            model=self.model,
            messages= messages,
            temperature=0.7
        )

        return completion.choices[0].message.content