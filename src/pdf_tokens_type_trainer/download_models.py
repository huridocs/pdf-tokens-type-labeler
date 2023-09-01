from huggingface_hub import hf_hub_download

pdf_tokens_type_model = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmetation",
    filename="pdf_tokens_type.model",
    revision="2605abe101cab67c3d13e21ea9e80e6e55376d62",
)

token_type_finding_config_path = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmetation",
    filename="tag_type_finding_model_config.txt",
    revision="7d98776dd34acb2fe3a06495c82e64b9c84bdc16",
)

letter_corpus_path = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmetation",
    filename="letter_corpus.txt",
    revision="da00a69c8d6a84493712e819580c0148757f466c",
)
