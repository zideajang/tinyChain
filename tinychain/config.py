import os
import uuid
import configparser

from dataclasses import dataclass


from tinychain.constants import TINYCHAIN_DIR,DEFAULT_PERSONA,DEFAULT_HUMAN,DEFAULT_PRESET
from tinychain.data_type import LLMConfig, EmbeddingConfig
from tinychain.utils import printd
# from tinychain.migrate import VERSION_CUTOFF, config_is_compatible


def get_field(config, section, field):
    if section not in config:
        return None
    if config.has_option(section, field):
        return config.get(section, field)
    else:
        return None


def set_field(config, section, field, value):
    if value is None:  # cannot write None
        return
    if section not in config:  # create section
        config.add_section(section)
    config.set(section, field, value)

@dataclass
class TinyChainConfig:
    config_path: str =  os.path.join(TINYCHAIN_DIR, "config")
    anon_clientid: str = str(uuid.UUID(int=0))

    # preset
    preset: str = DEFAULT_PRESET

    # persona parameters
    persona: str = DEFAULT_PERSONA
    human: str = DEFAULT_HUMAN

    # model parameters
    default_llm_config: LLMConfig = None

    # embedding parameters
    default_embedding_config: EmbeddingConfig = None

    # database configs: archival
    archival_storage_type: str = "tinydb"  # local, db
    archival_storage_path: str = os.path.join(TINYCHAIN_DIR, "tinydb")
    archival_storage_uri: str = None  # TODO: eventually allow external vector DB

    # database configs: recall
    recall_storage_type: str = "tinydb"  # local, db
    recall_storage_path: str = TINYCHAIN_DIR
    recall_storage_uri: str = None  # TODO: eventually allow external vector DB

    # database configs: metadata storage (sources, agents, data sources)
    metadata_storage_type: str = "sqlite"
    metadata_storage_path: str = TINYCHAIN_DIR
    metadata_storage_uri: str = None

    # database configs: agent state
    persistence_manager_type: str = None  # in-memory, db
    persistence_manager_save_file: str = None  # local file
    persistence_manager_uri: str = None  # db URI

    # version (for backcompat)
    tinychian_version: str = "1.0.0"

    # user info
    policies_accepted: bool = False

    def __post_init__(self):
        # ensure types
        # self.embedding_chunk_size = int(self.embedding_chunk_size)
        # self.embedding_dim = int(self.embedding_dim)
        # self.context_window = int(self.context_window)
        pass

    @staticmethod
    def generate_uuid() -> str:
        return uuid.UUID(int=uuid.getnode()).hex

    @classmethod
    def load(cls) -> "TinyChainConfig":
        # avoid circular import
        

        # if not config_is_compatible(allow_empty=True):
        #     error_message = " ".join(
        #         [
        #             f"\nYour current config file is incompatible with TinyChain versions later than {VERSION_CUTOFF}.",
        #             f"\nTo use TinyChain, you must either downgrade your TinyChain version (<= {VERSION_CUTOFF}) or regenerate your config using `TinyChain configure`, or `TinyChain migrate` if you would like to migrate old agents.",
        #         ]
        #     )
        #     raise ValueError(error_message)

        config = configparser.ConfigParser()

        # allow overriding with env variables
        if os.getenv("TINYCHAIN_CONFIG_PATH"):
            config_path = os.getenv("TINYCHAIN_CONFIG_PATH")
        else:
            config_path = TinyChainConfig.config_path

        # insure all configuration directories exist
        cls.create_config_dir()
        printd(f"Loading config from {config_path}")
        if os.path.exists(config_path):
            # read existing config
            config.read(config_path)

            # Handle extraction of nested LLMConfig and EmbeddingConfig
            llm_config_dict = {
                # Extract relevant LLM configuration from the config file
                "model": get_field(config, "model", "model"),
                "model_endpoint": get_field(config, "model", "model_endpoint"),
                "model_endpoint_type": get_field(config, "model", "model_endpoint_type"),
                "model_wrapper": get_field(config, "model", "model_wrapper"),
                "context_window": get_field(config, "model", "context_window"),
            }
            embedding_config_dict = {
                # Extract relevant Embedding configuration from the config file
                "embedding_endpoint": get_field(config, "embedding", "embedding_endpoint"),
                "embedding_model": get_field(config, "embedding", "embedding_model"),
                "embedding_endpoint_type": get_field(config, "embedding", "embedding_endpoint_type"),
                "embedding_dim": get_field(config, "embedding", "embedding_dim"),
                "embedding_chunk_size": get_field(config, "embedding", "embedding_chunk_size"),
            }
            # Remove null values
            llm_config_dict = {k: v for k, v in llm_config_dict.items() if v is not None}
            embedding_config_dict = {k: v for k, v in embedding_config_dict.items() if v is not None}
            # Correct the types that aren't strings
            if llm_config_dict["context_window"] is not None:
                llm_config_dict["context_window"] = int(llm_config_dict["context_window"])
            if embedding_config_dict["embedding_dim"] is not None:
                embedding_config_dict["embedding_dim"] = int(embedding_config_dict["embedding_dim"])
            if embedding_config_dict["embedding_chunk_size"] is not None:
                embedding_config_dict["embedding_chunk_size"] = int(embedding_config_dict["embedding_chunk_size"])
            # Construct the inner properties
            llm_config = LLMConfig(**llm_config_dict)
            embedding_config = EmbeddingConfig(**embedding_config_dict)

            # Everything else
            config_dict = {
                # Two prepared configs
                "default_llm_config": llm_config,
                "default_embedding_config": embedding_config,
                # Agent related
                "preset": get_field(config, "defaults", "preset"),
                "persona": get_field(config, "defaults", "persona"),
                "human": get_field(config, "defaults", "human"),
                "agent": get_field(config, "defaults", "agent"),
                # Storage related
                "archival_storage_type": get_field(config, "archival_storage", "type"),
                "archival_storage_path": get_field(config, "archival_storage", "path"),
                "archival_storage_uri": get_field(config, "archival_storage", "uri"),
                "recall_storage_type": get_field(config, "recall_storage", "type"),
                "recall_storage_path": get_field(config, "recall_storage", "path"),
                "recall_storage_uri": get_field(config, "recall_storage", "uri"),
                "metadata_storage_type": get_field(config, "metadata_storage", "type"),
                "metadata_storage_path": get_field(config, "metadata_storage", "path"),
                "metadata_storage_uri": get_field(config, "metadata_storage", "uri"),
                # Misc
                "anon_clientid": get_field(config, "client", "anon_clientid"),
                "config_path": config_path,
                # "tinychain_version": get_field(config, "version", "tinychain_version"),
            }
            # Don't include null values
            config_dict = {k: v for k, v in config_dict.items() if v is not None}

            return cls(**config_dict)

        # create new config
        anon_clientid = TinyChainConfig.generate_uuid()
        config = cls(anon_clientid=anon_clientid, config_path=config_path)
        config.create_config_dir()  # create dirs

        return config
    
    def save(self):

        config = configparser.ConfigParser()

        # CLI defaults
        set_field(config, "defaults", "preset", self.preset)
        set_field(config, "defaults", "persona", self.persona)
        set_field(config, "defaults", "human", self.human)

        # model defaults
        set_field(config, "model", "model", self.default_llm_config.model)
        set_field(config, "model", "model_endpoint", self.default_llm_config.model_endpoint)
        set_field(
            config,
            "model",
            "model_endpoint_type",
            self.default_llm_config.model_endpoint_type,
        )
        set_field(config, "model", "model_wrapper", self.default_llm_config.model_wrapper)
        set_field(
            config,
            "model",
            "context_window",
            str(self.default_llm_config.context_window),
        )

        # embeddings
        set_field(
            config,
            "embedding",
            "embedding_endpoint_type",
            self.default_embedding_config.embedding_endpoint_type,
        )
        set_field(
            config,
            "embedding",
            "embedding_endpoint",
            self.default_embedding_config.embedding_endpoint,
        )
        set_field(
            config,
            "embedding",
            "embedding_model",
            self.default_embedding_config.embedding_model,
        )
        set_field(
            config,
            "embedding",
            "embedding_dim",
            str(self.default_embedding_config.embedding_dim),
        )
        set_field(
            config,
            "embedding",
            "embedding_chunk_size",
            str(self.default_embedding_config.embedding_chunk_size),
        )

        # archival storage
        set_field(config, "archival_storage", "type", self.archival_storage_type)
        set_field(config, "archival_storage", "path", self.archival_storage_path)
        set_field(config, "archival_storage", "uri", self.archival_storage_uri)

        # recall storage
        set_field(config, "recall_storage", "type", self.recall_storage_type)
        set_field(config, "recall_storage", "path", self.recall_storage_path)
        set_field(config, "recall_storage", "uri", self.recall_storage_uri)

        # metadata storage
        set_field(config, "metadata_storage", "type", self.metadata_storage_type)
        set_field(config, "metadata_storage", "path", self.metadata_storage_path)
        set_field(config, "metadata_storage", "uri", self.metadata_storage_uri)

        # set version
        set_field(config, "version", "tinychain_version", "1.0.0")

        # client
        if not self.anon_clientid:
            self.anon_clientid = self.generate_uuid()
        set_field(config, "client", "anon_clientid", self.anon_clientid)

        # always make sure all directories are present
        self.create_config_dir()

        with open(self.config_path, "w", encoding="utf-8") as f:
            config.write(f)
        print(f"Saved Config:  {self.config_path}")

    @staticmethod
    def exists():
        # allow overriding with env variables
        if os.getenv("TINYCHAIN_CONFIG_PATH"):
            config_path = os.getenv("TINYCHAIN_CONFIG_PATH")
        else:
            config_path = TinyChainConfig.config_path

        assert not os.path.isdir(config_path), f"Config path {config_path} cannot be set to a directory."
        return os.path.exists(config_path)

    @staticmethod
    def create_config_dir():
        if not os.path.exists(TINYCHAIN_DIR):
            os.makedirs(TINYCHAIN_DIR, exist_ok=True)

        folders = [
            "personas",
            "humans",
            "archival",
            "agents",
            "functions",
            "system_prompts",
            "presets",
            "settings",
        ]

        for folder in folders:
            if not os.path.exists(os.path.join(TINYCHAIN_DIR, folder)):
                os.makedirs(os.path.join(TINYCHAIN_DIR, folder))

if __name__ == "__main__":
    config = TinyChainConfig()
