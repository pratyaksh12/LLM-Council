from AgentBase import AgentBase
import os
from groq import Groq

# Initialize Groq Client (Shared or Local)
# For safety, we init inside the class or globally if keys are guaranteed
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Judge(AgentBase):
    """Judge using Groq Llama 3.3 70B"""
    def __init__(self, name, system_prompt, model="llama-3.3-70b-versatile"):
        super().__init__(name, system_prompt)
        self.model = model

    def speak(self, conversation_history: list):
        # Groq is stateless, so we pass the full history
        # We prepend the system prompt here as well
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_history)

        completion = groq_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7
        )
        return completion.choices[0].message.content
