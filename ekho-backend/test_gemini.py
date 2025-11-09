import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    """
    Connects to Gemini and generates a test text response.
    """
    print("--- Starting Gemini Standalone Test ---")

    # 1. Load the .env file from the current directory
    load_dotenv()

    # 2. Get the API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file.")
        print("Please make sure your .env file is in the same directory as this script.")
        return

    print("✅ GEMINI_API_KEY loaded.")

    try:
        # 3. Configure the Gemini client
        genai.configure(api_key=api_key)

        # 4. Initialize the model
        # Using the model specified in the instructions for text generation
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        print("Gemini model initialized.")
        
        # 5. Define a test prompt
        test_prompt = "Hello, Gemini. In one sentence, what is the core idea of a 'future self' journal?"

        print(f"Sending prompt: '{test_prompt}'...")

        # 6. Generate the content
        response = model.generate_content(test_prompt)

        # 7. Print the response
        print("✅ Gemini response received!")
        print("---")
        print(response.text)
        print("---")
        print("--- Test Finished ---")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()