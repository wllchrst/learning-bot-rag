import os
from dotenv import load_dotenv
from app_decorator import singleton

ENVS = ["SESSION_PPT_COLUMN", "DATABASE_NAME", "GEMINI_API_KEY"]

@singleton
class EnvHelper:
    """Class for gathering and saving all env for the application """
    def __init__(self):
        load_dotenv()
        self.envs = {}

        self.gather_envs()
        self.assign_env()

    def gather_envs(self) -> bool:
        """Gather All env for the application if there is a missing value throws error

        Returns:
            bool: _description_
        """
        for env in ENVS:
            env_value = os.getenv(env)
            if env_value is None:
                raise ValueError(f'{env} has value None')

            self.envs[env] = os.getenv(env)

        return True
    
    def assign_env(self):
        self.SESSION_PPT_COLLECTION = self.envs[ENVS[0]]
        self.DATABASE_NAME = self.envs[ENVS[1]]
        self.GEMINI_API_KEY = self.envs[ENVS[2]]

EnvHelper()
