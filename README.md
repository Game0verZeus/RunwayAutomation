🚀 RunwayAutomation
Automate prompt submission on RunwayML for continuous AI-generated content creation.

📌 Purpose:
This script automates the prompt submission process on RunwayML (or any similar AI platform).
It allows users to continuously generate AI-generated videos from a list of prompts, without manual intervention.

🎯 Features
✅ Automated Login – Logs into RunwayML using stored credentials.
✅ Batch Processing – Reads prompts from prompts.txt and submits them one by one.
✅ Retry Mechanism – Waits if the "Generate" button is disabled, then retries.
✅ Loop Execution – When all prompts are submitted, it restarts from the beginning.
✅ No Manual Work Needed – Set it and let it run indefinitely.

📌 Installation & Setup
1️⃣ Clone the repository
bash
Copier
Modifier
git clone https://github.com/Game0verZeus/RunwayAutomation.git
cd RunwayAutomation
2️⃣ Install dependencies
bash
Copier
Modifier
pip install selenium webdriver-manager
3️⃣ Configure the script
Open runway_automation.py
Replace the following:
"VOTRE_EMAIL" → Your RunwayML email
"VOTRE_MOT_DE_PASSE" → Your RunwayML password
"URL_DE_CONNEXION" → RunwayML login page URL
"URL_DE_GENERATION" → The generation page URL
4️⃣ Add your prompts
Open prompts.txt
Add your prompts, one per line.
Example:

css
Copier
Modifier
"A drone shot of an abandoned city with overgrown buildings, cinematic lighting."
"A futuristic AI assistant guiding a human through a neon-lit cyberpunk city."
"A close-up of an astronaut discovering an ancient alien artifact on Mars."
5️⃣ Run the script
bash
Copier
Modifier
python runway_automation.py
🚀 The bot will log in, submit prompts, and loop indefinitely.

💡 How It Works
The script logs in automatically.
It reads prompts.txt and pastes them into RunwayML's prompt field.
It waits until "Generate" is clickable, then submits the prompt.
If the button is disabled, it waits and retries.
Once all prompts are done, it restarts from the first prompt.
📌 Contribution
Want to improve the script? Feel free to fork the repository and submit pull requests.

bash
Copier
Modifier
git clone https://github.com/Game0verZeus/RunwayAutomation.git
git checkout -b new-feature
git add .
git commit -m "Added a new feature"
git push origin new-feature
📜 License
This project is released under the MIT License – you are free to use, modify, and share it.

