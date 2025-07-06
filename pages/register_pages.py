# This module handles registration of all pages for the Dash app layout dict.

def register_borrowing_saving():
    from pages.borrowing_saving import (
        borrowing_saving_home,
        retirement_planning,
        npv,
        irr,
        inflation,
        amortization,
        amortization_schedules,
        retirement_planning_sim,
        two_stage,
        _npv,
        _irr,
        _retirement_planning_sim,
        _retirement_planning,
        _amortization,
        _amortization_schedules,
    )
    pages = {
        "/borrowing-saving/borrowing-saving-home": borrowing_saving_home.layout,
        "/borrowing-saving/retirement-planning-sim": retirement_planning_sim.layout,
        "/borrowing-saving/retirement-planning": retirement_planning.layout,
        "/borrowing-saving/npv": npv.layout,
        "/borrowing-saving/irr": irr.layout,
        "/borrowing-saving/inflation": inflation.layout,
        "/borrowing-saving/amortization": amortization.layout,
        "/borrowing-saving/amortization-schedule": amortization_schedules.layout,
        "/borrowing-saving/two-stage": two_stage.layout,
        "/borrowing-saving/_npv": _npv.layout,
        "/borrowing-saving/_irr": _irr.layout,
        "/borrowing-saving/_retirement_planning_sim": _retirement_planning_sim.layout,
        "/borrowing-saving/_retirement_planning": _retirement_planning.layout,
        "/borrowing-saving/_amortization": _amortization.layout,
        "/borrowing-saving/_amortization-schedules": _amortization_schedules.layout,
    }
    return pages

def register_fixed_income():
    from pages.bonds import (
        bonds_home,
        termstructure,
        creditspreads,
        prices_yields,
        tips,
        clean_dirty,
        real_termstructure,
        clean_dirty_paths,
    )
    from pages.fixed_income import (
        duration_risk,
        duration,
        term_structure_movements,
        principal_components,
        spot_forward,
        rate_tree,
        embedded_option,
    )
    pages = {
        "/fixed-income/fixed-income-home": bonds_home.layout,
        "/fixed-income/termstructure": termstructure.layout,
        "/fixed-income/creditspreads": creditspreads.layout,
        "/fixed-income/prices-yields": prices_yields.layout,
        "/fixed-income/tips": tips.layout,
        "/fixed-income/clean-dirty": clean_dirty.layout,
        "/fixed-income/real-termstructure": real_termstructure.layout,
        "/fixed-income/clean-dirty-paths": clean_dirty_paths.layout,
        "/fixed-income/duration": duration.layout,
        "/fixed-income/duration-risk": duration_risk.layout,
        "/fixed-income/termstructure-movements": term_structure_movements.layout,
        "/fixed-income/principal-components": principal_components.layout,
        "/fixed-income/spot-forward": spot_forward.layout,
        "/fixed-income/rate-tree": rate_tree.layout,
        "/fixed-income/oas": embedded_option.layout,
    }
    return pages

def register_risk():
    from pages.risk import (
        risk_home,
        geometric,
        continuous_compounding,
        long_run_risk,
        simulation,
        returns,
        best_worst,
        frequencies,
        volatilities,
        sbb,
        sbb_real,
        correlations,
        asset_classes,
    )
    pages = {
        "/risk/risk-home": risk_home.layout,
        "/risk/asset-classes": asset_classes.layout,
        "/risk/simulation": simulation.layout,
        "/risk/continuous-compounding": continuous_compounding.layout,
        "/risk/geometric": geometric.layout,
        "/risk/correlations": correlations.layout,
        "/risk/sbb": sbb.layout,
        "/risk/sbb-real": sbb_real.layout,
        "/risk/long-run": long_run_risk.layout,
        "/risk/best-worst": best_worst.layout,
        "/risk/frequencies": frequencies.layout,
        "/risk/volatilities": volatilities.layout,
        "/risk/returns": returns.layout,
    }
    return pages

def register_portfolios():
    from pages.portfolios import (
        portfolios_home,
        two_assets,
        short_sales,
        three_assets,
        riskfree,
        diversification,
        optimal_sb,
        short_sales_constraints,
        sharpe,
        optimal,
        tangency,
        optimal_yahoo,
        optimal_N,
        preferences,
        optimal_two_rates,
        frontier,
    )
    pages = {
        "/portfolios/portfolios-home": portfolios_home.layout,
        "/portfolios/short-sales": short_sales.layout,
        "/portfolios/optimal": optimal.layout,
        "/portfolios/frontier": frontier.layout,
        "/portfolios/preferences": preferences.layout,
        "/portfolios/tangency": tangency.layout,
        "/portfolios/sharpe": sharpe.layout,
        "/portfolios/risk-free": riskfree.layout,
        "/portfolios/optimal-yahoo": optimal_yahoo.layout,
        "/portfolios/two-assets": two_assets.layout,
        "/portfolios/optimal-two-rates": optimal_two_rates.layout,
        "/portfolios/three-assets": three_assets.layout,
        "/portfolios/optimal-sb": optimal_sb.layout,
        "/portfolios/diversification": diversification.layout,
        "/portfolios/short-sales-constraints": short_sales_constraints.layout,
        "/portfolios/optimal-N": optimal_N.layout,
    }
    return pages

