from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
def preprocess_china_data(china_df):
    """
    Written for china data; will drop null values and
    split into training and testing sets. Uses price
    as the target column.
    """
    china_df['pm2.5'] = china_df['pm2.5'].fillna(china_df['pm2.5'].mean())
    china_df = china_df.dropna()
    X = pd.get_dummies(china_df.drop(columns='pm2.5'))
    y = china_df['pm2.5'].values.reshape(-1, 1)
    return train_test_split(X, y)   
def preprocess_china_data_keep_na(china_df):
    """
    Written for china data; will split into training
    and testing sets. Uses price as the target column.
    """
    X = china_df.drop(columns='pm2.5')
    y = china_df['pm2.5'].values.reshape(-1, 1)
    return train_test_split(X, y)
def r2_adj(x, y, model):
    """
    Calculates adjusted r-squared values given an X variable,
    predicted y values, and the model used for the predictions.
    """
    r2 = model.score(x,y)
    n_cols = x.shape[1]
    return 1 - (1 - r2) * (len(y) - 1) / (len(y) - n_cols - 1)
def check_metrics(X_test, y_test, model):
    # Use the pipeline to make predictions
    y_pred = model.predict(X_test)
    # Print out the MSE, r-squared, and adjusted r-squared values
    print(f"--> Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
    print(f"--> R-squared: {r2_score(y_test, y_pred)}")
    print(f"--> Adjusted R-squared: {r2_adj(X_test, y_test, model)}")    
    return r2_adj(X_test, y_test, model)
def get_best_pipeline(pipeline, pipeline2, china_df):
    """
    Accepts two pipelines and china data.
    Uses two different preprocessing functions to
    split the data for training the different
    pipelines, then evaluates which pipeline performs
    best.
    """
    # Apply the preprocess_china_data step
    X_train, X_test, y_train, y_test = preprocess_china_data(china_df)
    # Fit the first pipeline
    pipeline.fit(X_train, y_train)
    print("** Testing dropped NAs")  
    # Print out the MSE, r-squared, and adjusted r-squared values
    # and collect the adjusted r-squared for the first pipeline
    p1_adj_r2 = check_metrics(X_test, y_test, pipeline)
    # Apply the preprocess_china_data_keep_na step
    X_train, X_test, y_train, y_test = preprocess_china_data_keep_na(china_df)
    # Fit the second pipeline
    pipeline2.fit(X_train, y_train)
    print("** Testing no dropped data")
    # Print out the MSE, r-squared, and adjusted r-squared values
    # and collect the adjusted r-squared for the second pipeline
    p2_adj_r2 = check_metrics(X_test, y_test, pipeline2)
    # Compare the adjusted r-squared for each pipeline and
    # return the best model
    if p2_adj_r2 > p1_adj_r2:
        print("** Returning no dropped data pipeline")      
        return pipeline2
    else:
        print("** Returning dropped NAs pipeline")       
        return pipeline
def china_model_generator(china_df, dynamic_name):
    """
    Defines a series of steps that will preprocess data,
    split data, and train a model for predicting rent prices
    using linear regression. It will return the trained model
    and print the mean squared error, r-squared, and adjusted
    r-squared scores.
    """
    # Create a list of steps for a pipeline that will one hot encode and scale data
    # Each step should be a tuple with a name and a function
    steps = [("One hot encode", OneHotEncoder(handle_unknown="ignore")),
             ("Scale", StandardScaler(with_mean=False)),
             ("Linear Regression", LinearRegression())]
    # Create a pipeline object
    pipeline = Pipeline(steps)
    # Create a second pipeline object
    pipeline2 = Pipeline(steps)
    # Get the best pipeline
    print("----------")
    print("* " + dynamic_name + " *")
    print("----------")
    pipeline = get_best_pipeline(pipeline, pipeline2, china_df)
    # Return the trained model
    return pipeline
if __name__ == "__main__":
    print("This script should not be run directly! Import these functions for use in another file.")