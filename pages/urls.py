titleDict = {}

# ---------------------------------------------
#
# add new chapters here
#
# ---------------------------------------------

titleDict["/borrowing-saving"] = "Time Value of Money"
titleDict["/risk"] = "Risk and Return"
core_urls = [
    "/borrowing-saving",
    "/risk",
]

titleDict["/portfolios"] = "Portfolios"
titleDict["/capm"] = "Capital Asset Pricing Model"
titleDict["/factor-investing"] = "Sorts and Factors"
# titleDict["/performance-evaluation"] = "Performance Evaluation"
# titleDict["/taxes"] = "Taxes"
titleDict["/topics"] = "Funds and Taxes"
investments_urls = [
    "/portfolios",
    "/capm",
    "/factor-investing",
    "/topics",
    # "/taxes",
]

titleDict["/futures-options"] = "Futures and Options"
titleDict["/fixed-income"] = "Fixed Income"
other_urls = ["/futures-options", "/fixed-income"]

all_chapter_urls = [
    "/borrowing-saving",
    "/risk",
    "/portfolios",
    "/capm",
    "/factor-investing",
    "/topics",
    "/futures-options",
    "/fixed-income",
]

homepages = {
    "Time Value of Money": "/borrowing-saving/borrowing-saving-home",
    "Risk and Return": "/risk/risk-home",
    "Portfolios": "/portfolios/portfolios-home",
    "Funds and Taxes": "/performance-evaluation/performance-evaluation-home",
    "Futures and Options": "/futures-options/futures-options-home",
    "Sorts and Factors": "/factor-investing/factor-investing-home",
    "Capital Asset Pricing Model": "/capm/capm-home",
     "Fixed Income": "/fixed-income/fixed-income-home",
}
# -----------------------------------------------
#
# add new pages here
#
# -----------------------------------------------

# Core chapters
titleDict["/borrowing-saving/borrowing-saving-home"] = "Overview: Time value of money"
titleDict["/borrowing-saving/amortization"] = "Amortization"
titleDict["/borrowing-saving/amortization-schedule"] = "Amortization schedule"
titleDict["/borrowing-saving/inflation"] = "Inflation and real returns"
titleDict["/borrowing-saving/irr"] = "Internal rate of return"
titleDict["/borrowing-saving/retirement-planning"] = "Retirement planning"
titleDict["/borrowing-saving/npv"] = "Net present value"
# titleDict["/borrowing-saving/retirement-solution"] = "Retirement planning solution"
titleDict["/borrowing-saving/two-stage"] = "Two-stage valuation model"
titleDict["/borrowing-saving/retirement-planning-sim"] = "Retirement planning simulation"
borrowing_saving_urls = [
    "borrowing-saving-home",
    "npv",
    "irr",
    "two-stage",
    "amortization",
    "amortization-schedule",
    "retirement-planning",
    # "retirement-solution",
    "retirement-planning-sim",
    "inflation",
]
borrowing_saving_urls = ["/borrowing-saving/" + x for x in borrowing_saving_urls]

titleDict["/risk/risk-home"] = "Overview: Risk and return"
titleDict["/risk/sbb-real"] = "Real stock, bond, and gold returns"
titleDict["/risk/sbb"] = "Stock, bond, and gold returns"
titleDict["/risk/correlations"] = "Inflation and returns"
titleDict["/risk/returns"] = "Stock market returns"
titleDict["/risk/best-worst"] = "Best and worst periods"
titleDict["/risk/frequencies"] = "Returns at different frequencies"
titleDict["/risk/volatilities"] = "Time varying volatilities"
titleDict["/risk/long-run"] = "Skewness of long-run returns"
# titleDict["/risk/means"] = "Arithmetic and geometric averages as forecasts"
titleDict["/risk/geometric"] = "Geometric average returns"
titleDict["/risk/continuous-compounding"] = "Continuously compounded returns"
titleDict["/risk/simulation"] = "Simulating returns"
titleDict["/risk/asset-classes"] = "Correlations of stocks or funds"
risk_urls = [
    "risk-home",
    "returns",
    "frequencies",
    "volatilities",
    "geometric",
    "best-worst",
    "continuous-compounding",
    "simulation",
    "long-run",
    # "means",
    "sbb",
    "correlations",
    "sbb-real",
    "asset-classes",
]
risk_urls = ["/risk/" + x for x in risk_urls]




