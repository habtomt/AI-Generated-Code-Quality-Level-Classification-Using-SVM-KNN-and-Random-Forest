import os
import ast
import pandas as pd
import numpy as np

from radon.complexity import cc_visit
from radon.metrics import mi_visit

from transformers import AutoTokenizer, AutoModel
import torch

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# --------------------------
# 1. AST FEATURE EXTRACTION
# --------------------------

def extract_ast_features(code):
    tree = ast.parse(code)

    num_functions = 0
    num_variables = 0
    max_depth = 0

    def visit(node, depth=0):
        nonlocal num_functions, num_variables, max_depth
        max_depth = max(max_depth, depth)

        if isinstance(node, ast.FunctionDef):
            num_functions += 1

        if isinstance(node, ast.Assign):
            num_variables += len(node.targets)

        for child in ast.iter_child_nodes(node):
            visit(child, depth + 1)

    visit(tree)

    loc = len(code.splitlines())

    return {
        "loc": loc,
        "num_functions": num_functions,
        "num_variables": num_variables,
        "max_depth": max_depth
    }

# --------------------------
# 2. RADON FEATURES
# --------------------------

def extract_radon_features(code):
    complexity = cc_visit(code)
    avg_complexity = np.mean([c.complexity for c in complexity]) if complexity else 0

    mi = mi_visit(code, True)

    return {
        "cyclomatic_complexity": avg_complexity,
        "maintainability_index": mi
    }

# --------------------------
# 3. EMBEDDING (CodeBERT)
# --------------------------

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

def get_embedding(code):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embedding

# --------------------------
# 4. DATASET BUILD
# --------------------------

def build_dataset(code_samples, labels):
    feature_list = []

    for code in code_samples:
        ast_feat = extract_ast_features(code)
        radon_feat = extract_radon_features(code)
        embedding = get_embedding(code)

        combined = list(ast_feat.values()) + list(radon_feat.values()) + list(embedding)
        feature_list.append(combined)

    return np.array(feature_list), np.array(labels)

# --------------------------
# 5. TRAIN MODEL
# --------------------------

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print(classification_report(y_test, preds))

    return model

# --------------------------
# 6. MAIN FLOW
# --------------------------

if __name__ == "__main__":
    # örnek veri (sen CSV'den okuyacaksın)
    code_samples = [
        "def add(a,b): return a+b",
        "def bad(x):\n for i in range(10):\n  for j in range(10):\n   print(i,j)"
    ]

    labels = [1, 0]  # 1=good, 0=bad

    X, y = build_dataset(code_samples, labels)
    model = train_model(X, y)