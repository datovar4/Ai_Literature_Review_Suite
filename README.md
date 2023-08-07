# Ai_Literature_Review_Suite
**Getting Started Guide**

1. Register for CORE API (https://core.ac.uk/services/api) and OpenAI API(https://openai.com/blog/openai-api). CORE API is neccessary for PDF search and PDF extraction and Chat GPT is currently used as the main large language model. The AI Literature suite upon first running it will ask you for these APIs and then save them as a file in the folder. Functionality for LLaMA2 coming soon!


![CORE_API](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/c756474f-fa50-4316-adfc-0408ef092b85)

![OpenAI_Logo svg-3](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/a685972c-2e04-4a81-a2d7-a257f17646db)



2. Clone Github
3. Set up Conda environment (for someone who does not have Conda installed)
    1. Visit the Miniconda download page at https://docs.conda.io/en/latest/miniconda.html Choose the installer that matches your operating system and download it.
       For Linux and macOS, you'll need to open a terminal to install it. For Windows, you can just run the .exe file that you downloaded.

       ![Screen Shot 2023-07-27 at 11 09 01 AM](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/fc8dbf52-ed70-4c62-bb55-0800b021cae3)

    3. On Windows, run the installer and follow the prompts. On Linux and macOS, open a terminal and run bash with install file. For example, Miniconda3-latest-MacOSX-x86_64.sh  #macOS
    4. In terminal type: conda create --name AILitReview
    5. In terminal type: conda activate AILitReview
    6. In terminal type: conda install pip
    7. If using a Windows or Mac Intel computer, type: pip install -r requirements_win.txt
    8. If using a Mac M1 computer, type: pip install -r requirements_mac.txt
    9. Install your favorite python interpreter. Example: conda install spyder
4. Launch Python interpreter in terminal, in this case Spyder
<img width="757" alt="Screen Shot 2023-07-27 at 11 06 48 AM" src="https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/67ee3d55-553f-4f9c-83c0-800640d525a4">


5. Navigate to MainGUI and press run. A GUI will pop up and you are ready to select one of the different modules
   
![Screen Shot 2023-07-26 at 5 22 30 PM](https://github.com/datovar4/Ai_Literature_Review_Suite/assets/24495304/25c567bc-1284-422b-8e12-8ab9f351d7a7)


For more information regarding the features, check out the paper: https://arxiv.org/abs/2308.02443 
If you use the AI Literature Review Suite, please cite this paper:

Tovar, D. (2023). AI Literature Review Suite. arXiv preprint arXiv:2308.02443.



