import ollama
import subprocess
import time
import sys
import os

def is_ollama_running():
    """Check if Ollama service is accessible"""
    try:
        ollama.list()
        return True
    except Exception:
        return False

def start_ollama_service():
    """Start the Ollama service in the background"""
    print("Ollama service not detected. Attempting to start...")
    
    try:
        if sys.platform == "win32":
            # Windows: Start Ollama in the background
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW
            )
        else:
            # Linux/Mac: Start Ollama in the background
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        
        # Wait for service to start
        print("Waiting for Ollama service to start", end="")
        for i in range(10):
            time.sleep(1)
            print(".", end="", flush=True)
            if is_ollama_running():
                print("\n✓ Ollama service started successfully!")
                return True
        
        print("\n✗ Ollama service failed to start within timeout.")
        return False
        
    except FileNotFoundError:
        print("✗ Ollama command not found. Please install Ollama from https://ollama.ai")
        return False
    except Exception as e:
        print(f"✗ Error starting Ollama: {e}")
        return False


def main():
    # Ensure Ollama is running
    if not is_ollama_running():
        if not start_ollama_service():
            print("Cannot proceed without Ollama service.")
            sys.exit(1)
    else:
        print("✓ Ollama service is already running")
    
    # Check/download model
    model_name = 'llama2'
    
    # Now use Ollama
    print(f"\n{'='*50}")
    print("Running inference...")
    print('='*50)

    unknown_category = "credit"
    example_data = "$32.34"

    prompt = f"""Task: Map a transaction file column header to our standard field names.

    Our standard fields:
    - transaction_type (SPENDING or INCOME)
    - price (dollar amount)
    - date (transaction date)
    - category (spending/income category)
    - description (transaction details)

    File column header: "{unknown_category}"
    Example data from this column: "{example_data}"

    Which standard field does this column map to? (respond with only the field name)"""


    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        print("\nResponse:")
        print(response['message']['content'])
        
    except Exception as e:
        print(f"Error during inference: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()