# Prediction-Validation
Coding challenge for Insight Fellowship

Problem: https://github.com/InsightDataScience/prediction-validation

### Requirements:
1) Python 2.7

## Approach

### 1) Reading and Preparing data.
  - Any stock value not present in the Predicted file is of no use in error calculation, so **start with the predicted file**.
  - It is stated that we may assume all input data fits in main memory of a single system. Hence, we can read the predicted file in one go.
  - Each **predicted stock** is stored in a **Hash map (Dictionary)** with key being the hour and stock name.
  ```P
  Format of Stock dictionary:
  stock_dict = {1:{'stock1':value, 'stock2':value},
                2:{'stock1':value, 'stock2':value},
                3:{'stock1':value, 'stock2':value}}
  ```
  > Where the first key is the hour. Each hour has another dictionary as its value, which consists of all 
  stock and their values in that particular hour.
  - Then read the **actual.txt** file, line by line, as we do not need to store all of the stocks.
  - If a **stock matches** with one of the predicted values, **update the stock's value** in dictionary **to the absolute difference** between the two values.
  - Like this, **all the values** stored in dictionary will be **updated to** the absolute difference, or **Error in prediction values.**
  ```P
  Stock Dictionary now:
  stock_dict = {1:{'stock1':error_val, 'stock2':error_val},
                2:{'stock1':error_val, 'stock2':error_val},
                3:{'stock1':error_val, 'stock2':error_val}}
  ```
  - We also make note of the maximum hour in the actual file, as this will be where the sliding window ends.
  
### 2) Calculating Averages
