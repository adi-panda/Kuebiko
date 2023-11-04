<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/thesoftdiamond/Kazushin">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Kazushin</h3>

  <p align="center">
    Kazushin, a fork of <a href="https://github.com/adi-panda/Kuebiko">this project</a>, is a Twitch Chat Bot that reads chat and generates text-to-speech responses using OpenAI API and Google Cloud API. It comes with profanity detection, and more built-in.
    <br />
    <a href="https://github.com/TheSoftDiamond/Kazushin/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/TheSoftDiamond/Kazushin/">View Demo</a>
    ·
    <a href="https://github.com/TheSoftDiamond/Kazushin/issues">Report Bug</a>
    ·
    <a href="https://github.com/TheSoftDiamond/Kazushin/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- [VLC](https://www.videolan.org/vlc/)
- [Python 3.10.0](https://www.python.org/downloads/release/python-3100/)

In order to install the prerequisites, you will need to run the following command in a command line:  
* pip
  ```sh
  pip install -r requirements.txt
  ```
  
### Installation

1. Clone the repo or fork it
   ```sh
   git clone https://github.com/TheSoftDiamond/Kazushin.git
   ```
2. Grab an OpenAI API key from [OpenAPIKey](https://openai.com/api/), and Twitch Token from [TwitchApps](https://twitchapps.com/tmi/)<br>
  2a. Strip the <b>oauth:</b> from the Twitch Token
3. Create a [Google Cloud Project with TTS Service enabled](https://cloud.google.com/) and download the JSON credentials file andd add it to root folder. See [here](https://github.com/TheSoftDiamond/Kazushin/wiki/Setting-up-Google.json) for more info.
4. Enter API Keys in creds.py:
  ```python
  # You're Twitch Token 
  TWITCH_TOKEN = ""
  # Your TWITCH Channel Name
  TWITCH_CHANNEL = ""
  # Your OpenAI API Key
  OPENAI_API_KEY = ""
  # Your Google Cloud JSON Path
  GOOGLE_JSON_PATH = ""
  ```
5. In main_usercontext.py, add api info:
```python
def send_messages_to_chat(self, textresponse):
  sendMessage = True
  my_chat = TwitchChat(oauth='BOTNAMEOAUTH', bot_name='BOTNAME', channel_name='MAINCHANNEL')
  messages = self.split_messages(textresponse)
    
  if sendMessage:
    [my_chat.send_to_chat(messageChat) for messageChat in messages]
```
6. In main_usercontext.py, change the redeem ID (you can find it [here](https://www.instafluff.tv/TwitchCustomRewardID/?channel=YOURTWITCHCHANNEL) and bot name:
```python
REDEEM_ID = 'REDEEMID'  # The ID of the specific redemption you want to monitor
AINAME = 'AINAME' # The name that will be printed in chat messages.
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features
* Separate conversations per user.
* Coversation History (last 10 messages. for every user). Can be changed.
* Profanity Filter (Can be turned on and off)
* Detect Cheers
* Post the bot's messages in chat. (Can be turned on and off)

## Usage

After finishing installing Kazunshin, you will most likely want to do some <a href="">post-installation setup</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Make the python bot have user prompt context on a per person basis.
  - [ ] Would require the user to create a file called prompt_chat_USERNAME.txt, otherwise uses default prompt if the file doesn't exist. As to prevent potential hundreds of files from being created if this feature was added..
- [ ] Ability to block a list of users from interacting with the bot in chat.

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Profanity Filter, by arhankundu99](https://github.com/arhankundu99/profanity-filter)
* [Kuebiko, by adi-panda](https://github.com/adi-panda/Kuebiko)
* [twitch_chat, by MariusPerle](https://github.com/MariusPerle/twitch_chat)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/thesoftdiamond/kazushin/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/thesoftdiamond/kazushin.svg?style=for-the-badge
[forks-url]: https://github.com/thesoftdiamond/kazushin/network/members
[stars-shield]: https://img.shields.io/github/stars/thesoftdiamond/kazushin.svg?style=for-the-badge
[stars-url]: https://github.com/thesoftdiamond/kazushin/stargazers
[issues-shield]: https://img.shields.io/github/issues/thesoftdiamond/kazushin.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.webp
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
