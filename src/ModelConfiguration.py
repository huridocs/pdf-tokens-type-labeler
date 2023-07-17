from dataclasses import dataclass, asdict


@dataclass
class ModelConfiguration:
    context_size: int = 4
    num_boost_round: int = 500
    num_leaves: int = 47
    bagging_fraction: float = 1
    lambda_l1: float = 0.1276297259
    lambda_l2: float = 1.6814661807
    feature_fraction: float = 0.8
    bagging_freq: int = 0
    min_data_in_leaf: int = 10
    feature_pre_filter: bool = False
    boosting_type: str = "gbdt"
    objective: str = "multiclass"
    metric: str = "multi_logloss"
    learning_rate: float = 0.1
    seed: int = 42
    num_class: int = 7
    verbose: int = -1

    def dict(self):
        return asdict(self)
