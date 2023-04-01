from typing import Dict, List

from langchain.chains import loading as chains_loading

from langflow.interface.base import LangChainTypeCreator
from langflow.settings import settings
from langflow.utils.util import build_template_from_function

# Assuming necessary imports for Field, Template, and FrontendNode classes


class ChainCreator(LangChainTypeCreator):
    type_name: str = "chains"

    @property
    def type_to_loader_dict(self) -> Dict:
        if self.type_dict is None:
            self.type_dict = chains_loading.type_to_loader_dict
        return self.type_dict

    def get_signature(self, name: str) -> Dict | None:
        try:
            return build_template_from_function(
                name, self.type_to_loader_dict, add_function=True
            )
        except ValueError as exc:
            raise ValueError("Chain not found") from exc

    def to_list(self) -> List[str]:
        return [
            chain.__annotations__["return"].__name__
            for chain in self.type_to_loader_dict.values()
            if (
                chain.__annotations__["return"].__name__ in settings.chains
                or settings.dev
            )
        ]


chain_creator = ChainCreator()