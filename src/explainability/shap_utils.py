import shap


def create_explainer(model):
    """
    Create a SHAP TreeExplainer for a tree-based model.
    """
    return shap.TreeExplainer(model)


def calculate_shap_values(explainer, X):
    """
    Calculate SHAP values for the given feature data.
    """
    return explainer(X)