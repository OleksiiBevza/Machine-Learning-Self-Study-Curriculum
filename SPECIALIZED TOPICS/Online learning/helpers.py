######################################################################################
########################## DATA PREPROCESSING ########################################
######################################################################################

# packages for dealing with data
from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import warnings
warnings.filterwarnings('ignore')





# ------------------------------------------------------
# 1. EXTRACT RELEVANT VARIABLES
# ------------------------------------------------------
def extract_variables(x_sar_csv: str | Path) -> pd.DataFrame:
    """
    Function selects variables that are stated in a paper as significant 
    for modelling purposes

    Summing disk and network columns comes from the fact that we want to 
    see the total work the server is doing across all parts
    
    Multiplying by 512 we make bytes so that it is clear how much data i
    moving

    In `interface_util_pct` take the max cause single disk hitting 100% can 
    stop an app, while disks doing nothing
    """
    df = pd.read_csv(x_sar_csv)

    # disk data in seconds
    bytes_read_per_s = df.filter(regex=r"^dev\d+-\d+_rd_sec/s$").sum(axis=1) * 512
    bytes_written_per_s = df.filter(regex=r"^dev\d+-\d+_wr_sec/s$").sum(axis=1) * 512

    # network traffic in seconds
    rx_packets_per_s = df.filter(regex=r"^eth\d+_rxpck/s$").sum(axis=1)
    tx_packets_per_s = df.filter(regex=r"^eth\d+_txpck/s$").sum(axis=1)
    rx_kb_per_s = df.filter(regex=r"^eth\d+_rxkB/s$").sum(axis=1)
    tx_kb_per_s = df.filter(regex=r"^eth\d+_txkB/s$").sum(axis=1)

    interface_util_pct = df.filter(regex=r"^dev\d+-\d+_%util$").max(axis=1)

    return pd.DataFrame(
        {
            "TimeStamp": df["TimeStamp"],

            # CPU metrics: idle, work, waiting
            "cpu_idle_pct": df["all_%%idle"],
            "cpu_user_pct": df["all_%%usr"],
            "cpu_system_pct": df["all_%%sys"],
            "cpu_iowait_pct": df["all_%%iowait"],

            # emory and swap in kb
            "mem_used_kb": df["kbmemused"],
            "mem_committed_kb": df["kbcommit"],
            "swap_used_kb": df["kbswpused"],
            "swap_cached_kb": df["kbswpcad"],

            # transaction and block rates
            "read_trans_per_s": df["rtps"],
            "write_trans_per_s": df["wtps"],
            "bytes_read_per_s": bytes_read_per_s,
            "bytes_written_per_s": bytes_written_per_s,
            "block_reads_per_s": df["bread/s"],
            "block_writes_per_s": df["bwrtn/s"],

            # operating system performance metrics
            "new_processes_per_s": df["proc/s"],
            "context_switches_per_s": df["cswch/s"],

            # aggregated network stats
            "rx_packets_per_s": rx_packets_per_s,
            "tx_packets_per_s": tx_packets_per_s,
            "rx_kb_per_s": rx_kb_per_s,
            "tx_kb_per_s": tx_kb_per_s,
            "interface_util_pct": interface_util_pct,
        }
    )




# ------------------------------------------------------
# 2. DEFINE LABELS
# ------------------------------------------------------
def make_labels_from_Y(Y: pd.DataFrame) -> pd.DataFrame:
    """
    Function labels data wen FPS dropped below 20.
    If yes = 1, if no = 0
    """
    # make copy of original data
    y = Y.copy()
    # check every second to see if the FPS dropped below 20
    # and label it 
    y["fps_violation"] = (y["DispFrames"] < 20).astype(int)
    return y[["TimeStamp", "fps_violation"]]







# ------------------------------------------------------
# 3. DEFINE LABELS
# ------------------------------------------------------
def make_task_dataset(root: str | Path, scenario: str, W: int, H: int):
    """
    Function creates dataset by giving every metric a label like in 
    'make_labels_from_Y'
    """
    root = Path(root)

    # put together hardware metrics (X) and quality labels (Y)
    # extract only variables for modelling
    X = extract_variables(root / "X_SAR" / scenario / "X.csv")
    Y = pd.read_csv(root / "X_SAR" / scenario / "Y.csv")[["TimeStamp", "DispFrames", "noAudioPlayed"]]
    labels = make_labels_from_Y(Y)

    # put together that every hardware metric has label
    df = X.merge(labels, on="TimeStamp", how="inner")
    # make it numpy
    X_feat = df.drop(columns=["TimeStamp", "fps_violation"]).to_numpy()
    inc = df["fps_violation"].to_numpy()

    # W = look back history
    # H = look ahead prediction
    X_windows, y_targets, t_idx = [], [], []
    n = len(df)
    for t in range(W - 1, n - H):
        # if system failing now = skip
        # we wanna predict comming crash from good performance
        if inc[t] == 1:
            continue
        # take last W seconds as input 
        X_windows.append(X_feat[t - W + 1 : t + 1])
        # look ahead H seconds. If any failure give score 1
        # cause failure will occur
        y_targets.append(int(inc[t + 1 : t + H + 1].max()))
        t_idx.append(t)

    return np.asarray(X_windows), np.asarray(y_targets), np.asarray(t_idx)




