<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="/README_DATA/search-house.png" alt="Bot logo"></a>
</p>
<h3 align="center">List_House_Search</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> 🤖 Telegram bot - be the first to receive new notifications about house rentals on the <a href=https://list.am> list.am </a> website.
    <br>
</p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [🧐 About ](#-about-)
- [💭 How it works ](#-how-it-works-)
- [🎈 Usage ](#-usage-)
- [🏁 Getting Started ](#-getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installing](#installing)
- [🚀 Deploying your own bot ](#-deploying-your-own-bot-)
- [✍️ Authors ](#️-authors-)


## 🧐 About <a name = "about"></a>

List.am posts about house rentals come up quite often, and there isn't always a chance to keep track of them in time.\
The bot allows you to receive notifications about new house rental listings, filtering them based on your specified criteria.\
You can change these filters at any time.\
Additionally, you can request not to be notified about updated listings that you've already received. \
(Listings on the website are sorted by update date, and landlords often make minor changes to keep their listings at the top of the search results.)

## 💭 How it works <a name = "working"></a>

Every half an hour, the parser collects data on new house rental listings on list.am, adding the listings to your local SQLite database. \
The database consists of three tables (you can view its SQL structure in the file schema.sql): \
a table for listings (updated every half an hour), \
a table for bot users (to store user IDs and user-configured filters), \
and a table for the IDs of listings sent to specific users (to avoid sending duplicate listings). 

The bot is deployed in a Docker container, and the SQLite database provides local storage (to ensure its persistence in case the Docker \
container stops working) and is connected to the Docker container as a <a href=https://docs.docker.com/storage/volumes/>volume</a>.

The final workflow looks like this:

    The parser runs every half an hour:
    1.1. It finds the latest update/publication date in the listings table.
    1.2. It gathers information about listings from all pages of list.am with dates later than the one obtained from 
    the database.
    1.3. It adds the listings to the database table.
    1.4. For each saved user, it finds their filters in the database.
    1.5. If the found listings match the user (based on filters), it sends the listing to the user's Telegram chat.

    The Telegram bot operates in infinity polling mode:
    2.1. A user can change filters at any time in dialogue with the Telegram bot; new filters are immediately saved 
    to the corresponding database table for the user. In the next iteration of the parser, the user will receive 
    listings based on the new filters.

The entire bot is written in Python 3.10.12 \
Utilizes <a href=https://python-poetry.org/>Poetry</a> as a package manager for Python. \
The scheduler for the parser utilizes <a href=https://pypi.org/project/APScheduler/>apscheduler</a>. \
The parser utilizes <a href=https://pypi.org/project/beautifulsoup4/>beautifulsoup4</a> and <a href=https://pypi.org/project/lxml/>lxml</a> for parsing HTML code \
The <a href=https://pypi.org/project/Brotli/>brotli</a> package is used for decompressing data from the website.\
<a href=https://pypi.org/project/pydantic/>Pydantic</a> is used for data normalization and verification before working with the database.\
The library <a href=https://pypi.org/project/requests/>requests</a> is used for accessing the website with fake HTTP headers and a <a href=https://requests.readthedocs.io/en/latest/user/advanced/>session</a> mechanism to preserve cookies between requests.\
Environment variables (Telegram bot token and log level) are loaded from the .env file using <a href=https://pypi.org/project/dotenv/>dotenv</a>. \
The database used is SQLite and the sqlite3 package.
The Telegram bot utilizes the <a href=https://pytba.readthedocs.io/en/latest/>pyTelegramBotAPI</a> library.

The project structure:\
\
LIST_PARSER\
├── 01create_database.sh\
├── 02run_docker_container.sh\
├── database.py\
├── Dockerfile\
├── list_am_parser.py\
├── logger_config.py\
├── main.py\
├── Makefile\
├── normalization_validation.py\
├── poetry.lock\
├── pyproject.toml\
├── README.md\
├── schema.sql\
├── telegram_bot\
│   ├── callback_handler.py\
│   ├── command_handler.py\
│   ├── \_\_init\_\_.py\
│   ├── keyboard_markups.py\
│   └── message_handler.py\
|\
└── test\
    ├── database_dump.sql\
    ├── \_\_init\_\_.py\
    └── test.py\

Here:

01create_database.sh - Script for making a local database.\
02run_docker_container.sh - Script for starting a Docker container.\
database.py - Code for interacting with the database.\
list_am_parser.py - Main logic for the parser.\
logger_config.py - Logging configuration\
main.py - Entry point\
normalization_validation.py - Data normalization and validation logic\
schema.sql - SQL schema for the database\
telegram_bot - Directory containing Telegram bot logic


## 🎈 Usage <a name = "usage"></a>
Find this bot on Telegram by its name
`@List_House_Search_bot`
To use the bot, type:
`\start`

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

A Linux machine with: (All examples for ubuntu) 

1. curl:
   
`sudo apt install curl`

2. Docker:

https://docs.docker.com/engine/install/ubuntu/ 

3. Git:
   
`sudo apt install git-all` 

4. SQLite3:
   
`sudo apt install sqlite3`

5. Telegram bot token from
   
https://core.telegram.org/bots/features#creating-a-new-bot


### Installing

1. Get a copy of the GitHub repository on your machine

```
git clone https://github.com/la-strole/list_parser.git
```

2. Set up the Poetry package manager by running the installation command

```
curl -sSL https://install.python-poetry.org | python3 -
```

3. Make sure all the project's dependencies are installed by running 'poetry install'

```
~/.local/bin/poetry install --no-root
```

4. Set up the SQLite database by executing the installation script.

```
./01create_database.sh
```

5. To create your virtual environment variables, you'd make a file named `.env` \
and add the variables "TLG_BOT_TOKEN" and "LOG_LEVEL".

```
TLG_BOT_TOKEN=<YOUR_TOKEN>
LOG_LEVEL=DEBUG (OR INFO|WARNING|ERROR)
```

6. To run your bot you'd execute the command:

```
~/.local/bin/poetry run python main.py
```

## 🚀 Deploying your own bot <a name = "deployment"></a>

Deploy the bot as a Docker container, \
ensuring it's connected to an external SQLite database by mounting it as a volume.

1. Fetch the source code of this project to your server by running 'git clone' followed by the repository's URL

3. Create a local database on your server by executing the 01create_database.sh script:

```
./01create_database.sh
```
3. Build the Docker image on your server for this project: 
```
sudo docker build . -t litst_parser
```
4. Start the Docker container with the `./02run_docker_container.sh` command, \
and don't forget to adjust the Docker logging configuration in the `02run_docker_container.sh` script.
5. Here are GET parameters:
```
<https://www.list.am/ru/category/63>? - renting houses through / page number for the second (<https://www.list.am/category/63/2>)
n=0& - area and neighborhood (1-Yerevan, 2, etc. Achapnyak Arabkir Avan Davitashen Erebuni Zeytun Kanaker Kentron Malatia Sebastia Nor Nork Shengavit Nork Marash Nubarashen). disallow by robots.txt
cmtype=1& (2) - individual/company - disallow by robots.txt
sid=0& - category (house-365, townhouse-366, cottage-367).
price1=& - price from disallow by robots.txt
price2=& - price to disallow by robots.txt
crc=& - currency 0 - AMD, 1 - USD
_a5=0&
_a136_1=& - area from
_a136_2=& - area to
_a34=0& - floors (1-4)
_a4=0& - rooms count (1-8) you can use multiple separated by %2C
_a37=0& - toilet count (1-3) you can use multiple separated by %2C
_a78=0& - furniture (1-yes, 2-no, 3-partial, 4-by agreement) you can use multiple separated by %2C
_a76=0& - garage (1-no, 2-one spot, 3-two, 4 - three or more)
_a38=0& - house renovation (1-no, 2-old, 3-partial, 4-cosmetic, 5-European, 6-designer, 7-major) you can use multiple separated by %2C
_a83=0& - facilities
_a75=0& - household appliances
_a35_1=& - land area from
_a35_2=& - land area to
_a68=0& - children allowed (1-no, 2-yes, 3-by agreement)
_a69=0& - animals allowed (1-no, 2-yes, 3-by agreement)
gl=1 - 1 gallery, 2 - list
```
## ✍️ Authors <a name = "authors"></a>

+ [@la-strole](https://github.com/la-strole) - Idea & Initial work


