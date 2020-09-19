import numpy as np
import pandas as pd
from scipy import optimize
from sklearn import metrics
from statsmodels import api as sm


def power_function(x, a, b, c):
    return (a * np.power(x, b)) + c


def power_function_loss(params, x, y):
    a, b, c = params
    return power_function(x, a, b, c) - y


def calculate_curve_fit(df, x_var, y_var, loss_function, f_scale):
    x, y = df.loc[:, [x_var, y_var]].to_numpy().T

    ls_results = optimize.least_squares(
        power_function_loss,
        [1, 1, 0],
        args=(x, y),
        max_nfev=5000,
        loss=loss_function,
        f_scale=f_scale,
    )
    if ls_results.success:
        a, b, c = ls_results.x
        r2 = metrics.r2_score(y, power_function(x, a, b, c))
    else:
        a = b = c = r2 = np.nan

    return {
        "a": a,
        "b": b,
        "c": c,
        "r2": r2,
    }


def fit_robust_linear_trend(df, x_var, y_var):
    x = sm.add_constant(df[x_var])
    y = df[y_var]
    model = sm.RLM(y, x, M=sm.robust.norms.HuberT(t=1.345))
    rlm_results = model.fit()
    results = {
        "intercept": rlm_results.params[0],
        "slope": rlm_results.params[1],
        "intercept_pval": rlm_results.pvalues[0],
        "slope_pval": rlm_results.pvalues[1],
        "r2_unweighted": metrics.r2_score(y, rlm_results.fittedvalues),
        "r2_weighted": metrics.r2_score(y, rlm_results.fittedvalues, sample_weight=rlm_results.weights),
    }
    return pd.Series(results)
