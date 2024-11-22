from openai import OpenAI
import os
import sys
# import json support
import json

api_key = os.environ["OPENAI_API_KEY"]
api_url = os.environ["OPENAI_API_URL"]

client = OpenAI(api_key=api_key,
                base_url=api_url)

# read json file from command line, where the "language" field is the programming language,
# and the "requirement" field is the requirement

# a sample of the json file with python language to write hello world could be:
# {
#     "language": "python",
#     "requirements": "Write a program that prints 'Hello, World!' to the console."
# }

json_file = sys.argv[1]

with open(json_file) as f:
    data = json.load(f)
    language = data["language"]
    requirements = data["requirements"]

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
# if language is not recognized, then use the language name as extension
# dict between language and extension name
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

ext = file_ext_map.get(language, language)
output_file = json_file.replace(".json", f".{ext}")
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
