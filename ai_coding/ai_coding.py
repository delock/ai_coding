import os
import sys
import toml
from openai import OpenAI


# Language to extension mapping
LANGUAGE_EXTENSIONS = {
    "python": "py",
    "bash": "sh",
    "javascript": "js",
    "java": "java",
    "c": "c",
    "cpp": "cpp",
    "go": "go",
    "rust": "rs",
    "ruby": "rb",
    "php": "php"
}


def get_extension(language):
    """Get file extension for a given language."""
    return LANGUAGE_EXTENSIONS.get(language.lower(), "txt")


def read_toml_file(file_path):
    """Read and parse the TOML file."""
    with open(file_path, 'r') as f:
        return toml.load(f)


def generate_reasoning_prompt(toml_data):
    """Generate the prompt for the reasoning API."""
    file_info = toml_data.get('file', {})
    project_info = toml_data.get('project', {})

    prompt = (
        f"You are an expert AI programmer with over 20 years of experience in "
        f"{file_info.get('language', 'programming')}. You have a PhD in "
        f"Computer Science and have won multiple coding competitions. Your "
        f"code is known for being clean, efficient, and maintainable.\n\n"
        f"I need you to generate source code for a program with the following "
        f"specifications:\n\n"
        f"Program Name: {file_info.get('name', 'Untitled')}\n"
        f"Language: {file_info.get('language', 'Unknown')}\n"
        f"Description: {file_info.get('description', 'No description provided')}\n\n"
        f"Requirements:\n"
        f"{project_info.get('requirements', 'No requirements provided')}\n\n"
        f"Additional Specifications:\n"
        f"{project_info.get('specs', 'No additional specifications')}\n\n"
        f"Hints:\n"
        f"{project_info.get('hints', 'No hints provided')}\n\n"
        f"Please analyze these requirements carefully and generate the complete "
        f"source code.\n"
        f"First, explain your thought process and approach to solving this problem.\n"
        f"Then provide the complete implementation."
    )
    return prompt


def generate_code_with_reasoner(client, prompt):
    """Generate code using the reasoning API."""
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_REASONER", "deepseek-reasoner"),
        messages=messages
    )

    return response.choices[0].message.content


def generate_final_code(client, reasoning_output):
    """Generate final code using chat prefix completion."""
    messages = [
        {"role": "user", "content": reasoning_output},
        {"role": "assistant", "content": "`"+"``python\n", "prefix": True}
    ]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL", "deepseek-chat"),
        messages=messages,
        stop=["`"+"``\n"],
    )

    return response.choices[0].message.content


def save_code_to_file(code, file_name, language):
    """Save the generated code to a file."""
    extension = get_extension(language)
    output_file = f"{file_name}.{extension}"

    with open(output_file, 'w') as f:
        f.write(code)

    return output_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_coder.py <toml_file>")
        sys.exit(1)

    toml_file = sys.argv[1]

    try:
        # Read and parse TOML file
        toml_data = read_toml_file(toml_file)
        file_info = toml_data.get('file', {})

        # Initialize OpenAI client
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_URL", "https://api.deepseek.com/beta")
        )

        # Generate reasoning output
        reasoning_prompt = generate_reasoning_prompt(toml_data)
        reasoning_output = generate_code_with_reasoner(client, reasoning_prompt)

        # Generate final code
        final_code = generate_final_code(client, reasoning_output)

        # Print outputs for debugging
        print("=== Reasoning API Output ===")
        print(reasoning_output)
        print("\n=== Final Code ===")
        print(final_code)
        print("===")

        # Save to file
        output_file = save_code_to_file(
            final_code,
            file_info.get('name', 'output'),
            file_info.get('language', 'python')
        )

        print(f"Code saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
