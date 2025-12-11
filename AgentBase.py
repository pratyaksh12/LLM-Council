class AgnetBase:
    """Base blueprint for all council members"""
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt   

    def speak(self, conversation_history):
        raise NotImplementedError





    
        
