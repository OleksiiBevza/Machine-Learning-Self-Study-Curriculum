######################################################################################
########################## ONLINE METHODS ############################################
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

# packages for modelling
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_recall_fscore_support, balanced_accuracy_score

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
)







# ------------------------------------------------------
# 1. EVALUATION
# ------------------------------------------------------
def evaluate_simple(p_test, y_test, thr):
    """
    Function evaluates results of the models
    """
    pr_auc = average_precision_score(y_test, p_test)
    y_hat = (p_test >= thr).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_hat, average="binary", zero_division=0)
    ba = balanced_accuracy_score(y_test, y_hat)
    return pr_auc, precision, recall, f1, ba








# ------------------------------------------------------
# 2. ADAPTIVE THRESHOLD USING ACTUAL ONLINE DECISIONS
# ------------------------------------------------------
class AdaptiveThreshold:
    """
    Adaptive threshold watches recent mistakes
    and adjusts threshold in real-time to keep 
    false positive rate stable around 1%
 
    """
    def __init__(
        self,
        initial_threshold: float = 0.5,
        fpr_target: float = 0.01,
        window_size: int = 200,
        adjustment_factor: float = 1.05,
        min_threshold: float = 0.2,
        max_threshold: float = 0.9,
        fpr_tolerance: float = 0.002,  # don't overreact to tiny deviations
    ):
        self.threshold = initial_threshold
        self.fpr_target = fpr_target
        self.window_size = window_size
        self.adjustment_factor = adjustment_factor
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.fpr_tolerance = fpr_tolerance

        # sliding windows care about last N samples
        self.recent_y_pred = deque(maxlen=window_size)
        self.recent_y_true = deque(maxlen=window_size)


    def get_threshold(self) -> float:
        """returns current threshol"""
        return self.threshold


    def update(self, y_pred: int, y_true: int) -> float:
        """
        updates threshold by new outcome.
        y_pred: model predicted  (0 or 1)
        y_true: ground truth (0 or 1)
        """
        # store new data point in sliding history
        self.recent_y_pred.append(int(y_pred))
        self.recent_y_true.append(int(y_true))

        # gather sample 
        if len(self.recent_y_true) < self.window_size // 2:
            return self.threshold

        # make arrays
        y_pred_arr = np.array(self.recent_y_pred)
        y_true_arr = np.array(self.recent_y_true)

        # false positives and true negatives
        fp = ((y_pred_arr == 1) & (y_true_arr == 0)).sum()
        tn = ((y_pred_arr == 0) & (y_true_arr == 0)).sum()


        # false positive rate
        if fp + tn > 0:
            current_fpr = fp / (fp + tn)
        else:
            current_fpr = 0.0

        # false positive rate error
        fpr_error = current_fpr - self.fpr_target

        # false positive rate error > threshold
        if abs(fpr_error) > self.fpr_tolerance:
            if fpr_error > 0:  # be strict
                self.threshold = min(
                    self.threshold * self.adjustment_factor, self.max_threshold
                )
        # false positive rate error < threshold
            else:  # show some empathy 
                self.threshold = max(
                    self.threshold / self.adjustment_factor, self.min_threshold
                )
        # return updated threshold        
        return self.threshold








