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
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/adi-panda/Kuebiko">
    <img src="images/logo.webp" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Kuebiko</h3>

  <p align="center">
    A Twitch Chat Bot that reads twitch chat and creates a text to speech response using google could api and openai's GPT-3 text completion model.
    <br />
    <a href="https://github.com/adi-panda/Kuebiko"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/adi-panda/Kuebiko/">View Demo</a>
    ·
    <a href="https://github.com/adi-panda/Kuebiko/issues">Report Bug</a>
    ·
    <a href="https://github.com/adi-panda/Kuebiko/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
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
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## YouTube Videl Tutorial 

[![Product Name Screen Shot][product-screenshot]](https://www.youtube.com/watch?v=EXICATDyYWI&lc=UgzyiL0K3akxPeX9U8F4AaABAgm)

This is a project to setup your very own VTuber AI similar to "Neuro-Sama".

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Python 


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

- VLC MUST BE DOWNLOADED ON YOUR COMPUTER

In order to install the prerequisites you will need to do:  
* pip
  ```sh
  pip install -r requirements.txt
  ```

### Installation

1. Get a OpenAI API Key at [OpenAPIKey](https://openai.com/api/)
2. Get a Twitch API Token at [TwitchToken](https://twitchtokengenerator.com/)
3. Create a Google Cloud Project with TTS Service enabled and download JSON credentials file. [GoogleCloud](https://cloud.google.com/)
4. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
5. Add the Google Cloud JSON file into the project folder. 
6. Enter your Twitch Username and API Token in `main.py`
   ```python
   super().__init__(token='', prefix='!', initial_channels=[''])
   ```
7. Add the name of the Google Cloud JSON File into `main.py`
   ```python
   os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
   ```
9. Add the OpenAI API Key into `chat.py`
    ```python
    openai.api_key = ""
    ```
10. Download VTube Studio and use VBAudio Cable to route audio coming from the program. 
11. Add the following script into OBS [CaptionsScript](https://gist.github.com/kkartaltepe/861b02882056b464bfc3e0b329f2f174)
12. Create a new text source for captions, and set it to read from a file, select the `output.txt` file from the project folder.
13. In the script options put the name of you're text source.
14. Set the script in transform options to scale to inner bounds, and adjust the size of the captions.
15. Enjoy! For more details watch the attatched video.
16. IN ORDER TO CHANGE THE VOICE OF YOU'RE VTUBER you will need to change the following parameters in main.py
    Here is a list of [supported voices](https://cloud.google.com/text-to-speech/docs/voices)
    
  ```python
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",
        name= "en-GB-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

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



<!-- CONTACT -->
## Contact

Your Name - [@adi_panda](https://twitter.com/adi_panda) - hello@adipanda.me

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/adi-panda/Kuebiko/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/adi-panda/Kuebiko.svg?style=for-the-badge
[forks-url]: https://github.com/adi-panda/Kuebiko/network/members
[stars-shield]: https://img.shields.io/github/stars/adi-panda/Kuebiko.svg?style=for-the-badge
[stars-url]: https://github.com/adi-panda/Kuebiko/stargazers
[issues-shield]: https://img.shields.io/github/issues/adi-panda/Kuebiko.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/adipanda/
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



### Instructions

Replace API Keys in code and add google cloud json file and program should work!
