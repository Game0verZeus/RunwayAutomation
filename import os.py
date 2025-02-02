import os
import time
import pickle
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 🗂 Définition des chemins relatifs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Détecte le dossier du script
PROMPTS_FILE = os.path.join(BASE_DIR, "prompts.txt")  # Fichier des prompts
COOKIES_FILE = os.path.join(BASE_DIR, "cookies.pkl")  # Fichier des cookies

# 🌐 Configuration Selenium (REMPLACER AVEC VOS DONNÉES)
EMAIL = "VOTRE_EMAIL"
PASSWORD = "VOTRE_MOT_DE_PASSE"
LOGIN_URL = "URL_DE_CONNEXION"  # Remplacez avec l'URL de connexion à la plateforme
GENERATE_URL = "URL_DE_GENERATION"  # Remplacez avec l'URL où la génération a lieu

# 📜 Charger les prompts depuis un fichier texte
def load_prompts_from_file():
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as file:
            prompts = [line.strip() for line in file.readlines() if line.strip()]
            print(f"[{datetime.now()}] {len(prompts)} prompts chargés depuis le fichier.")
            return prompts
    except FileNotFoundError:
        print(f"❌ Erreur : Fichier des prompts introuvable ({PROMPTS_FILE}).")
        return []

# 🌍 Initialiser le navigateur avec WebDriver Manager
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())  # 🚀 Téléchargement automatique de ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# 🔐 Sauvegarder les cookies après la connexion
def save_cookies(driver):
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("✔️ Cookies sauvegardés.")

# 🔄 Charger les cookies pour éviter une reconnexion
def load_cookies(driver):
    try:
        with open(COOKIES_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("✔️ Cookies chargés.")
    except FileNotFoundError:
        print("⚠️ Fichier de cookies introuvable. Connexion normale requise.")

# 🔑 Automatiser la connexion
def login(driver):
    wait = WebDriverWait(driver, 30)
    print("🔓 Connexion en cours...")
    driver.get(LOGIN_URL)

    try:
        email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="usernameOrEmail"]')))
        email_input.send_keys(EMAIL)

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(PASSWORD)

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        login_button.click()

        wait.until(EC.url_contains("video-tools"))
        print("✅ Connexion réussie.")

        save_cookies(driver)
    except Exception as e:
        print(f"❌ Erreur pendant la connexion : {e}")
        driver.quit()
        exit()

# ✅ Vérifier si le bouton "Generate" est actif
def is_generate_button_enabled(driver):
    try:
        generate_button = driver.find_element(By.XPATH, "//button[contains(., 'Generate')]")
        return generate_button.is_enabled()
    except:
        return False

# 🚀 Générer une prompt en boucle jusqu'à soumission réussie
def generate_for_prompt(driver, prompt):
    wait = WebDriverWait(driver, 30)
    print(f"📝 Traitement du prompt : {prompt}")

    while True:  # 🔄 Réessaie tant que la prompt n'est pas soumise
        try:
            # 📥 Trouver le champ textuel et insérer la prompt
            prompt_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']")))
            prompt_field.click()
            prompt_field.clear()
            prompt_field.send_keys("\uE009a\uE003")  # CTRL+A puis DEL
            prompt_field.send_keys(prompt)
            print(f"[{datetime.now()}] ✅ Prompt collée : {prompt}")

            # ⏳ Attendre que le bouton "Generate" devienne actif
            while not is_generate_button_enabled(driver):
                print(f"[{datetime.now()}] ⏳ Bouton 'Generate' désactivé, réessai dans 5s...")
                time.sleep(5)

            # 🖱️ Cliquer sur "Generate"
            generate_button = driver.find_element(By.XPATH, "//button[contains(., 'Generate')]")
            generate_button.click()
            print(f"[{datetime.now()}] ✅ Génération envoyée avec succès.")

            return  # 🔄 Sortir de la boucle et passer à la prochaine prompt

        except Exception as e:
            print(f"[{datetime.now()}] ❌ Erreur lors de la génération. Réessai dans 5 secondes...")
            time.sleep(5)

# 🔄 Naviguer et générer pour tous les prompts
def navigate_and_generate(driver, prompts):
    driver.get(GENERATE_URL)
    time.sleep(5)  # Attendre le chargement de la page

    while True:  # 🔄 Boucle infinie
        for prompt in prompts:
            generate_for_prompt(driver, prompt)
        print(f"[{datetime.now()}] 🔄 Tous les prompts ont été traités. Recommence depuis le début.")

# 🚀 Exécuter le script
if __name__ == "__main__":
    PROMPTS = load_prompts_from_file()

    if not PROMPTS:
        print("❌ Erreur : Aucun prompt trouvé dans prompts.txt.")
        exit()

    driver = setup_driver()
    try:
        login(driver)
        navigate_and_generate(driver, PROMPTS)
    except Exception as e:
        print(f"❌ Erreur générale : {e}")
    finally:
        driver.quit()
