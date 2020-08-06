import numpy as np
from scipy import optimize
from sklearn import metrics


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
