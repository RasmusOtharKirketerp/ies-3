import ollama

def main():
    # Check available models
    print("Available models:")
    for model in ollama.list()['models']:
        print(f"- {model['name']}")

    # Simple chat completion
    response = ollama.chat(
        model='deepseek-r1:1.5b',  # replace with your preferred model
        messages=[{
            'role': 'user',
            'content': 'Explain quantum computing in simple terms'
        }]
    )
    
    print("\nAssistant's response:")
    print(response['message']['content'])

    # Stream response example
    print("\nStreaming response:")
    stream = ollama.chat(
        model='llama2',
        messages=[{
            'role': 'user', 
            'content': 'Tell me a short story about a robot learning to love'
        }],
        stream=True
    )
    
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure Ollama is running (ollama serve)")