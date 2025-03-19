import os
from dotenv import load_dotenv

load_dotenv()




DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/elimu")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
