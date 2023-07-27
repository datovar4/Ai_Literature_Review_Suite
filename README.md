# Ai_Literature_Review_Suite
**Getting Started Guide**

1. Register for CORE API (https://core.ac.uk/services/api) and OpenAI API(https://openai.com/blog/openai-api). CORE API is neccessary for PDF search and PDF extraction and Chat GPT is currently used as the main large language model. The AI Literature suite upon first running it will ask you for these APIs and then save them as a file in the folder. Functionality for LLaMA2 coming soon!

![CORE_API](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/4b52d7bf-ddab-4b11-8723-c8f5c5c6158d)
![OpenAI_Logo svg-2](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/6f30f35b-ec17-4f2f-b37e-9861ca9f3626)


2. Clone Github
3. Set up Conda environment (for someone who does not have Conda installed)
    1. Visit the Miniconda download page at https://docs.conda.io/en/latest/miniconda.html Choose the installer that matches your operating system and download it.
       For Linux and macOS, you'll need to open a terminal to install it. For Windows, you can just run the .exe file that you downloaded.
    2. On Windows, run the installer and follow the prompts. On Linux and macOS, open a terminal and run bash with install file. For example, Miniconda3-latest-MacOSX-x86_64.sh  #macOS
    3. In terminal type: conda create --name AILitReview
    4. In terminal type: conda activate AILitReview
    5. In terminal type: conda install pip
    6. If using a Windows or Mac Intel computer, type: pip install -r requirements_win.txt
    7. If using a Mac M1 computer, type: pip install -r requirements_mac.txt
    8. Install your favorite python interpreter. Example: conda install spyder
4. Launch Python interpreter in terminal, in this case Spyder
<img width="757" alt="Screen Shot 2023-07-27 at 11 06 48 AM" src="https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/ed580c8c-859b-4a08-b606-b4d5a320e05b">

5. Navigate to MainGUI and press run. A GUI will pop up and you are ready to select one of the different modules
   
![Screen Shot 2023-07-26 at 5 22 30 PM](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/937a7c68-a961-4184-9181-f5e8eb16112e)
