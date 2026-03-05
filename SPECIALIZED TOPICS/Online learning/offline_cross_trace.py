# packages for dealing with data
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import warnings
warnings.filterwarnings('ignore')

# my helpers
from helpers import *
from online_single_trace import *


# packages for modelling offline
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# packages for modelling online
from collections import deque
from sklearn.linear_model import SGDClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    precision_recall_fscore_support,
    balanced_accuracy_score

)




def compute_binary_metrics(y_true, y_prob, thr):
    """Calculates classification performance metrics based 
       on a threshold """
    y_pred = (y_prob >= thr).astype(int)

    pr_auc = average_precision_score(y_true, y_prob)
    prec   = precision_score(y_true, y_pred, zero_division=0)
    rec    = recall_score(y_true, y_pred, zero_division=0)
    f1     = f1_score(y_true, y_pred, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    ba  = balanced_accuracy_score(y_true, y_pred)

    return {
        "pr_auc": pr_auc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "fpr": fpr,
        "ba": ba,
    }




def train_on_source(X, y):
    """Function returns dict with fitted models, thresholds and
       validation metrics for log reg and random forests
    """
    # split dataset
    train_idx, val_idx, _ = time_split_indices(len(y))
    X_train, y_train = X[train_idx], y[train_idx]
    X_val,   y_val   = X[val_idx],   y[val_idx]

    # log reg
    lr = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", max_iter=1000),
    )
    lr.fit(X_train, y_train)
    p_val_lr = lr.predict_proba(X_val)[:, 1]
    # threshold where validation FPR is < 1%
    thr_lr   = choose_threshold_fpr_cap(p_val_lr, y_val, fpr_cap=0.01)
    val_lr   = compute_binary_metrics(y_val, p_val_lr, thr_lr)

    # random forest
    rf = RandomForestClassifier(
        class_weight="balanced_subsample",
        random_state=0,
    )
    rf.fit(X_train, y_train)
    p_val_rf = rf.predict_proba(X_val)[:, 1]
    thr_rf   = choose_threshold_fpr_cap(p_val_rf, y_val, fpr_cap=0.01)
    val_rf   = compute_binary_metrics(y_val, p_val_rf, thr_rf)

    return {
        "LR": {"clf": lr, "thr": thr_lr, "val": val_lr},
        "RF": {"clf": rf, "thr": thr_rf, "val": val_rf},
    }




def fmt(val):
    return f"{val:.4f}"




def make_table_lines(train_name, test_name, res_lr, res_rf):
    """build table with results"""
    thr_lr = res_lr["thr"]
    thr_rf = res_rf["thr"]
    v_lr   = res_lr["val"]
    v_rf   = res_rf["val"]
    t_lr   = res_lr["test"]
    t_rf   = res_rf["test"]

    lines = []
    lines.append("="*70)
    lines.append(f"OFFLINE CROSS-TRACE: TRAIN ON {train_name}        TEST ON {test_name}")
    lines.append("="*70)
    lines.append(f"{'Metric':<25} {'Logistic Regression':>22} {'Random Forest':>22}")
    lines.append("-"*70)

    # Validation on train trace
    lines.append(f"{'Validation:':<25} {'':>22} {'':>22}")
    lines.append(f"{'  PR-AUC (prob)':<25} {fmt(v_lr['pr_auc']):>22} {fmt(v_rf['pr_auc']):>22}")
    lines.append(f"{'  Precision':<25} {fmt(v_lr['precision']):>22} {fmt(v_rf['precision']):>22}")
    lines.append(f"{'  Recall':<25} {fmt(v_lr['recall']):>22} {fmt(v_rf['recall']):>22}")
    lines.append(f"{'  F1':<25} {fmt(v_lr['f1']):>22} {fmt(v_rf['f1']):>22}")
    lines.append(f"{'  FPR':<25} {fmt(v_lr['fpr']):>22} {fmt(v_rf['fpr']):>22}")
    lines.append(f"{'  Balanced Acc.':<25} {fmt(v_lr['ba']):>22} {fmt(v_rf['ba']):>22}")
    lines.append(f"{'  Threshold used':<25} {fmt(thr_lr):>22} {fmt(thr_rf):>22}")
    lines.append("")

    # Test on test trace
    lines.append(f"{'Test:':<25} {'':>22} {'':>22}")
    lines.append(f"{'  PR-AUC (prob)':<25} {fmt(t_lr['pr_auc']):>22} {fmt(t_rf['pr_auc']):>22}")
    lines.append(f"{'  Precision':<25} {fmt(t_lr['precision']):>22} {fmt(t_rf['precision']):>22}")
    lines.append(f"{'  Recall':<25} {fmt(t_lr['recall']):>22} {fmt(t_rf['recall']):>22}")
    lines.append(f"{'  F1':<25} {fmt(t_lr['f1']):>22} {fmt(t_rf['f1']):>22}")
    lines.append(f"{'  FPR':<25} {fmt(t_lr['fpr']):>22} {fmt(t_rf['fpr']):>22}")
    lines.append(f"{'  Balanced Acc.':<25} {fmt(t_lr['ba']):>22} {fmt(t_rf['ba']):>22}")
    lines.append("")

    return lines



def print_two_side_by_side(lines1, lines2, width=70, sep="   "):
    """print two tables in one row"""
    n1, n2 = len(lines1), len(lines2)
    n = max(n1, n2)
    # 
    lines1 = lines1 + [""] * (n - n1)
    lines2 = lines2 + [""] * (n - n2)
    for l1, l2 in zip(lines1, lines2):
        print(f"{l1:<{width}}{sep}{l2}")



