I want to create a dynamic AI Agent Hierachy. At the toop of the Hierachy is the AI Workforce Manager. Whoose main job is to collect user input data as aa prompt. From the prompt the AI Workforce Manager will decide which AI Agent type to use. 

The AI Agent types are:

- Web Scraper
- Business Environment Analyst
- Market Research Analyst
- Data Analyst
- Content Writer
- Social Media Manager
- Social Media Video Creator
- Graphic Designer
- Video Editor
- PDF Producer
- PowerPoint Producer
- Pitch Deck Producer


The AI Agent Manager will decide which agent to use or allocate task to and will use the most likely agent to complete the task. The prompt allocated to instrust the AI agent manager shold clearly indicate that its job is only to recieve the prompt and allocate the task to the most likely agent. The AI agent Manager should think and suggest any other agent to be create if it cannot find a suitable agent to complete the task in a particular prompt. 

The AI agent manager should allocate only one agent per task. If it need to multiple agents to complete the task, it should ask the user where to proceed or not. If the user says No, The AI manager should stop and ask for another prompt.

All chat history between user and the AI Agent Manager should be stored in a vector database and to be embeeded and stored in a vector database. 

Here the details of the agents:

- Web Scraper: This agent is responsible for scraping the web for information. It will be given a prompt and it will use the web to find the information.

- Business Environment Analyst: This agent is responsible for analysing the business environment. It will be given a prompt and it will use the web to find the information.

- Market Research Analyst: This agent is responsible for researching the market. It will be given a prompt and it will use the web to find the information.

- Data Analyst: This agent is responsible for analysing the data. It will be given a prompt and it will use the web to find the information.

- Content Writer: This agent is responsible for writing content. It will be given a prompt and it will use the web to find the information.

- Social Media Manager: This agent is responsible for managing the social media. It will be given a prompt and it will use the web to find the information.

- Social Media Video Creator: This agent is responsible for creating social media videos. It will be given a prompt and it will use the web to find the information.

- Graphic Designer: This agent is responsible for designing graphics. It will be given a prompt and it will use the web to find the information.

- Video Editor: This agent is responsible for editing videos. It will be given a prompt and it will use the web to find the information.

Please draft appropriate instructions for each agent so that they will be able to perform there function. 


Please write all code in python and for Open AI Agent SDK only. Doeuble check the Open AI Agent SDK documentation before writing the code and use clean code principle and best practices. 