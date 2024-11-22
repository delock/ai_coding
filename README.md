# Use DeepSeek to code from requirement file.

## Usage:
1. Write a requirement .json file, use `helloworld.json` as example.
2. Set the following three environment variables accordingly:
  * `OPENAI_API_KEY`, your api key from deepseek
  * `OPENAI_API_URL`, I use https://api.deepseek.com/beta
  * `OPENAI_API_MODEL`, I use deepseek-chat
4. Run ```python ai_coding.py <requirement.json>```
5. Result will be written to a file ready to execute.
