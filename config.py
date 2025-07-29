from dotenv import load_dotenv
import os 
load_dotenv()

TOKEN = os.getenv("TOKEN")
MAIN_ADMIN = int(os.getenv("MAIN_ADMIN"))
ADMIN = int(os.getenv("ADMIN"))