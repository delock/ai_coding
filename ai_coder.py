import toml
import os
import sys
from openai import OpenAI

# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.deepseek.com/beta")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "deepseek-chat")

# Common language to file extension mapping
LANGUAGE_EXTENSION_MAP = {
    "python": "py",
    "bash": "sh",
    "javascript": "js"
}

def load_toml(file_path):
    """Load the TOML file and return the parsed data."""
    with open(file_path, 'r') as file:
        return toml.load(file)

def generate_code(toml_data):
    """Generate the source code based on the TOML data."""
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_URL,
    )

    # Extract data from TOML
    file_section = toml_data['file']
    project_section = toml_data['project']

    name = file_section['name']
    language = file_section['language']
    description = file_section['description']
    extension = file_section.get('extension', LANGUAGE_EXTENSION_MAP.get(language, 'txt'))
    requirements = project_section['requirements']
    specs = project_section.get('specs', '')
    hints = project_section.get('hints', '')

    # Compose the prompt for the LLM
    prompt = (
        f"You are an experienced {language} developer with over 10 years of experience. "
        f"You have a deep understanding of {language} and are known for writing clean, efficient, and maintainable code. "
        f"Your task is to generate a {language} program based on the following requirements and specifications:\n"
        f"Description: {description}\n"
        f"Requirements: {requirements}\n"
        f"Specs: {specs}\n"
        f"Hints: {hints}\n"
    )

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "`"+"``" + language + "\n", "prefix": True}
    ]

    response = client.chat.completions.create(
        model=OPENAI_API_MODEL,
        messages=messages,
        stop=["`"+"``\n"],
    )

    code = response.choices[0].message.content
    return code

def review_code_with_flake8(code):
    """Review the generated code with flake8 and return the feedback."""
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp:
        temp.write(code)
        temp_path = temp.name

    try:
        result = subprocess.run(['flake8', temp_path], capture_output=True, text=True)
        feedback = result.stdout
    finally:
        os.remove(temp_path)

    return feedback

def regenerate_code_with_feedback(toml_data, original_code, feedback):
    """Regenerate the code based on the feedback from flake8."""
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_URL,
    )

    # Extract data from TOML
    file_section = toml_data['file']
    project_section = toml_data['project']

    language = file_section['language']
    requirements = project_section['requirements']
    specs = project_section.get('specs', '')
    hints = project_section.get('hints', '')

    # Compose the prompt for the LLM
    prompt = (
        f"Here’s code intended for task X: {original_code}\n"
        f"Check the code carefully for correctness, style, and efficiency, and give constructive criticism for how to improve it.\n"
        f"Feedback: {feedback}\n"
        f"Requirements: {requirements}\n"
        f"Specs: {specs}\n"
        f"Hints: {hints}\n"
    )

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "`"+"``" + language + "\n", "prefix": True}
    ]

    response = client.chat.completions.create(
        model=OPENAI_API_MODEL,
        messages=messages,
        stop=["`"+"``\n"],
    )

    code = response.choices[0].message.content
    return code

def save_code_to_file(code, file_name, extension):
    """Save the generated code to a file."""
    with open(f"{file_name}.{extension}", 'w') as file:
        file.write(code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai_coder.py <toml_file>")
        sys.exit(1)

    toml_file = sys.argv[1]
    toml_data = load_toml(toml_file)

    # Generate the initial code
    initial_code = generate_code(toml_data)

    # Review the code with flake8
    feedback = review_code_with_flake8(initial_code)

    # Regenerate the code based on the feedback
    final_code = regenerate_code_with_feedback(toml_data, initial_code, feedback)

    # Save the final code to a file
    file_section = toml_data['file']
    name = file_section['name']
    extension = file_section.get('extension', LANGUAGE_EXTENSION_MAP.get(file_section['language'], 'txt'))
    save_code_to_file(final_code, name, extension)

    print(f"Code saved to {name}.{extension}")

if __name__ == "__main__":
    main()
