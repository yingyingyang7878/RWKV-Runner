from typing import Any, List, Union

try:
    import web_rwkv_py as wrp
except ModuleNotFoundError:
    try:
        from . import web_rwkv_py as wrp
    except ImportError:
        raise ModuleNotFoundError(
            "web_rwkv_py not found, install it from https://github.com/cryscan/web-rwkv-py"
        )


class RWKV:
    def __init__(self, model_path: str, strategy: str = None):
        self.model = wrp.v5.Model(
            model_path,
            turbo=False,
            quant=32 if "i8" in strategy else None,
            quant_nf4=26 if "i4" in strategy else None,
        )
        self.w = {}  # fake weight
        self.w["emb.weight"] = [0] * wrp.peek_info(model_path).num_vocab

    def forward(self, tokens: List[int], state: Union[Any, None] = None):
        return wrp.v5.run_one(self.model, tokens, state)