# ------------------------------------------------------
# 4. TRAIN - VALIDATE - TEST SETS
# ------------------------------------------------------
def time_split_indices(n: int, train_frac: float = 0.70, val_frac: float = 0.15):
    """
    Function defines train, validate, test sets
    """
    # how many samples go into each bucket
    n_train = int(n * train_frac)
    n_val = int(n * val_frac)
    # past data to train model
    train_idx = np.arange(0, n_train)
    # validation set 
    val_idx = np.arange(n_train, n_train + n_val)
    # test set
    test_idx = np.arange(n_train + n_val, n)
    return train_idx, val_idx, test_idx




# ------------------------------------------------------
# 5. TRAIN - VALIDATE - TEST SETS
# ------------------------------------------------------
def flatten_windows(X_windows: np.ndarray) -> np.ndarray:
    """
    Takes (Number of samples, Time window, Features) and 
    reshapes them 
    """
    # X_windows: (N, W, F) -> (N, W*F)
    return X_windows.reshape(X_windows.shape[0], -1)




# ------------------------------------------------------
# 6. RESHAPE FEATURES
# ------------------------------------------------------
def summary_features(X_windows: np.ndarray) -> np.ndarray:
    """"
    Function calculates summary statistics
    """
    # X_windows: (N, W, F) -> (N, 5*F) using mean,std,min,max,last over W
    # basic stats across the time dimension (axis=1)
    mean = X_windows.mean(axis=1)
    std  = X_windows.std(axis=1)
    mn   = X_windows.min(axis=1)
    mx   = X_windows.max(axis=1)
    # take recent value in the window to capture current state
    last = X_windows[:, -1, :]
    # shape them as: (N, 5 * Features)
    return np.concatenate([mean, std, mn, mx, last], axis=1)




# ------------------------------------------------------
# 7. DEFINE THRESHOLD
# ------------------------------------------------------
def choose_threshold_fpr_cap(p_val, y_val, fpr_cap=0.01):
    """"
    Function calculates confusion matrix and defines the 
    best possible threshold.
    """
    # make inputs numpy
    p_val = np.asarray(p_val)
    y_val = np.asarray(y_val).astype(int)

    best_thr = float(p_val.max())
    best_recall = -1.0

    for thr in np.unique(p_val):
        y_hat = (p_val >= thr).astype(int)
        # calculat confusion matrix
        TP = ((y_hat == 1) & (y_val == 1)).sum()    # true positives
        FP = ((y_hat == 1) & (y_val == 0)).sum()    # false positives
        FN = ((y_hat == 0) & (y_val == 1)).sum()    # false negatives
        TN = ((y_hat == 0) & (y_val == 0)).sum()    # true negatives

        # if false positive rate (FP / total negatives) > 1%
        #ignore threshold 
        if FP / (FP + TN) > fpr_cap:
            continue

        # if threshold is good:  false positive rate < 1%
        # try to catch more positives (Recall) than  previous
        recall = TP / (TP + FN) if (TP + FN) else 0.0
        if recall > best_recall:
            best_recall = recall
            best_thr = float(thr)

    return best_thr




# ------------------------------------------------------
# 8. CALCULATE FALSE POSITIVE RATE
# ------------------------------------------------------
def fpr_at_threshold(p, y, thr):
    """
    Function calculates false positive rate
    """
    y = np.asarray(y).astype(int)
    p = np.asarray(p)
    # binary predictions (1 if prob > 1% threshold, else 0)
    y_hat = (p >= thr).astype(int)
    FP = ((y_hat == 1) & (y == 0)).sum()    # false positives
    TN = ((y_hat == 0) & (y == 0)).sum()    # true negatives
    # calculate false positive rate
    return FP / (FP + TN) if (FP + TN) else 0.0














