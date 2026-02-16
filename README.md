<div align="center">

  <!--  
  <img src="https://github.com/obitouka/InstagramPrivSniffer/blob/main/img/logo.png" width="140"/>  
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Audiowide&weight=400&size=70&letterSpacing=&duration=1&pause=9&color=FF0000&center=true&multiline=true&width=470&height=160&lines=INSTAGRAM;PrivSniffer">
  </a>
  -->
  
  <table>
   <td><img src="./assets/img/logo.png" width="125"/></td>
    <td>
      <!-- Instagram -->
      <a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Audiowide&size=50&duration=1&pause=10&color=E700FF&vCenter=true&width=350&lines=INSTAGRAM&repeat=true" alt="INSTAGRAM" /></a><br>
      <!-- PrivSniffer -->
      <a href="https://git.io/typing-svg"> <img src="https://readme-typing-svg.herokuapp.com?font=Audiowide&size=50&duration=1&pause=20&color=FF0000&vCenter=true&width=320&lines=PrivSniffer&repeat=true" alt="PrivSniffer" /></a>
    </td>
  </table>

  <br>
  
  <!-- Badges Row 1 -->
  <img alt="Built with Python" src="https://img.shields.io/badge/Built_with-Python-26A5E4?logo=python&logoColor=white&style=plastic" height="30"/> <!-- PYTHON -->
  <img alt="Version" src="https://img.shields.io/badge/Version-2.4.3-D3FF00?style=plastic" height="30"/> <!-- Version -->
  <a href="https://awesome.re" title="Awesome"><img alt="Awesome" src="https://awesome.re/badge-flat.svg" height="30"/></a> <!-- Awesome -->
  <img alt="Category OSINT" src="https://img.shields.io/badge/Category-OSINT-BD00FF?style=plastic" height="30"/> <!-- Category: OSINT -->
  <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-ff0004.svg?style=plastic" height="30"/> <!-- License: MIT -->  
  <img src="https://img.shields.io/github/stars/obitouka/InstagramPrivSniffer?style=plastic&color=ffffff&labelColor=111111&logo=github" width="150"/> <!-- Stars -->
  <a href="https://t.me/voidologist"><img alt="Telegram" src="https://img.shields.io/badge/Telegram-26A5E4?style=plastic&logo=telegram&logoColor=white" width="135"/></a><!-- Telegram -->
  <a href="https://github.com/obitouka"><img alt="GitHub Profile" src="https://img.shields.io/badge/GitHub-111111?style=plastic&logo=github&logoColor=FF0000" width="103"/></a> <!-- Github -->
  <a href="mailto:obitouka@protonmail.com"><img alt="ProtonMail" src="https://img.shields.io/badge/ProtonMail-782DFF?style=plastic&logo=protonmail&logoColor=white" width="135"/></a> <!-- ProtonMail -->
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/obitouka/InstagramPrivSniffer?style=plastic&color=ffffff&labelColor=111111&logo=github" width="145"/> <!-- Forks -->
  
</div>

## DISCLAIMER  
> [!IMPORTANT]  
> Date reported: 29/06/2025  
> Meta replied: 01/07/2025  
> Tool created: 09/07/2025
> 
> I Discovered an endpoint that allowed me viewing posts from a private Instagram account revealed via collaborating with public accounts. I reported this to Meta BBP related to privacy issue but after few days Meta confirmed that this is **intended behavior** based on [Collaboration feature](https://help.instagram.com/3526836317546926). Therefore, this is **not a vulnerability**
>  
> ## **POC**
> ![POC](https://github.com/obitouka/InstagramPrivSniffer/blob/main/assets/POC/MetaResponce.png)

> [!CAUTION]  
> **Created for educational purposes only, so please use it ethically. The developer is not responsible for any misuse.**
> 
> **For any legal concerns regarding this project, please contact me directly before taking any action (read "Issues Guide" of [CONTRIBUTING.md](https://github.com/obitouka/InstagramPrivSniffer/blob/main/.github/CONTRIBUTING.md#issues-guide)).**

<br>

## FEATURE :

- **`Access private account posts` revealed via collaborating with public account**
- **Download & view media**

<br>

## INSTALLATION :   
1. **Clone the tool**  
   - Click [here](https://github.com/obitouka/InstagramPrivSniffer/archive/refs/heads/main.zip) to download the ZIP file  
   - *Or* clone the repository via command line:
     ```bash
     git clone https://github.com/obitouka/InstagramPrivSniffer.git
     ```
   
2. **Install dependencies**
   - Navigate to the repository root folder (where requirements.txt is located) in command line and run:
     ```bash
     python -m pip install -r requirements.txt
     ```
  
<br>

## USAGE :  
### View available commands
> [!TIP]
> Navigate to the `InstagramPrivSniffer` root folder in a command line and run:
> ```bash
> python main.py -h
> ```

<br>

### How to use those commands
> [!NOTE]
> You have **my permission** to test this command on **my** experimental private Insta account [@keyloggerluvr](https://www.instagram.com/keyloggerluvr) as a proof that tool works.  
>
> Use this to access private account post links
>  ```bash
>  python main.py -n keyloggerluvr
>  ```
>  Or use this to download and view post
>  ```bash
>  python main.py -d https://www.instagram.com/keyloggerluvr/p/DL47hX4olz8wRQXBQ4HAaEmba9x7nC9HCSm4M80
>  ```     

<br>

![Example](./assets/img/sample.png)

<br>

## FAQ
- **Why “No posts found” even when the account has posts?**  
Please refer [issues14](https://github.com/obitouka/InstagramPrivSniffer/issues/14)

<br>

## CONTRIBUTING : 
- Wish to contribute by adding a feature or by fixing a bug, please read the [CONTRIBUTING.md](.github/CONTRIBUTING.md) file for guidelines.   
- Want to ask a question, suggest a feature or report a bug, please read the "Issues Guide" of [CONTRIBUTING.md](https://github.com/obitouka/InstagramPrivSniffer/blob/main/.github/CONTRIBUTING.md#issues-guide) for the guidlines.

<br>

## LICENSE :
Licensed under the [MIT License](LICENSE) © 2025 [obitouka](https://github.com/obitouka).  
You are free to use, modify, and distribute this project, provided that you **give credit, include the original copyright and license notice**.
