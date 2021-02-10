import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tests.utilities_for_tests import get_data, setup_efficient_frontier
from pypfopt import plotting, risk_models, expected_returns
from pypfopt import HRPOpt, CLA, EfficientFrontier


def test_correlation_plot():
    plt.figure()
    df = get_data()

    S = risk_models.CovarianceShrinkage(df).ledoit_wolf()
    ax = plotting.plot_covariance(S, showfig=False)
    assert len(ax.findobj()) == 256
    plt.clf()
    ax = plotting.plot_covariance(S, show_tickers=False, showfig=False)
    assert len(ax.findobj()) == 136
    plt.clf()
    plt.close()


def test_dendrogram_plot():
    plt.figure()
    df = get_data()
    returns = df.pct_change().dropna(how="all")
    hrp = HRPOpt(returns)
    hrp.optimize()

    ax = plotting.plot_dendrogram(hrp, showfig=False)
    assert len(ax.findobj()) == 185
    assert type(ax.findobj()[0]) == matplotlib.collections.LineCollection
    plt.clf()

    ax = plotting.plot_dendrogram(hrp, show_tickers=False, showfig=False)
    assert len(ax.findobj()) == 65
    assert type(ax.findobj()[0]) == matplotlib.collections.LineCollection
    plt.clf()
    plt.close()


def test_cla_plot():
    plt.figure()
    df = get_data()
    rets = expected_returns.mean_historical_return(df)
    S = risk_models.exp_cov(df)
    cla = CLA(rets, S)

    ax = plotting.plot_efficient_frontier(cla, showfig=False)
    assert len(ax.findobj()) == 143
    plt.clf()

    ax = plotting.plot_efficient_frontier(cla, show_assets=False, showfig=False)
    assert len(ax.findobj()) == 161
    plt.clf()
    plt.close()


def test_cla_plot_ax():
    plt.figure()
    df = get_data()
    rets = expected_returns.mean_historical_return(df)
    S = risk_models.exp_cov(df)
    cla = CLA(rets, S)

    fig, ax = plt.subplots(figsize=(12, 10))
    plotting.plot_efficient_frontier(cla, ax=ax)
    assert len(ax.findobj()) == 143
    plt.close()
    plt.close()


def test_default_ef_plot():
    plt.figure()
    ef = setup_efficient_frontier()
    ax = plotting.plot_efficient_frontier(ef, show_assets=True)
    assert len(ax.findobj()) == 125
    plt.clf()

    # with constraints
    ef = setup_efficient_frontier()
    ef.add_constraint(lambda x: x <= 0.15)
    ef.add_constraint(lambda x: x[0] == 0.05)
    ax = plotting.plot_efficient_frontier(ef)
    assert len(ax.findobj()) == 125
    plt.clf()
    plt.close()


def test_ef_plot_utility():
    plt.figure()
    ef = setup_efficient_frontier()
    delta_range = np.arange(0.001, 100, 1)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="utility", ef_param_range=delta_range, showfig=False
    )
    assert len(ax.findobj()) == 125
    plt.clf()
    plt.close()


def test_ef_plot_risk():
    plt.figure()
    ef = setup_efficient_frontier()
    ef.min_volatility()
    min_risk = ef.portfolio_performance()[1]

    ef = setup_efficient_frontier()
    risk_range = np.linspace(min_risk + 0.05, 0.5, 50)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="risk", ef_param_range=risk_range, showfig=False
    )
    assert len(ax.findobj()) == 125
    plt.clf()
    plt.close()


def ef_plot_return():
    plt.figure()
    ef = setup_efficient_frontier()
    return_range = np.linspace(0, ef.expected_returns.max(), 50)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="return", ef_param_range=return_range, showfig=False
    )
    assert len(ax.findobj()) == 125
    plt.clf()
    plt.close()


def test_ef_plot_utility_short():
    plt.figure()
    ef = EfficientFrontier(
        *setup_efficient_frontier(data_only=True), weight_bounds=(None, None)
    )
    delta_range = np.linspace(0.001, 20, 100)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="utility", ef_param_range=delta_range, showfig=False
    )
    assert len(ax.findobj()) == 161
    plt.clf()
    plt.close()


def test_constrained_ef_plot_utility():
    plt.figure()
    ef = setup_efficient_frontier()
    ef.add_constraint(lambda w: w[0] >= 0.2)
    ef.add_constraint(lambda w: w[2] == 0.15)
    ef.add_constraint(lambda w: w[3] + w[4] <= 0.10)

    delta_range = np.linspace(0.001, 20, 100)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="utility", ef_param_range=delta_range, showfig=False
    )
    assert len(ax.findobj()) == 125
    plt.clf()
    plt.close()


def test_constrained_ef_plot_risk():
    plt.figure()
    ef = EfficientFrontier(
        *setup_efficient_frontier(data_only=True), weight_bounds=(None, None)
    )

    ef.add_constraint(lambda w: w[0] >= 0.2)
    ef.add_constraint(lambda w: w[2] == 0.15)
    ef.add_constraint(lambda w: w[3] + w[4] <= 0.10)

    # 100 portfolios with risks between 0.10 and 0.30
    risk_range = np.linspace(0.157, 0.40, 100)
    ax = plotting.plot_efficient_frontier(
        ef, ef_param="risk", ef_param_range=risk_range, show_assets=True, showfig=False
    )
    assert len(ax.findobj()) == 137
    plt.clf()
    plt.close()


def test_weight_plot():
    plt.figure()
    df = get_data()
    returns = df.pct_change().dropna(how="all")
    hrp = HRPOpt(returns)
    w = hrp.optimize()

    ax = plotting.plot_weights(w, showfig=False)
    assert len(ax.findobj()) == 197
    plt.clf()
    plt.close()


def test_weight_plot_multi():
    ef = setup_efficient_frontier()
    w1 = ef.min_volatility()
    ef = setup_efficient_frontier()
    w2 = ef.max_sharpe()

    fig, (ax1, ax2) = plt.subplots(2)
    plotting.plot_weights(w1, ax1, showfig=False)
    plotting.plot_weights(w2, ax2, showfig=False)

    assert len(fig.axes) == 2
    assert len(fig.axes[0].findobj()) == 209
    assert len(fig.axes[1].findobj()) == 209
    plt.close()


def test_weight_plot_add_attribute():
    plt.figure()

    ef = setup_efficient_frontier()
    w = ef.min_volatility()
    ax = plotting.plot_weights(w)
    ax.set_title("Test")
    assert len(ax.findobj()) == 209
    plt.close()
