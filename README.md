# LLM Council: Autonomous Multi-Agent System
Instead of a single AI model answering a prompt, a **Council** of specialized personas (Product Manager, Lead Engineer, Project Lead) debate, critique, and refine ideas autonomously.

## Key Innovation: The Dynamic Router
The core breakthrough in this project is the shift from **Scripted Execution** to **Dynamic Routing**. 

### The Old Way (Scripted)
Previously, `Main.py` hardcoded the flow:
> 1. PM speaks.
> 2. Engineer speaks.
> 3. Judge decides.

### The New Way (Autonomous)
Introduced a **Router Agent** (`Router.py`) that acts as the "Kernel" or "Scheduler" of the system.
*   **Context Aware**: The Router reads the conversation history.
*   **Decision Making**: It outputs *only* the name of the next speaker (e.g., "Lead Engineer" if a technical constraint is raised, or "Product Manager" if scope needs adjustment).
*   **Robustness**: Includes strict prompt engineering and fuzzy matching to handle LLM output quirks (e.g., stripping punctuation).


### 1. `AgentBase.py` (The Interface)
A polymorphic base class that standardizes how different models (Google Gemini or Groq Llama) communicate. All agents must implement the `speak(history)` method.

### 2. `Router.py` (The Brain)
*   **Model**: Uses a fast, low-latency model (`llama-3.1-8b-instant`).
*   **Logic**: 
    *   Input: Full conversation history.
    *   Output: Single token (Agent Name or "TERMINATE").
    *   Safety: Defaults to "Project Lead" if the LLM hallucinates an invalid name.

### 3. `Debater.py` & `Judge.py` (The Workers)
*   **Debater**: Stateless agents (using Groq) that act as "Proponents" or "Opponents".
*   **Judge**: A stateful or higher-intelligence agent (using Llama-70b via Groq) that synthesizes information and makes final decisions.

### 4. `Main.py` (The OS Loop)
The entry point is an infinite `while` loop:
```python
while True:
    next_speaker = router.speak(history)
    if "TERMINATE" in next_speaker:
        break
    agents[next_speaker].speak(history)
```

## Mimicking Human Conversation
To simulate a real meeting, uses the **ChatML Protocol**:
*   The conversation history is a list of dictionaries: `{"role": "assistant", "content": "Name: Message"}`.
*   This shared history is passed to every agent.
*   When the Router chooses "Lead Engineer", the Engineer reads the history, sees what the PM just said, and responds directly to it.

## Usage
1.  **Set Keys**: Ensure `GROQ_API_KEY` is in your `.env`.
2.  **Run**:
    ```bash
    python Main.py
    ```
3.  **Result**: The agents will converse in the terminal until they agree on a plan, and a `meeting_minutes.txt` will be generated with the final summary.

## Tech Stack
*   **Python 3.11+**
*   **Groq API**: For ultra-fast inference (Llama 3.1 8B & 70B).
*   **python-dotenv**: For secure environment management.
