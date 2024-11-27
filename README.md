# Use LLM to code from requirement file.

## Description:
This project uses LLM to generate code from a requirement file.  The requirement file is in TOML format.  The program reads the requirement file, and generate code in the language specified in the requirement file.  The generated code is written to a file, and ready to execute.

This project is an exploration on the possibility of using LLM to write program without direct interact with code.  Tools like github copilot and cursor allows you interact with code more efficiently, but user still act as the role of *programmer*.  This project let user act as *architect* who design the program, write requirements and specifications, and let LLM to write the code.  The goal is to maintain requirement file, rather than maintain AI generated code itself.

We all want AI could take one line description from user and generate the whole project, and user would say 'ah, that's what I want'.  However this is a long way to go.  This project follows the following principle: If one level of abstraction can be used as a 99.99% reliable tool, then next level could be automated by AI.  So if Python language can be 99.99% reliable, then code generation of a small Python program can be automated by LLM.  But it still needs human to write the next level of abstraction, which is the requirement file, because the automation by LLM to generate code is not 99.99% reliable.  When we evolve, we will check whether the generated code is 99.99% reliable, and if it is, then we can automate the next level of abstraction, that is let AI generate requirement file by chat with user or product manager.

This seems in contrast with current practice that either let AI co-programming with human, or let a bunch of AI agent talk to each other to generate a project, or let AI agent divide and conquer to generate a project.  This project is more bottom up approach.  It takes what AI can do now, and seek to expand its capability by evolve little by little, and ask human to do what human must do to make sure everything is workable.

## Blogs:
* 小实验：使用DeepSeek来设计能为需求自动生成代码的代码生成器ai_coder，而且还能自我迭代！https://zhuanlan.zhihu.com/p/8471526424

## Usage:
1. Write a requirement .toml file, use `helloworld.toml` as example.
2. Set the following three environment variables accordingly:
  * `OPENAI_API_KEY`, your api key from deepseek
  * `OPENAI_API_URL`, I use https://api.deepseek.com/beta
  * `OPENAI_API_MODEL`, I use deepseek-chat
4. Run ```python ai_coding.py <requirement.toml>```
5. Result will be written to a file ready to execute.

## Directory structure
* `ai_coding.py`: the main program that generates code from requirement file
* `examples`: example requirements
* `tests`: test programs in requirement file format
* `history/iter<n>`: history of the project, this contains old `ai_coding.py` and `ai_coder.toml`.

## Examples:
Examples are under `examples/` directory.
* `helloworld.toml`: a simple hello world program in Python
* `qsort.toml`: a quick sort program that sorts your inputs from command line in Python
* `askllm.toml`: a program that asks a question and gets an answer from DeepSpeed in bash script
* `ai_coder.toml`: a program that takes requirement file and generates code in Python, so this project can generate itself

## Requirement file format:
Requirement file is in TOML format. It has the following sections:
* file section: this sections contains general information about the program
  - name: name of the program
  - language: language of the program
  - description: description of the program
  - extension(optional): file extension of the program
* project section: this section contains information about the project
  - requirements: Your requirements goes to this field, it is a single string not a list
  - specs: This fields contains specs that the program would use, for example, how to do certain action following a specification.  If you want to tell the program about a function prototype you want it to call, put it here
  - requirements: Your requirements goes to this field, it is a single string not a list
  - specs: This fields contains specs that the program would use, for example, how to do certain action following a specification.  If you want to tell the program about a function prototype you want it to call, etc. put it here.
  - hints: This fields contains things that LLM should know if it is smart enough.  If you want to tell the program about something it might get confused without, put it here.

## Feature plan
* Reflection following Andrew Ng's artical https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/?ref=dl-staging-website.ghost.io
* Multiple component support, so that one requirement file can generate multiple files
* increase stability of code generated
* Generate and launch the generated code in Docker container

## Logs
This project is evolving.  I look it as an experiment to see how far I could go without write new code except the initial bootstrap code, or at least no new hand written code beyond certain iterations.   This is the log of the project:
* 2024-11-22 morning: I created this project, and write the initial Python code.  It can be used to generate `helloworld` and soon I expand to `qsort` and `askllm`.
* 2024-11-22 afternoon: I want to know whether the program can generate itself, so I wrote `ai_coder.toml` to describe the program itself.  I use `ai_coding.py` to generate `ai_coder.py`, and the generated code can generate `helloworld.py` and `qsort.py`.
* 2024-11-24: I tried to use `ai_coder.py` to generate `ai_coder.toml`, it met some problem with handling of ```` ``` ```` in the string.  `ai_coder` would stop generate code if met "```` ``` ````" in code because it is looked as stop sign.  However ai_coder itself check for ```` ``` ```` as stop condition, so generation of itself would trigger early stop.  It is easy to fix when I wrote `ai_coding.py`, but now I have to tell `ai_coder` how to get around this in `ai_coder.toml`.  I put a hint in `ai_coder.toml` to tell `ai_coder` to use "`` ` ``"+"``` `` ```" instead of "```` ``` ````" to avoid early stop.
* 2024-11-25: Spent one hour on making a new iteration (`iter1`).  Now I want to seperate reqirements field into requirements, specs, and hints.  So requirement file will be easier to maintain or possible for auto generate requirement file in the future.  I rewrote requirement file for `ai_coder` to use the new format.  Replaced `ai_coding.py` with generated `ai_coder.py`.  I didn't write new python code in this iteration
* 2024-11-27: Tried to add reflection in ai_coder.  However it turns out that code comments given by LLM sometimes make the code generation generate worse code.  i.e. exception handling around print statement.  Finally I use flake8 as python critic for reflection I didn't yet have conclusion for use flake8 as critic.  Need to do more test and exploration on this.  Another thing I found is that LLM will get confused if there are too many requirements.  For example, initially code generator would be able to generate code according to language field in TOML file.  But when I add more requirements, sometimes it would always generate with python language.  Now I removed some requirements that is not very critical (i.e. compute cost of generation) so the code generator can focus on logic that is really important.  Let's call this `iter2`
  - Consider execute the code as a critic as well to see how it works

## Security consideration
It would eventurally comes to the question that whether we can trust AI generated code without look at them.  This is a topic that needs to be considered.  In the future, actions may need to take to ensure the generated code is safe to run, this includes:
1. Add a security check LLM for generated code
2. Run the generated code in a sandbox environment to minimize interaction with the system
