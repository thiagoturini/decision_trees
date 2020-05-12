import pandas as pd
import math
import numpy as np
#import sys
#sys.path.append('../')
#from project import config
from config import data_windows


df = pd.read_csv(data_windows)

print(df.head(10))

instances = df.shape[0]


def continuos_data(df, name_column, entropy):
    unique_values = sorted(df[name_column].unique())  ############
    continuous_gain = []

    for i in range(0, len(unique_values) - 1):
        ranking = unique_values[i]

        subdata1 = df[df[name_column] <= ranking]
        subdata2 = df[df[name_column] > ranking]

        subdata1_instances = subdata1.shape[0]
        subdata2_instances = subdata2.shape[0]
        instances = df.shape[0]

        subdata1_probability = subdata1_instances / instances
        subdata2_probability = subdata2_instances / instances

        ranking_gain = entropy - subdata1_probability * calculate_entropy(
            subdata1) - subdata2_probability * calculate_entropy(subdata2)

        ranking_split = - subdata1_probability * math.log(subdata1_probability, 2) - subdata2_probability * math.log(
            subdata2_probability, 2)

        ganancia_ratio = ranking_gain / ranking_split
        continuous_gain.append(ganancia_ratio)

    max_gain = continuous_gain.index(max(continuous_gain))
    max_gain_column = unique_values[max_gain]

    df[name_column] = np.where(df[name_column] <= max_gain_column, "<=" + str(max_gain_column),
                               ">" + str(max_gain_column))
    return df


def calculate_entropy(df):
    instances = df.shape[0]  ########
    entropy = 0
    categories = df.iloc[:, -1].value_counts().keys().tolist()

    for i in range(0, len(categories)):
        probability_category = df.iloc[:, -1].value_counts().tolist()[i] / instances
        entropy = entropy - probability_category * math.log(probability_category, 2)

    return entropy


def entropy_category(df):
    entropy = calculate_entropy(df)  
    gains = []
    gains_ratio = []
    columns = df.shape[1]  
    instances = df.shape[0]  

    for i in range(0, columns - 1):
        name_column = df.columns[i]
        type_column = df[name_column].dtypes
        if type_column != "object":  
            df = continuos_data(df, name_column, entropy)

        column_categories = df[name_column].value_counts()
        gain = entropy
        split = 0

        for j in range(0, len(column_categories)):
            actual_category = column_categories.keys().tolist()[j]
            sub_data = df[df[name_column] == actual_category]
            sub_data_entropy = calculate_entropy(sub_data)
            sub_data_instances = sub_data.shape[0]
            category_probability = sub_data_instances / instances
            gain = gain - category_probability * sub_data_entropy

            split = split - category_probability * math.log(category_probability, 2)

        gains.append(gain)

        gain_ratio = gain / split
        gains_ratio.append(gain_ratio)

        highest_gain = gains_ratio.index(max(gains_ratio))

    name_highest_gain = df.columns[highest_gain]

    return name_highest_gain


def tree(df, condition):
    df_copy = df.copy()  ######
    decision = entropy_category(df)
    columns = df.shape[1]

    for i in range(0, columns - 1):  ########
        name_column = df.columns[i]
        # print("name_column")
        if name_column != decision:
            df[name_column] = df_copy[name_column]

    decision_category = df[decision].value_counts().keys().tolist()
    for i in range(0, len(decision_category)):
        actual_category = decision_category[i]
        sub_data = df[df[decision] == actual_category]
        sub_data = sub_data.drop(columns=[decision])
        # print(sub_data)

        if len(sub_data.iloc[:, -1].value_counts().tolist()) == 1:
            decision_final = sub_data.iloc[:, -1].value_counts().keys().tolist()[0]
            print(condition, " Yes ", decision, " is ", actual_category, " , the answer is ", decision_final)
        elif sub_data.shape[1] == 1:  #######################
            decision_final = sub_data.iloc[:, -1].value_counts().idxmax()
            print(condition, " Yes ", decision, " is ", actual_category, " , the answer is ", decision_final)
        else:
            condition = str(condition) + " Yes " + str(decision) + " is " + str(actual_category) + " and "
            tree(sub_data, condition)
            condition = " "


print(tree(df, ""))

