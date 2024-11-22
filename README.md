# Use DeepSeek to code from requirement file.

## Usage:
1. Write a requirement .toml file, use `helloworld.toml` as example.
2. Set the following three environment variables accordingly:
  * `OPENAI_API_KEY`, your api key from deepseek
  * `OPENAI_API_URL`, I use https://api.deepseek.com/beta
  * `OPENAI_API_MODEL`, I use deepseek-chat
4. Run ```python ai_coding.py <requirement.toml>```
5. Result will be written to a file ready to execute.

## Sample requirements:
* `helloworld.toml`: a simple hello world program in Python
* `qsort.toml`: a quick sort program that sorts your inputs from command line in Python
* `askllm.toml`: a program that asks a question and gets an answer from DeepSpeed in bash script
* `ai_coder.toml`: a program that takes requirement file and generates code in Python, so this project can generate itself
