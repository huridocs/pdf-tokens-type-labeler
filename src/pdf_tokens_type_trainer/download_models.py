from huggingface_hub import hf_hub_download

pdf_tokens_type_model = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmentation",
    filename="pdf_tokens_type.model",
    revision="87895b77811d11d89efa71861ca7a35e1c34bf47",
)

token_type_finding_config_path = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmentation",
    filename="tag_type_finding_model_config.txt",
    revision="7d98776dd34acb2fe3a06495c82e64b9c84bdc16",
)

letter_corpus_path = hf_hub_download(
    repo_id="HURIDOCS/pdf-segmentation",
    filename="letter_corpus.txt",
    revision="da00a69c8d6a84493712e819580c0148757f466c",
)
