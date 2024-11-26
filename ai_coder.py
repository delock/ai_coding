import toml
import os
import sys
from openai import OpenAI

def load_toml(file_path):
    with open(file_path, 'r') as file:
        return toml.load(file)

def generate_source_code(toml_data):
    file_section = toml_data['file']
    project_section = toml_data['project']
    
    language = file_section['language']
    description = file_section['description']
    requirements = project_section['requirements']
    specs = project_section.get('specs', {})
    hints = project_section.get('hints', {})
    
    # Determine file extension
    extension_mapping = {
        'python': 'py',
        'bash': 'sh',
        'javascript': 'js'
    }
    extension = file_section.get('extension', extension_mapping.get(language, 'txt'))
    
    # Compose prompt for LLM
    prompt = f"You are an experienced {language} developer with over 10 years of experience. You have a deep understanding of {language} and are known for writing clean, efficient, and maintainable code. Please generate the following {language} code based on the requirements and specs provided."
    
    # Use hints to guide the prompt
    if hints:
        prompt += "\n\nHints:\n"
        for key, value in hints.items():
            prompt += f"- {key}: {value}\n"
    
    # Use specs to guide the prompt
    if specs:
        prompt += "\n\nSpecs:\n"
        for key, value in specs.items():
            prompt += f"- {key}: {value}\n"
    
    prompt += f"\n\nRequirements:\n{requirements}"
    
    # Use chat prefix completion
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL"),
    )

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "`"+"``" + language + "\n", "prefix": True}
    ]
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL"),
        messages=messages,
        stop=["`"+"``\n"],
    )
    code = response.choices[0].message.content
    
    return code, file_section['name'], extension

def review_code(code):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL"),
    )

    messages = [
        {"role": "user", "content": f"Here’s code intended for task X: {code}\nCheck the code carefully for correctness, style, and efficiency, and give constructive criticism for how to improve it."}
    ]
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL"),
        messages=messages,
    )
    feedback = response.choices[0].message.content
    
    return feedback

def regenerate_code(toml_data, feedback):
    file_section = toml_data['file']
    project_section = toml_data['project']
    
    language = file_section['language']
    description = file_section['description']
    requirements = project_section['requirements']
    specs = project_section.get('specs', {})
    hints = project_section.get('hints', {})
    
    # Compose prompt for LLM
    prompt = f"You are an experienced {language} developer with over 10 years of experience. You have a deep understanding of {language} and are known for writing clean, efficient, and maintainable code. Please generate the following {language} code based on the requirements and specs provided."
    
    # Use hints to guide the prompt
    if hints:
        prompt += "\n\nHints:\n"
        for key, value in hints.items():
            prompt += f"- {key}: {value}\n"
    
    # Use specs to guide the prompt
    if specs:
        prompt += "\n\nSpecs:\n"
        for key, value in specs.items():
            prompt += f"- {key}: {value}\n"
    
    prompt += f"\n\nRequirements:\n{requirements}\n\nFeedback:\n{feedback}"
    
    # Use chat prefix completion
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL"),
    )

    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "`"+"``" + language + "\n", "prefix": True}
    ]
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL"),
        messages=messages,
        stop=["`"+"``\n"],
    )
    code = response.choices[0].message.content
    
    return code

def save_code_to_file(code, filename, extension):
    with open(f"{filename}.{extension}", 'w') as file:
        file.write(code)
    print(f"Code saved to {filename}.{extension}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python ai_coder.py <toml_file>")
        sys.exit(1)
    
    toml_file = sys.argv[1]
    toml_data = load_toml(toml_file)
    
    code, filename, extension = generate_source_code(toml_data)
    feedback = review_code(code)
    final_code = regenerate_code(toml_data, feedback)
    
    save_code_to_file(final_code, filename, extension)

if __name__ == "__main__":
    main()
