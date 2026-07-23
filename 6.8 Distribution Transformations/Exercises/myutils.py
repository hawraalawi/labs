
import pandas as pd
import numpy as np

def skew_calc(df):
    """
    Diagnoses skewness for every numeric column in a DataFrame and recommends a transformation based on the column's skewness and
    minimum value. Binary, encoded, and ID columns are excluded, since skewness isn't a meaningful for them.
    It returns a DataFrame with the following columns:
    Feature, Skewness, Degree, Direction, Recommended Transformation
    """
    # Your code here 

    results = []

    # select only numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns


    for col in numeric_cols:

        # Skip binary indicators (0/1) or columns ending with '_id'
        if 'id' in str(col).lower() or df[col].nunique() <= 2:
            continue

        skew_val = df[col].skew()
        min_val = df[col].min()

        # classify degree and direction based on Table 1
        if skew_val < -1:
            degree, direction = 'Highly Skewed', 'Left'
        elif -1 <= skew_val < -0.5:
            degree, direction = 'Moderately Skewed', 'Left'
        elif -0.5 <= skew_val <= 0.5:
            degree, direction = 'Normal', 'Symmetrical'
        elif 0.5 < skew_val <= 1:
            degree, direction = 'Moderately Skewed', 'Right'
        else:
            degree, direction = 'Highly Skewed', 'Right'

        # recommend transformation based on Table 2
        if degree == 'Normal':
            recommendation = 'None'
        elif min_val < 0:
            recommendation = 'Yeo-Johnson'
        elif min_val == 0:
            recommendation = 'Log Plus One'
        else:
            recommendation = 'Box-Cox'

        results.append({
            'Feature': col,
            'Skewness': skew_val,
            'Degree': degree,
            'Direction': direction,
            'Recommended Transformation': recommendation
        })

    return pd.DataFrame(results)


