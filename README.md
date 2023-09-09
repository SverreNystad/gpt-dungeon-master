# GPT-Dungeon-Master

<div align="center">

![GPT-dungeon-master Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/SverreNystad/gpt-dungeon-master/python-app.yml)
![GPT-dungeon-master top language](https://img.shields.io/github/languages/top/SverreNystad/gpt-dungeon-master)
![GitHub language count](https://img.shields.io/github/languages/count/SverreNystad/gpt-dungeon-master)
[![GPT-dungeon-master License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Project Version](https://img.shields.io/badge/version-0.0.3-blue)](https://img.shields.io/badge/version-0.0.1-blue)

![Alt text](<DALL·E 2023-09-09 23.10.21 - A robot in a medieval cloak sitting at the head of a stone table, with AI-driven holographic projections of a 20 sided dice, digital art.png>)


</div>

## Table of contents
1. [Introduction](#Introduction)
2. [Setup](#Setup)
3. [Usage](#Usage)
4. [Tests](#Tests)
5. [Repository structure](#Repository-structure)

Welcome to the GPT Dungeon Master repository! This project harnesses the power of GPT models to create a dynamic and responsive Dungeon Master (DM) for tabletop role-playing games (RPGs). Whether you're a seasoned player looking for a quick rule reference or a group in need of an AI-driven DM for your next adventure, the GPT Dungeon Master is here to guide you.

## Features
**Knowledgebase Integration:** Access a vast digital library of RPG rulebooks. Get instant answers to rule queries, character abilities, and more.
**Dynamic Storytelling:** Let the GPT model craft intricate narratives, describe vivid settings, and generate unexpected plot twists.
**Rule Enforcement:** Ensure your gameplay adheres to the rules. The system checks player actions against the rulebook, ensuring a fair and consistent gaming experience.
**Interactive UI:** Engage with the GPT DM through a user-friendly interface. Input actions, ask questions, and immerse yourself in the game.



## Installation

### Prerequisites
- Python 3.6 or higher
- OpenAI API key (https://platform.openai.com/account/api-keys)
  

### Setup
1. Clone the repository
```bash
git clone https://github.com/SverreNystad/gpt-dungeon-master.git
cd gpt-dungeon-master
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Create a file called `.env` in the root directory of the project. Add the following lines to the file:
```bash
touch .env
echo "OPENAI_API_KEY=YOUR_API_KEY" > .env # Remember to change YOUR_API_KEY to your actual API key
```
