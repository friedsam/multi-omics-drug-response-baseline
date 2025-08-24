def add_drug_pathway_features(df, mapping):
    """
    mapping: dict drug_id -> dict(pathway_id -> score)
    Returns df with additional p_* columns (one per pathway).
    """
    # placeholder – safe no-op for now
    return df