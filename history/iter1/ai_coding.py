import os
import toml
from openai import OpenAI

# Load environment variables
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_API_URL", "https://api.deepseek.com/beta")
model_name = os.getenv("OPENAI_API_MODEL", "deepseek-chat")

# Common language to file extension mapping
LANGUAGE_EXTENSION_MAP = {
    "python": "py",
    "bash": "sh",
    "javascript": "js"
}

def generate_code(toml_file):
    # Load the TOML file
    with open(toml_file, 'r') as file:
        config = toml.load(file)

    # Extract file section
    file_section = config.get('file', {})
    name = file_section.get('name')
    language = file_section.get('language')
    description = file_section.get('description')
    extension = file_section.get('extension', LANGUAGE_EXTENSION_MAP.get(language, 'txt'))

    # Extract project section
    project_section = config.get('project', {})
    requirements = project_section.get('requirements')
    specs = project_section.get('specs', '')
    hints = project_section.get('hints', '')

    # Create the prompt for the AI
    prompt = f"{description}\nRequirements: {requirements}\nSpecs: {specs}\nHints: {hints}"

    # Initialize OpenAI client
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    # Prepare messages for chat prefix completion
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```{language}\n", "prefix": True}
    ]

    # Generate code using chat prefix completion
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stop=["```"],
    )

    # Extract the generated code
    generated_code = response.choices[0].message.content

    # Compute cost
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    cost = (0.1 * prompt_tokens + 0.2 * completion_tokens) / 1000000

    # Print cost
    print(f"Cost of code generation: CNY {cost:.6f}")

    # Save the generated code to a file
    file_name = f"{name}.{extension}"
    with open(file_name, 'w') as file:
        file.write(generated_code)

    print(f"Code saved to {file_name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python ai_coder.py <toml_file>")
        sys.exit(1)

    toml_file = sys.argv[1]
    generate_code(toml_file)
