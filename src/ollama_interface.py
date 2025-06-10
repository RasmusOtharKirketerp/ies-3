import ollama
from typing import Dict, Any, Optional
import re

def clean_response(text: str) -> str:
    """Remove any <think>...</think> sections from the response."""
    # Remove think blocks
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove extra newlines and whitespace
    cleaned = re.sub(r'\n\s*\n', '\n', cleaned.strip())
    return cleaned

def query_ollama(
    prompt: str,
    model: str = "deepseek-r1:1.5b",
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 40,
    context_length: int = 4096,
    stream: bool = False,
    system_prompt: Optional[str] = None,
    **kwargs: Any
) :
    """
    Send a query to Ollama with customizable parameters.
    
    Args:
        prompt: The user's input prompt
        model: Name of the Ollama model to use
        temperature: Randomness of output (0.0 to 1.0)
        top_p: Nucleus sampling threshold (0.0 to 1.0)
        top_k: Number of tokens to consider for sampling
        context_length: Maximum context length
        stream: Whether to stream the response
        system_prompt: Optional system prompt to set behavior
        **kwargs: Additional parameters to pass to Ollama
    """
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(
            model=model,
            messages=messages,
            stream=stream,
            options={
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "num_ctx": context_length,
                **kwargs
            }
        )

        if stream:
            return response
        content = response['message']['content']
        return clean_response(content)

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    response = query_ollama("Write the shortest python helloworld program")
    print(response)
