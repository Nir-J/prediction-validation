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
  stock_dict = {1:{'stock1':(value, False), 'stock2':(value, False)},
                2:{'stock1':(value, False), 'stock2':(value, False)},
                3:{'stock1':(value, False), 'stock2':(value, False)}}
  ```
  > Where the first key is the hour. Each hour has another dictionary as its value, which consists of all 
  stock and their values in that particular hour. False signifies that we do not know if it is present in both files.
  - Then read the **actual.txt** file, line by line, as we do not need to store all of the stocks.
  - If a **stock matches** with one of the predicted values, **update the stock's value** in dictionary **to the absolute difference** between the two values. And, update it to **True**
  - Like this, **all the values** stored in dictionary will be **updated to** the absolute difference, or **Error in prediction values.**
  ```P
  Stock Dictionary now:
  stock_dict = {1:{'stock1':(error_val, True), 'stock2':(error_val, True)},
                2:{'stock1':(value, False), 'stock2':(error_val, True)},
                3:{'stock1':(error_val, True), 'stock2':(error_val, True)}}
  ```
  > If a stock has False, it means its value has not been updated to error value as it was missing in the actual file.
  - We also make note of the maximum hour and minimum hour in the actual file, as this will be where the sliding window starts and ends.
  
### 2) Calculating Averages
