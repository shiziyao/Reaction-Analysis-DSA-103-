def calculate_reaction_rates(dataframe):
    """Calculate reaction rates for each time interval"""
    # hint: use df.groupby("setup")["columname"].diff()
    merged_data = dataframe.groupby("setup")[['time (min)','concentration (M)']].diff()
    merged_data['reaction_rates (M/min)']=merged_data['concentration (M)']/merged_data['time (min)']
    merged_data.columns = ['time_diff(min)','concentration_diff(M)','reaction_rates(M/min)']
    final_dataset= pd.concat([dataframe,merged_data], axis=1)
    return final_dataset

def find_optimal_conditions(dataframe):
    """Analyze data to find optimal reaction conditions"""
    # for best conditions, the sweet spot should be yield>90% of max, and then the tradeoff
    # between yield, time and temperature
    top_yields=dataframe[dataframe['yield (%)']>=0.9*max(dataframe['yield (%)'])]
    top_yields['yield%/min']=top_yields['yield (%)']/top_yields['time (min)']
    top_yield_per_min=top_yields.nlargest(2, "yield%/min")

    # capping the temperature below 45 C
    top_yield_per_min=top_yield_per_min[top_yield_per_min['temperature (°C)']<46]
    final_optimum_condition = top_yield_per_min.loc[top_yield_per_min['yield%/min'].idxmax()]
    return final_optimum_condition

def compare_setups(dataframe):
    dataframe = dataframe.copy()
    dataframe['yield%/min'] = dataframe['yield (%)'] / dataframe['time (min)'].replace(0, float('nan'))
    """Compare performance between setups A and B"""
    setup_A= dataframe[dataframe['setup']=='A']
    setup_B= dataframe[dataframe['setup']=='B']

    # for setup_A
    max_yield_condition_A = setup_A.loc[setup_A['yield (%)'].idxmax()]
    max_yield_per_min_condition_A = setup_A.loc[setup_A['yield%/min'].idxmax()]
    average_reaction_rate_A = setup_A['reaction_rates(M/min)'].mean()

    for_setup_A ={"for setup": "A","Max_yield_condition":max_yield_condition_A,
                  "Max_yield_per_min_condition":max_yield_per_min_condition_A,
                  "Average_reaction_rate": average_reaction_rate_A}
    # for setup_B
    max_yield_condition_B = setup_B.loc[setup_B['yield (%)'].idxmax()]
    max_yield_per_min_condition_B = setup_B.loc[setup_B['yield%/min'].idxmax()]
    average_reaction_rate_B = (setup_B['reaction_rates(M/min)']).mean()

    for_setup_B ={"for setup" :'B',"Max_yield_condition":max_yield_condition_B,
                  "Max_yield_per_min_condition":max_yield_per_min_condition_B,
                  "Average_reaction_rate": average_reaction_rate_B}
    

    return for_setup_A,for_setup_B