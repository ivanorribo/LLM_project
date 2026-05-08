from html import parser
import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

def main():
    available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
    )
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    # print("Hello from llm-project!")
    
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
   
    for _ in range(20):
        response = client.models.generate_content(model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)
        

        usage = response.usage_metadata
        if usage is None:
            raise RuntimeError("Usage metadata not found in response.")
        # if flag verbose used print extra lines to check the prompt and tokens
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        
        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError("Function call result has no parts.")
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError("Function response is None.")
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError("Function response content is None.")
                function_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            break
    else:
        print("Maximum iterations reached without a final response.")
        sys.exit(1)
if __name__ == "__main__":
    main()