# ---------------------------------------------------------
# 3. OAUEENSEMBLE AND WEIGHTED VOTING AND WINDOW ACCURACY
# ---------------------------------------------------------
class OAUEEnsemble:
    """
    This is for online trees.
    It tracks the performance of each tree in a sliding window.
    When accuracy < accepatble_min: replace a tree with a new.
    """
    def __init__(
        self,
        n_estimators: int = 20,
        grace_period: int = 100,        # Hoeffding Tree: samples before splitting a node
        delta: float = 1e-2,            # confidence level for split
        tau: float = 0.05,
        acc_init: float = 0.75,         # accuracy < 0.75: treee replaced
        acc_min: float = 0.55,
        acc_window_size: int = 200,     # nr recent samples to decide performance
        vote_temperature: float = 5.0,  # high number = trust best trees morre
    ):
        self.n_estimators = n_estimators
        self.acc_init = float(acc_init)
        self.acc_min = float(acc_min)
        self.acc_window_size = int(acc_window_size)
        self.vote_temperature = float(vote_temperature)

        # store tree settings
        self._tree_kwargs = dict(
            grace_period=grace_period,
            delta=delta,
            tau=tau,
        )

        from river import tree
        # initialize trees
        self.models = [
            tree.HoeffdingTreeClassifier(**self._tree_kwargs)
            for _ in range(n_estimators)
        ]

        # remember last 200 samples (1 = correct, 0 = incorrect)
        self.correct_windows = [
            deque(maxlen=self.acc_window_size)
            for _ in range(n_estimators)
        ]


    @staticmethod
    def _row_to_dict(x_row):
        """male dictionaries for rivr package"""
        if isinstance(x_row, dict):
            return {str(k): float(v) for k, v in x_row.items()}

        if hasattr(x_row, "shape"):
            x_row = np.ravel(x_row)
            return {str(i): float(v) for i, v in enumerate(x_row)}

        return {str(i): float(v) for i, v in enumerate(np.atleast_1d(x_row))}


    def _get_accuracy(self, idx: int) -> float:
        """ accuracy for for a specific tree"""
        w = self.correct_windows[idx]
        if not w:
            return self.acc_init
        return float(sum(w) / len(w))


    def _get_all_accuracies(self):
        return [self._get_accuracy(i) for i in range(self.n_estimators)]


    def _get_weights(self):
        """
        take accuracy and calculate how much you wanna trust each tree.
        give accurate trees have more power 
        """
        # define here accuracies
        accuracies = np.array(self._get_all_accuracies(), dtype=float)
        # calculate accuracies
        a_centered = accuracies - np.mean(accuracies)
        logits = self.vote_temperature * a_centered
        weights = np.exp(logits)
        weights_sum = weights.sum()
        # if all more or less equal 
        # give them equal weights
        if weights_sum <= 0:
            return np.ones_like(weights) / len(weights)
        return weights / weights_sum


    def predict_proba_one(self, x_row) -> float:
        """
        Return probability of positive class as weighted fraction of trees
        voting 1. Final decision in your pipeline is done by comparing this
        probability to the adaptive threshold.
        """
        x = self._row_to_dict(x_row)

        votes = []
        for model in self.models:
            proba = model.predict_proba_one(x)
            p1 = proba.get(1, 0.5)
            y_pred = 1 if p1 >= 0.5 else 0
            votes.append(y_pred)

        votes = np.array(votes, dtype=float)
        weights = self._get_weights()

        # Weighted fraction of positive votes
        p_hat = float(np.clip(np.sum(weights * votes), 0.01, 0.99))
        return p_hat


    def learn_one(self, x_row, y_true: int):
        """
        training the tree model
        update with one labeled example

        Each tree:
          * predicts an event
          * updates its correct window         
          * train tree on best correct prediction
          * the worst tree is replaced with new one
            if accuracy < acceptrable min defined
          * new tree is trained on current sample.
        """
        x = self._row_to_dict(x_row)
        y_true = int(y_true)

        from river import tree

        # update trees with samples
        for i, model in enumerate(self.models):
            proba = model.predict_proba_one(x)
            p1 = proba.get(1, 0.5)
            y_pred = 1 if p1 >= 0.5 else 0

            # calculate correctness
            correct = int(y_pred == y_true)
            self.correct_windows[i].append(correct)

            # train from sample 
            model.learn_one(x, y_true)

        # find worst-performing tree
        accuracies = np.array(self._get_all_accuracies(), dtype=float)
        worst_idx = int(np.argmin(accuracies))

        # replace worst tree if its accuracy < acc_min
        if accuracies[worst_idx] < self.acc_min:
            # define new tree
            new_tree = tree.HoeffdingTreeClassifier(**self._tree_kwargs)
            # train new tree on current sample 
            new_tree.learn_one(x, y_true)

            self.models[worst_idx] = new_tree
            # start new accuracy window for new tree
            self.correct_windows[worst_idx].clear() 








# ------------------------------------------------------------
# 4. PREQUENTIAL EVALUATION
# ------------------------------------------------------------ 
def evaluate_online_prequential(
    X_train,
    y_train,
    X_eval,
    y_eval,
    timestamps,
    model_class,
    model_params,
    fpr_target: float = 0.01,
    window_size: int = 200,
    initial_threshold: float = 0.5,
    adjustment_factor: float = 1.05,
):
    """
    Prequential evaluation for online models.

    Steps:
      1. Train model offline on training set (X_train, y_train).
      2. For each sample in the evaluation series (X_eval, y_eval, timestamps):
         - predict probability of the positive class
         - use current threshold and make binary choice
         - save the probability, decision, and threshold
         - update the model with the true label (online learning)
         - update the adaptive threshold using decision and true label
      3. Return all recorded probabilities, binary predictions, and thresholds.

    Parameters
    ----------
    X_train, y_train : array-like
        training data for an initial offline training 
    X_eval, y_eval : array-like
        evaluation series: validation 
    timestamps : array-like
        for rolling plots
    model_class : class
        SGDClassifier 
    fpr_target : float, default=0.01
        false positive rate for threshold 
    window_size : int, default=200
        window size for adaptive threshold to estimate recent false positive rate
    initial_threshold : float, default=0.5
        threshold for binary decision
    adjustment_factor : float, default=1.05
        used by adaptive threshold to+/- itself
    """    
    # initialize model
    if model_class == SGDClassifier:
        # data imbalanced!!! 
        classes = np.array([0, 1])
        # class_weight="balanced" changes loss function and
        # rare incidents receive  high penalty if misclassified
        cw = compute_class_weight(
            class_weight="balanced",
            classes=classes,
            y=y_train,
        )
        # dict expected by model
        cw_dict = {c: w for c, w in zip(classes, cw)}

        # SGDClassifier with log loss 
        model = SGDClassifier(
            loss="log_loss",                # logistic regression
            penalty="l2",                   # L2 regularisation        
            learning_rate="optimal",    
            class_weight=cw_dict,           # class weights from training set
            random_state=42,
        )
    else:
        model = model_class(**model_params)

    # initialize adaptive threshold 
    threshold_adapter = AdaptiveThreshold(
        initial_threshold=initial_threshold,
        fpr_target=fpr_target,
        window_size=window_size,
        adjustment_factor=adjustment_factor,
        min_threshold=0.2,  # not to big here
        max_threshold=0.9,
    )

    # offline training on train set
    if model_class == SGDClassifier:
        batch_size = 32
        # train as small batch size (as i did with variational inference)
        for i in range(0, len(X_train), batch_size):
            batch_X = X_train[i : i + batch_size]
            batch_y = y_train[i : i + batch_size]
            model.partial_fit(batch_X, batch_y, classes=classes)
    # train whole sample offline 
    else:
        for xi, yi in zip(X_train, y_train):
            model.learn_one(xi, int(yi))

    # prequential evaluation on eval series
    probabilities = []
    binary_predictions = []
    thresholds = []

    # iterate over every sample over evaluation series 
    for xi, yi_true, ts in zip(X_eval, y_eval, timestamps):
        # predict probability of positive class
        if model_class == SGDClassifier:
            prob = float(model.predict_proba(xi.reshape(1, -1))[0, 1])
        else:
            prob = float(model.predict_proba_one(xi))

        # current adaptive threshold to make binary decision
        thr = threshold_adapter.get_threshold()
        y_pred = 1 if prob >= thr else 0

        # save results 
        probabilities.append(prob)
        binary_predictions.append(y_pred)
        thresholds.append(thr)

        # update model with true label
        # THIS IS ONLINE LEARNING NOW!!!! 
        if model_class == SGDClassifier:
            # train partially in batcjes
            model.partial_fit(xi.reshape(1, -1), [yi_true])
        # or tarin in one sample
        else:
            model.learn_one(xi, int(yi_true))

        # update adaptive threshold with actual decision and true label
        threshold_adapter.update(y_pred, int(yi_true))

    return {
        "probabilities": np.array(probabilities),
        "binary_predictions": np.array(binary_predictions),
        "thresholds": np.array(thresholds),
    }









