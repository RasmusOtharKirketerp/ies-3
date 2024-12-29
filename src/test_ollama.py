import ollama

def test_ollama():
    try:
        # Simple test completion
        response = ollama.chat(model='llama2', messages=[
            {
                'role': 'user',
                'content': 'Say hello!'
            }
        ])
        print("Ollama test successful!")
        print(f"Response: {response['message']['content']}")
        return True
    except Exception as e:
        print(f"Ollama test failed: {e}")
        return False

if __name__ == "__main__":
    test_ollama()
