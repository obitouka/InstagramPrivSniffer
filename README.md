## FEATURES 
![Python](https://img.shields.io/badge/Built_with-Python-blue?logo=python&logoColor=white&style=plastic)
![Instagram](https://img.shields.io/badge/Target-Instagram-9300FF?style=plastic)
![OSINT](https://img.shields.io/badge/Category-OSINT-ff0004?style=plastic)
[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
![MIT License](https://img.shields.io/badge/License-MIT-D3FF00.svg?style=plastic)  
  
<img src="https://img.shields.io/github/stars/obitouka/InstagramPrivSniffer?style=plastic&color=ffffff&labelColor=000000&logo=github" width="100" /> <img src="https://img.shields.io/github/forks/obitouka/InstagramPrivSniffer?style=plastic&color=ffffff&labelColor=000000&logo=github" width="100" />


- Fetches a list of **collaborated media posts** from a private/public Instagram account
- Does **not** require login

<br>

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/obitouka/InstagramPrivSniffer.git
   cd InstagramPrivSniffer
   ```

2. **Install dependencies:**
   Make sure you have Python 3 installed. Then, install the required libraries using pip:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script from your terminal:
```sh
python src/privateMediaViewer.py
```
You will be prompted to enter an Instagram username. The script will then fetch and display the collaborated posts.

![Example](./img/sample.jpg)

## Building from Source

You can create a standalone executable for Windows, macOS, or Linux using `pyinstaller`. This is particularly useful for running the script on a Windows on ARM machine without needing to install Python.

1. **Install PyInstaller:**
   ```sh
   pip install pyinstaller
   ```

2. **Build the executable:**
   Run the following command in the repository's root directory:
   ```sh
   pyinstaller --onefile --name InstagramPrivSniffer src/privateMediaViewer.py
   ```
   The executable will be created in the `dist` folder.

   **Note for Windows on ARM:** To build for Windows on ARM, you must run this command on a Windows on ARM machine with a native ARM64 version of Python and PyInstaller installed.

<br>

## PROOF

You are **legally authorized** to test this tool on my private Instagram account: [@keyloggerluvr](https://www.instagram.com/keyloggerluvr).
This account is mine, and I give **full consent** for testing purposes only.
> ⚠️ Please use ethically and do not violate Instagram's Terms of Service.

<br>

## PRIVACY & LEGALITY

This tool uses **only publicly accessible data** and does **not bypass** any security mechanisms.  
It relies on the documented behavior of Instagram's [Collaboration feature](https://help.instagram.com/3526836317546926).  
Meta (Instagram) confirms that collaborative posts are **intended to be public**, even if one collaborator has a private account.

<br>

## DISCLAIMER

This project is for **educational and research purposes** only.  
The author is **not responsible for misuse**.  
Please use responsibly and follow Instagram’s Terms of Service.

<br>

## LICENSE

© 2025 [Obitouka](https://github.com/obitouka). All rights reserved.  
This tool is licensed under the **MIT License**.  
If you build upon this project, please give appropriate credit.
