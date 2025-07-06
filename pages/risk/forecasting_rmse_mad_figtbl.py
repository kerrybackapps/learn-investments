import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go
from pages.formatting import smallfig
import numpy as np

numsims = 5000

def figtbl(name, n_clicks, mn, sd, T):
    
    # assuming symmetric sample sizes
    T_past = T
    T_future = T
    
    mn /= 100
    sd /= 100
    
    # Generate the data
    rv = norm(loc=mn, scale=sd)
    past = pd.DataFrame(rv.rvs((T_past,numsims)))
    futures = pd.DataFrame(rv.rvs((T_future,numsims)))

    # Means using historical data
    arith = past.mean()
    geom  = (1 + past).prod() ** (1 / T_past) - 1

    # Predictors
    arith_forecast = (1+arith)**T_future
    geom_forecast  = (1+geom) **T_future

    # Outcomes
    outcome_cumret = (1+futures).prod()
    outcome_arithmean = futures.mean()
    outcome_geomean   = ((1+futures).prod())**(1/T_future)-1

    # Combine data into dataframe with past and future stats for each simulation
    data_dict = {'arith_forecast': arith_forecast, 'geom_forecast': geom_forecast, 'arith': arith, 'geom': geom, 
                 'outcome_cumret': outcome_cumret, 'outcome_arithmean': outcome_arithmean, 'outcome_geomean': outcome_geomean}
    df = pd.DataFrame(data_dict, columns=list(data_dict.keys()))
    
    # Table of forecasting stats for outcome=cumulative return
    tbl_cumret = pd.DataFrame(dtype=float, columns=['RMSE', 'Mean Abs Dev', 'Median Abs Dev'], index=['Arithmetic', 'Geometric'])
    tbl_cumret.loc['Arithmetic','RMSE']      = np.round(np.sqrt(((df.outcome_cumret-df.arith_forecast)**2).mean()),3)
    tbl_cumret.loc['Geometric','RMSE']       = np.round(np.sqrt(((df.outcome_cumret-df.geom_forecast)**2).mean()),3)

    tbl_cumret.loc['Arithmetic','Mean Abs Dev']      = np.round(np.abs(df.outcome_cumret-df.arith_forecast).mean(),3)
    tbl_cumret.loc['Geometric','Mean Abs Dev']       = np.round(np.abs(df.outcome_cumret-df.geom_forecast).mean(),3)

    tbl_cumret.loc['Arithmetic','Median Abs Dev']      = np.round(np.abs(df.outcome_cumret-df.arith_forecast).median(),3)
    tbl_cumret.loc['Geometric','Median Abs Dev']       = np.round(np.abs(df.outcome_cumret-df.geom_forecast).median(),3)
    for c in tbl_cumret.columns.to_list():
        tbl_cumret[c] = tbl_cumret[c].map(lambda x: f"${x:.3f}")
    # print(tbl_cumret)
    # work-around for dash datatable formatting
    col_list = [""] + tbl_cumret.columns.to_list()
    tbl_cumret = tbl_cumret.reset_index()
    tbl_cumret.columns = [name+c for c in col_list]
    tbl_cumret = tbl_cumret.to_dict('records')
        
    # Boxplot for outcome=cumulative return
    fig_cumret = go.Figure()
    trace1 = go.Box(y=df.outcome_cumret - df.arith_forecast, name='Arithmetic', hovertemplate="$%{y:.2f}<extra></extra>")
    trace2 = go.Box(y=df.outcome_cumret - df.geom_forecast, name='Geometric', hovertemplate="$%{y:.2f}<extra></extra>")
    fig_cumret.add_trace(trace1)
    fig_cumret.add_trace(trace2)
    fig_cumret.update_yaxes(tickformat=".2f", tickprefix="$")
    # fig_cumret.show()
    
    
    # Table of forecasting stats for outcome=arithmetic average return
    tbl_arithmean = pd.DataFrame(dtype=float, columns=['RMSE', 'Mean Abs Dev', 'Median Abs Dev'], index=['Arithmetic', 'Geometric'])
    tbl_arithmean.loc['Arithmetic','RMSE']      = np.round(100*np.sqrt(((df.outcome_arithmean-df.arith)**2).mean()),2)
    tbl_arithmean.loc['Geometric','RMSE']       = np.round(100*np.sqrt(((df.outcome_arithmean-df.geom)**2).mean()),2)

    tbl_arithmean.loc['Arithmetic','Mean Abs Dev']      = np.round(100*np.abs(df.outcome_arithmean-df.arith).mean(),2)
    tbl_arithmean.loc['Geometric','Mean Abs Dev']       = np.round(100*np.abs(df.outcome_arithmean-df.geom).mean(),2)

    tbl_arithmean.loc['Arithmetic','Median Abs Dev']      = np.round(100*np.abs(df.outcome_arithmean-df.arith).median(),2)
    tbl_arithmean.loc['Geometric','Median Abs Dev']       = np.round(100*np.abs(df.outcome_arithmean-df.geom).median(),2)
    # print(tbl_arithmean)
    # work-around for dash datatable formatting
    col_list = [""] + tbl_arithmean.columns.to_list()
    tbl_arithmean = tbl_arithmean.reset_index()
    tbl_arithmean.columns = [name+c for c in col_list]
    tbl_arithmean = tbl_arithmean.to_dict('records')    
    
    
    # Boxplot for outcome=arithmetic average return
    fig_arithmean = go.Figure()
    trace1 = go.Box(y=100*(df.outcome_arithmean - df.arith), name='Arithmetic', hovertemplate="%{y:.2f}<extra></extra>")
    trace2 = go.Box(y=100*(df.outcome_arithmean - df.geom), name='Geometric', hovertemplate="%{y:.2f}<extra></extra>")
    fig_arithmean.add_trace(trace1)
    fig_arithmean.add_trace(trace2)
    # fig_arithmean.show()
    
    # Table of forecasting stats for outcome=geometric average return
    tbl_geomean = pd.DataFrame(dtype=float, columns=['RMSE', 'Mean Abs Dev', 'Median Abs Dev'], index=['Arithmetic', 'Geometric'])
    tbl_geomean.loc['Arithmetic','RMSE']      = np.round(100*np.sqrt(((df.outcome_geomean-df.arith)**2).mean()),2)
    tbl_geomean.loc['Geometric','RMSE']       = np.round(100*np.sqrt(((df.outcome_geomean-df.geom)**2).mean()),2)

    tbl_geomean.loc['Arithmetic','Mean Abs Dev']      = np.round(100*np.abs(df.outcome_geomean-df.arith).mean(),2)
    tbl_geomean.loc['Geometric','Mean Abs Dev']       = np.round(100*np.abs(df.outcome_geomean-df.geom).mean(),2)

    tbl_geomean.loc['Arithmetic','Median Abs Dev']      = np.round(100*np.abs(df.outcome_geomean-df.arith).median(),2)
    tbl_geomean.loc['Geometric','Median Abs Dev']       = np.round(100*np.abs(df.outcome_geomean-df.geom).median(),2)
    # print(tbl_geomean)
    # work-around for dash datatable formatting
    col_list = [""] + tbl_geomean.columns.to_list()
    tbl_geomean = tbl_geomean.reset_index()
    tbl_geomean.columns = [name+c for c in col_list]
    tbl_geomean = tbl_geomean.to_dict('records')        
    
    
    # Boxplot for outcome=geometric average return
    fig_geomean = go.Figure()
    trace1 = go.Box(y=100*(df.outcome_geomean - df.arith), name='Arithmetic', hovertemplate="%{y:.2f}<extra></extra>")
    trace2 = go.Box(y=100*(df.outcome_geomean - df.geom), name='Geometric', hovertemplate="%{y:.2f}<extra></extra>")
    fig_geomean.add_trace(trace1)
    fig_geomean.add_trace(trace2)
    # fig_geomean.show()
    
    return tbl_cumret, tbl_arithmean, tbl_geomean, smallfig(fig_cumret), smallfig(fig_arithmean), smallfig(fig_geomean)

