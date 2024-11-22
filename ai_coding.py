from openai import OpenAI
import os
import sys
# import toml support
import toml

api_key = os.environ["OPENAI_API_KEY"]
api_url = os.environ["OPENAI_API_URL"]

client = OpenAI(api_key=api_key,
                base_url=api_url)

# read toml file from command line, where the "language" field is the programming language,
# and the "requirement" field is the requirement

# a sample of the json file with python language to write hello world could be:
# [file]
# language="python"
# extension="py"
# [project]
# requirements="Write a program that prints 'Hello, World!' to the console."

# the toml file should be passed as argument to the script

toml_file = sys.argv[1]

file_ext_map = {
    "python": "py",
    "javascript": "html",
    "c": "c",
    "c++": "cpp",
    "java": "java",
    "ruby": "rb",
    "php": "php",
    "html": "html",
    "css": "css",
    "sql": "sql"
}

# read the toml file
with open(toml_file) as f:
    data = toml.load(f)
    language = data["file"]["language"]
    # read extenion from toml file if it is defined
    ext = data["file"].get("extension", "")
    # if language is not recognized, then use the language name as extension
    # dict between language and extension name
    if ext == "":
        ext = file_ext_map.get(language, language)
    requirements = data["project"]["requirements"]

messages = [
    {"role": "user", "content": requirements},
    {"role": "assistant", "content": f"```{language}\n", "prefix": True}
]

response = client.chat.completions.create(
    model=os.environ["OPENAI_API_MODEL"],
    messages=messages,
    stop=["```"],
)
# write the response to the console
# and also output to file with same name as the input file but with proper extension according to lanaguage
# for example '.py' for 'python', '.c' for 'c', '.js' for 'javascript', etc.
# to avoid overwriting the input file, first strip the extension if it exists, then append new extension
output_file = toml_file.replace(".toml", f".{ext}")
if output_file == toml_file:
    output_file = toml_file + f".{ext}"
with open(output_file, "w") as f:
    f.write(response.choices[0].message.content)
    print(response.choices[0].message.content)
    print(f"Output written to {output_file}")

# show token usage statistics and estimate cost
# prompt tokens cost: 0.1 CNY per million tokens
# completion tokens cost: 0.2 CNY per million tokens
completion_tokens = response.usage.completion_tokens
prompt_tokens = response.usage.prompt_tokens

# calculate the cost of the request, and print with 3 effective digits
cost = (0.1 * prompt_tokens + 0.2 * completion_tokens) / 1000000
print(f"Cost: {cost:.5f} CNY")