# ------------------------------------------------------
# 11. VISUALIZATION 
# ------------------------------------------------------

def rolling_far_ba(y, yhat, x, window=500):
    
    """
    Compute 
        * rolling false positive rate and 
        * balanced accuracy
    over a sliding window

    Parameters
    ----------
    y : array-like
        true binary labels (0/1).
    yhat : array-like
        predicted binary labels (0/1).
    x : array-like
        x axis values (time points) for plotting.
    window : int, default=500
        size of the sliding window which is number of samples

    Returns
    -------
    x : array-like
        the input x values 
    far : ndarray
        rolling false positive rate for each time point.
    ba : ndarray
        rolling balanced accuracy for each time point.
    """
    # input is numpy
    y = np.asarray(y).astype(int)
    yhat = np.asarray(yhat).astype(int)
    x = np.asarray(x)

    n = len(y)
    w = int(window)
    if w < 1:
        raise ValueError("window must be >= 1")

    # confusion matrix per sample
    tp = ((yhat == 1) & (y == 1)).astype(int)
    fp = ((yhat == 1) & (y == 0)).astype(int)
    tn = ((yhat == 0) & (y == 0)).astype(int)
    fn = ((yhat == 0) & (y == 1)).astype(int)

    # compute cumulative sums
    def csum(a):
        return np.concatenate([[0], np.cumsum(a)])

    tp_c, fp_c, tn_c, fn_c = csum(tp), csum(fp), csum(tn), csum(fn)

    # define start and end point for each window
    start = np.clip(np.arange(n) - w + 1, 0, n)     # left boundary 
    end = np.arange(n) + 1                          # right boundary

    # summing over window using cumulative sums 
    TP = tp_c[end] - tp_c[start]
    FP = fp_c[end] - fp_c[start]
    TN = tn_c[end] - tn_c[start]
    FN = fn_c[end] - fn_c[start]

    # compute false positive rate
    FAR = FP / np.maximum(FP + TN, 1)
    # true positive rate = Recall
    TPR = TP / np.maximum(TP + FN, 1)
    # true negative rate specificity
    TNR = TN / np.maximum(TN + FP, 1)
    # balanced accuracy
    BA  = 0.5 * (TPR + TNR)

    return x, FAR, BA


def plot_far_ba(x, far, ba, title="", fpr_cap=0.01):
    """
    plot 
        * rolling false positive rate 
        * balanced accuracy 

    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # rolling rolling false positive rate 
    axes[0].plot(x, far)
    axes[0].axhline(fpr_cap, linestyle="--")
    axes[0].set_ylim(0, 1)
    axes[0].set_xlabel("t")
    axes[0].set_ylabel("False Positive Rate")
    axes[0].set_title(f"{title} rolling False positive rate")

    # rolling balanced accuracy
    axes[1].plot(x, ba)
    axes[1].set_ylim(0, 1)
    axes[1].set_xlabel("t")
    axes[1].set_ylabel("Balanced accuracy")
    axes[1].set_title(f"{title} rolling Balanced accuracy")

    plt.tight_layout()
    plt.show()






