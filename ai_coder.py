import toml
import os
import sys
from openai import OpenAI

def load_toml(file_path):
    """Load the TOML file and return the parsed data."""
    with open(file_path, 'r') as file:
        return toml.load(file)

def get_file_extension(language):
    """Get the file extension based on the programming language."""
    language_extension_map = {
        "python": "py",
        "bash": "sh",
        "javascript": "js"
    }
    return language_extension_map.get(language, language)

def generate_code(toml_data):
    """Generate the source code based on the TOML data."""
    file_section = toml_data['file']
    project_section = toml_data['project']

    # Extract necessary fields
    name = file_section['name']
    language = file_section['language']
    description = file_section['description']
    extension = file_section.get('extension', get_file_extension(language))
    requirements = project_section['requirements']
    specs = project_section.get('specs', {})
    hints = project_section.get('hints', {})

    # Prepare the prompt for the LLM
    prompt = (f"You are an experienced {language} developer with over 10 years of experience. "
              f"You have a deep understanding of {language} and are known for writing clean, efficient, and maintainable code. "
              f"Your task is to generate a {language} program based on the following requirements and specifications:\n\n"
              f"Description: {description}\n"
              f"Requirements: {requirements}\n"
              f"Specs: {specs}\n")

    # Use hints to guide the LLM
    if hints:
        prompt += f"Hints: {hints}\n"

    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL", "https://api.deepseek.com/beta"),
    )

    # Prepare messages for chat prefix completion
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "`"+"``python\n", "prefix": True}
    ]

    # Generate the code
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL", "deepseek-chat"),
        messages=messages,
        stop=["`"+"``\n"],
    )

    # Extract the generated code
    generated_code = response.choices[0].message.content

    # Save the generated code to a file
    output_file = f"{name}.{extension}"
    with open(output_file, 'w') as file:
        file.write(generated_code)

    print(f"Code saved to {output_file}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai_coder.py <toml_file>")
        sys.exit(1)

    toml_file = sys.argv[1]
    toml_data = load_toml(toml_file)
    generate_code(toml_data)

if __name__ == "__main__":
    main()
