from pdf_features.PdfFeatures import PdfFeatures


def train(pdf_features_list: list[PdfFeatures]):

    model_configs = {
        "context_sizes": [4],
        "num_boost_rounds": [700, 800],
        "num_leaves": [31, 47, 63, 127, 191]
    }

    for context_size in model_configs["context_sizes"]:

        model_configs_for_context = {
                    "context_size": context_size,
                    "num_boost_rounds": model_configs["num_boost_rounds"],
                    "num_leaves": model_configs["num_leaves"]
                }

        lightgbm_model = LightGBM_30Features_OneHotOneLetter.get_feature_matrix(pdf_features_list, model_configs_for_context)
        lightgbm_model.train()