def register_capm():
    from pages.capm import (
        capm_home,
        alphas_betas,
        capm_costequity,
        alphas_mve,
        alphas_sharpes,
        sml_industries,
        mrp_estimation,
        two_way_capm
    )
    pages = {
        "/capm/capm-home": capm_home.layout,
        "/capm/sml-industries": sml_industries.layout,
        "/capm/costequity": capm_costequity.layout,
        "/capm/alphas-mve": alphas_mve.layout,
        "/capm/alphas-sharpes": alphas_sharpes.layout,
        "/capm/mrp_estimation": mrp_estimation.layout,
        "/capm/alphas-betas": alphas_betas.layout,
        "/capm/two-way-capm": two_way_capm.layout,
    }
    return pages

def register_factor_investing():
    from pages.factor_investing import (
        quintiles,
        two_way_sorts,
        ff_costequity,
        ff_characteristics,
        factor_investing_home,
    )
    pages = {
        "/factor-investing/factor-investing-home": factor_investing_home.layout,
        "/factor-investing/ff-costequity": ff_costequity.layout,
        "/factor-investing/ff-characteristics": ff_characteristics.layout,
        "/factor-investing/quintiles": quintiles.layout,
        "/factor-investing/two-way-sorts": two_way_sorts.layout,
    }
    return pages

def register_topics():
    from pages.performance_evaluation import (
        performance_evaluation_home, 
        funds, 
        market_timing
    )
    from pages.taxes import (
        tax_vehicles, 
        tax_location_detail, 
        tax_location_compare, 
        marginal_tax_rates
    )
    pages = {
        "/performance-evaluation/performance-evaluation-home": performance_evaluation_home.layout,
        "/performance-evaluation/funds": funds.layout,
        "/performance-evaluation/market_timing": market_timing.layout,
        "/taxes/marginal_tax_rates": marginal_tax_rates.layout,
        "/taxes/tax_vehicles": tax_vehicles.layout,
        "/taxes/tax_location_detail": tax_location_detail.layout,
        "/taxes/tax_location_compare": tax_location_compare.layout,
    }
    return pages

def register_futures_options():
    from pages.futures_options import (
        futures_options_home,
        forward_curve,
        market_data,
        option_portfolios,
        binomial_trees,
        calibrated_binomial_trees,
        europeans_americans,
        binomial_convergence,
        delta_hedges,
        american_call,
        black_scholes_values,
        black_scholes_formula,
        american_boundary,
        greeks,
        implied_volatility,
        put_call_parity,
        delta_hedge_portfolios,
        market_implied_vols,
        general_black_scholes,
        monte_carlo,
    )
    pages = {
        "/futures-options/futures-options-home": futures_options_home.layout,
        "/futures-options/forward-curve": forward_curve.layout,
        "/futures-options/market-data": market_data.layout,
        "/futures-options/binomial-trees": binomial_trees.layout,
        "/futures-options/calibrated-binomial-trees": calibrated_binomial_trees.layout,
        "/futures-options/europeans-americans": europeans_americans.layout,
        "/futures-options/american-boundary": american_boundary.layout,
        "/futures-options/option-portfolios": option_portfolios.layout,
        "/futures-options/binomial-convergence": binomial_convergence.layout,
        "/futures-options/delta-hedges": delta_hedges.layout,
        "/futures-options/american-call": american_call.layout,
        "/futures-options/black-scholes-values": black_scholes_values.layout,
        "/futures-options/black-scholes-formula": black_scholes_formula.layout,
        "/futures-options/greeks": greeks.layout,
        "/futures-options/implied-volatilities": implied_volatility.layout,
        "/futures-options/put-call-parity": put_call_parity.layout,
        "/futures-options/delta-hedge-portfolios": delta_hedge_portfolios.layout,
        "/futures-options/market-implied-vols": market_implied_vols.layout,
        "/futures-options/general-black-scholes": general_black_scholes.layout,
        "/futures-options/monte-carlo": monte_carlo.layout,
    }
    return pages

def register_all():
    layout = {}
    layout.update(register_borrowing_saving())
    layout.update(register_fixed_income())
    layout.update(register_risk())
    layout.update(register_portfolios())
    layout.update(register_capm())
    layout.update(register_factor_investing())
    layout.update(register_topics())
    layout.update(register_futures_options())
    return layout

