def calculate_reaction_rates(dataframe):
    """Calculate reaction rates for each time interval"""
    # hint: use df.groupby("setup")["columname"].diff()
    merged_data = dataframe.groupby("setup")[['time (min)','concentration (M)']].diff()
    merged_data['reaction_rates (M/min)']=merged_data['concentration (M)']/merged_data['time (min)']
    merged_data.columns = ['time_diff(min)','concentration_diff(M)','reaction_rates(M/min)']
    final_dataset= pd.concat([dataframe,merged_data], axis=1)
    return final_dataset


# OPTIMAL CONDITION IDEATION
# for optimal conditions the condition used is yield/min and tempersture variable
# since generally to get the optimum condition and since in this kind of problem the
# optimal conditio is basically the function of all temp, reaction rate, time, ph
# which will be determined only  by 3-d plotting it and by getting the maxima point using
# the quadratic regression but since the data is quite linear here we cant use that
# hence have used a proxy condition where top_yield > 0.9x max top_yield
# temperature is capped at 46 celcius, since in industry increment in industry can result
# in high yield but increment in temperature increases cost, hence just the high yield cant 
# be the deciding factor, so here the the proxy condition used is highest yield/min with a 
# capping of 46 celcius 
# 
#     
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