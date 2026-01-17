from typing import Any

from common.infrastructure.config.config import Settings
from common.infrastructure.config.database_config import DatabaseConfig
from common.infrastructure.config.llm_config import LLMConfig
from common.infrastructure.config.logger_config import LoggerConfig
from common.infrastructure.config.telegram_config import TelegramConfig
from idp.auth.infrastructure.config.auth_config import AuthConfig


class AppConfig(Settings):
    auth: AuthConfig
    db: DatabaseConfig
    llm: LLMConfig
    logger: LoggerConfig
    telegram: TelegramConfig

    def masked_dict(self) -> dict[str, Any]:
        return self.model_dump(
            mode="json",
            exclude={
                "db": {"db_pass"},
                "auth": {"secret_key", "algorithm"},
                "llm": {"api_key"},
                "telegram": {"token"},
            },
        )
