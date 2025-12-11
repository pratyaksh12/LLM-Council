import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class Judge(AgnetBase):
    """Judge blueprint for all council members"""
    def __init__(self, name, system_prompt, model = "gemini-2.0-flash-exp"):
        super().__init__(name, system_prompt)

        self.model = genai.GenerativeModel(
            model_name = model,
            system_instruction = system_prompt
        )
        self.chat = self.model.start_chat(history=[])



    def speak(self, conversation_history: list):
        # handle history statefully
        # raw string can be converted to coherent prompt

        # extract last message as content for the 'new input'
        last_message = conversation_history[-1]['content'] if conversation_history else "Start."

        response = self.chat.send_message(last_message)
        return response.text