# Investments chapters
titleDict["/portfolios/portfolios-home"] = "Overview: Portfolios"
titleDict["/portfolios/two-assets"] = "Two risky assets"
titleDict["/portfolios/short-sales"] = "Short sales"
titleDict["/portfolios/preferences"] = "Preferences"
titleDict["/portfolios/frontier"] = "Frontier portfolios"
titleDict["/portfolios/risk-free"] = "Risk-free asset"
titleDict["/portfolios/three-assets"] = "Three risky assets"
titleDict["/portfolios/optimal-sb"] = "Optimal portfolios of stocks, bonds, and gold"
titleDict["/portfolios/optimal-yahoo"] = "Optimal portfolios of stocks or funds"
titleDict["/portfolios/diversification"] = "Diversification"
titleDict["/portfolios/short-sales-constraints"] = "Effect of short sales constraints"
titleDict['/portfolios/optimal-N'] = 'Optimal portfolios with more assets'
titleDict['/portfolios/sharpe'] = 'Sharpe ratios'
titleDict['/portfolios/optimal'] = 'Optimal capital allocation'
titleDict['/portfolios/tangency'] = 'Tangency portfolio'
titleDict['/portfolios/optimal-two-rates'] = "Optimal capital allocation with different rates"
portfolios_urls = ("portfolios-home",
                   "two-assets",
                   "three-assets",
                   "diversification",
                   "short-sales",
                   "frontier",
                   "risk-free",
                   "sharpe",
                   "tangency",
                   "preferences",
                   "optimal",
                   "optimal-two-rates",
                   "short-sales-constraints",
                   "optimal-N",
                   "optimal-sb",
                   "optimal-yahoo",
                   )
portfolios_urls = ["/portfolios/" + x for x in portfolios_urls]



titleDict["/capm/capm-home"] = "Overview: Capital Asset Pricing Model"
titleDict["/capm/alphas-betas"] = "Alphas and betas"
titleDict["/capm/costequity"] = "CAPM cost of equity calculator"
titleDict["/capm/mrp_estimation"] = "Estimating the market risk premium"
titleDict["/capm/alphas-mve"] = "Alphas and mean-variance efficiency"
titleDict["/capm/alphas-sharpes"] = "Alphas and Sharpe ratios"
titleDict["/capm/sml-industries"] = "Security market line for industry returns"
titleDict["/capm/two-way-capm"] = "CAPM for two-way sorts"
capm_urls = ["capm-home", "alphas-betas", "alphas-mve", "alphas-sharpes", "costequity", "mrp_estimation", "sml-industries", "two-way-capm"]
capm_urls = ["/capm/" + x for x in capm_urls]

titleDict["/factor-investing/factor-investing-home"] = "Overview: Sorts and factors"
titleDict["/factor-investing/quintiles"] = "Sorts on characteristics"
# titleDict["/factor-investing/ghz-sorts"] = "Sorts on other characteristics"
titleDict["/factor-investing/two-way-sorts"] = "Two-way sorts"
titleDict["/factor-investing/ff-industries"] = "Fama-French model for industries"
titleDict["/factor-investing/ff-costequity"] = "Fama-French cost of equity calculator"
titleDict["/factor-investing/ff-characteristics"] = "Fama-French model for two-way sorts"
factor_investing_urls = ["factor-investing-home", "quintiles", "two-way-sorts"] # , "ghz-sorts"]
factor_investing_urls += ["ff-costequity",  "ff-characteristics"] # , "ff-industries"]
factor_investing_urls = ["/factor-investing/" + x for x in factor_investing_urls]

# titleDict["/performance-evaluation/user-returns"] = "Evaluation of user-supplied returns"
titleDict["/performance-evaluation/performance-evaluation-home"] = "Overview: Funds and taxes"
titleDict["/performance-evaluation/funds"] = "Evaluation of mutual funds"
titleDict["/performance-evaluation/market_timing"] = "Market timing"
performance_evaluation_urls = ["performance-evaluation-home", "funds", 'market_timing'] # , "user-returns"]
performance_evaluation_urls = [
    "/performance-evaluation/" + x for x in performance_evaluation_urls
]

titleDict["/taxes/marginal_tax_rates"] = "Marginal and effective tax rates"
titleDict["/taxes/tax_vehicles"] = "Tax-advantaged savings vehicles"
titleDict["/taxes/tax_location_detail"] = "Asset location with taxes"
titleDict["/taxes/tax_location_compare"] = "Comparison of asset locations with taxes"
taxes_urls = ["marginal_tax_rates","tax_vehicles", "tax_location_detail", "tax_location_compare"]
taxes_urls = ["/taxes/" + x for x in taxes_urls]

topics_urls = performance_evaluation_urls + taxes_urls

# Other chapters
titleDict["/futures-options/futures-options-home"] = "Overview: Futures and options"
titleDict["/futures-options/forward-curve"] = "Forward curves"
titleDict["/futures-options/market-data"] = "Market option data"
titleDict["/futures-options/calibrated-binomial-trees"] = "Calibrated binomial trees"
titleDict["/futures-options/option-portfolios"] = "Option portfolios"
titleDict["/futures-options/binomial-trees"] = "Binomial trees"
titleDict["/futures-options/europeans-americans"] = "European and American option values"
titleDict["/futures-options/american-boundary"] = "American option exercise boundaries"
titleDict["/futures-options/binomial-convergence"] = "Binomial convergence"
titleDict["/futures-options/delta-hedges"] = "Delta hedges"
titleDict["/futures-options/american-call"] = "American call with a single cash dividend"
titleDict["/futures-options/black-scholes-values"] = "Black-Scholes plots"
titleDict["/futures-options/black-scholes-formula"] = "Black-Scholes formula"
titleDict["/futures-options/greeks"] = "Option Greeks"
titleDict["/futures-options/implied-volatilities"] = "Implied volatilities"
titleDict["/futures-options/put-call-parity"] = "Put-call parity"
titleDict["/futures-options/delta-hedge-portfolios"] = "Delta hedges of option portfolios"
titleDict["/futures-options/market-implied-vols"] = "Market implied volatilities"
titleDict["/futures-options/general-black-scholes"] = "General Black-Scholes formula"
titleDict["/futures-options/monte-carlo"] = "Monte Carlo option valuation"
futures_options_urls = [
    "futures-options-home",
    "forward-curve",
    "market-data",
    "option-portfolios",
    "put-call-parity",
    "black-scholes-formula",
    "black-scholes-values",
    "monte-carlo",
    "implied-volatilities",
    "market-implied-vols",
    "greeks",
    "delta-hedges",
    "delta-hedge-portfolios",
    "binomial-trees",
    "calibrated-binomial-trees",
    "binomial-convergence",
    "american-boundary",
    "europeans-americans",
    "american-call",
    "general-black-scholes",
]
futures_options_urls = ["/futures-options/" + x for x in futures_options_urls]

#titleDict["/futures/forward-curve"] = "Forward curves"
#futures_urls = ["forward-curve"]
#futures_urls = ["/futures/" + x for x in futures_urls]

titleDict["/fixed-income/fixed-income-home"] = "Overview: Fixed income"
titleDict["/fixed-income/termstructure"] = "Term structure of interest rates"
titleDict["/fixed-income/creditspreads"] = "Credit spreads"
titleDict["/fixed-income/prices-yields"] = "Bond prices and yields"
titleDict["/fixed-income/tips"] = "Treasury inflation protected securities"
titleDict["/fixed-income/clean-dirty"] = "Clean and dirty bond prices and yields"
titleDict["/fixed-income/clean-dirty-paths"] = "Hypothetical clean and dirty price paths"
titleDict["/fixed-income/real-termstructure"] = "Term structure of real interest rates"
titleDict['/fixed-income/duration'] = 'Duration'
titleDict['/fixed-income/duration-risk'] = 'Duration and risk'
titleDict['/fixed-income/termstructure-movements'] = 'Term structure movements'
titleDict['/fixed-income/principal-components'] = 'Principal components'
titleDict['/fixed-income/spot-forward'] = "Spot and forward rates"
titleDict['/fixed-income/rate-tree'] = 'Interest rate trees'
titleDict['/fixed-income/oas'] = 'Option adjusted spreads'
fixed_income_urls = [
    "fixed-income-home",
    "prices-yields",
    "termstructure",
    "creditspreads",
    "tips",
    "real-termstructure",
    "clean-dirty",
    "clean-dirty-paths",
    'duration',
    'duration-risk',
    'spot-forward',
    'rate-tree',
    'oas',
    'termstructure-movements',
    'principal-components'
]
fixed_income_urls = ['/fixed-income/' + x for x in fixed_income_urls]

