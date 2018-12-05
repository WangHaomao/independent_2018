# Independent Projetc in 2018 

## Hong Kong Real Estate Prediction

In this report, I will divide this project into two parts, the first is **machine learnning** module and another part is about a simple **website**. (There are the links about video and project video)

Video about UI: [ https://youtu.be/LpSvyZWD10w](https://youtu.be/LpSvyZWD10w)
Github: [https://github.com/WangHaomao/independent_2018](https://github.com/WangHaomao/independent_2018)


## Part one, Machine Learnning

In this part, it mainly includes several parts such as data processing, data analysis, missing value supplement, model training, etc.

#### 1. Dataset introduction

The raw dataset stored in the mysql dataset with two different tables, after select as follow sql:

```python
# roughlly get about 522749 recorders
sql = "SELECT * FROM House_Location_Reference\
        INNER JOIN House_Linkage ON House_Linkage.rid = House_Location_Reference.rid"
```

Roughlly get about 522749 recorders, and the index of this frame as follow:

```python
Index(['rid', 'estateNameCN', 'estateNameEN', 'districtL', 'districtS', 'lat',
       'lng', 'tid', 'address', 'transcationDate', 'princeInHKD',
       'trans_change', 'SFA', 'GFA', 'unitPriceSFA', 'unitPriceGFA',
       'contract'],
      dtype='object')
```

And there are too much missing data

```python
# Ture value mean this column has missing data
rid                False
estateNameCN        True
estateNameEN        True
districtL          False
districtS           True
lat                False
lng                False
tid                False
address            False
transcationDate    False
princeInHKD         True
trans_change        True
SFA                 True
GFA                 True
unitPriceSFA        True
unitPriceGFA        True
contract            True
dtype: bool
```



#### 2. Missing value supplement & Generate features

After finishing filling missing values:

```python
districtL      False
districtS      False
floor          False
dis_mtr        False
dis_school     False
dis_market     False
areaSize       False
year           False
month          False
day            False
princeInHKD    False
dtype: bool
```

Created (generated) three new features by map api and spider

```python
# This three columns are search from google map api
# MTR station name from spider
'dis_mtr': Nearest distance of MTR stations
'dis_school': Nearest distance of school
'dis_market': Nearest distance of shopping center
```

The co-relationship of new features as follow:

<img width="50%" height="50%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181205234909754.png"/>

Arranged three four features from original data:

```python
'floor': regular extration from address
'year', 'month', 'day': from date features
'areaSize': from SFA and GFA
```
The co-relationship of floor and areaSize  as follow:

<img width="55%" height="55%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181206003014539.png"/>

<img width="60%" height="60%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181206003032536.png"/>

#### 3. Data analysis

Plot the distribution of categorical data:

<img width="55%" height="60%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181206002117351.png"/>

<img width="60%" height="60%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181206002136598.png"/>


The co-relationship of all features:
![image-20181206001735012](/Users/haomao/Library/Application Support/typora-user-images/image-20181206001735012.png)

#### 4. Models selection (Cross-Validation 4 CV)

I tried ExtraTreesRegressor, RandomForestRegressor, AdaBoostRegressor, MLPRegressor, LinearRegression , etc. The results in MAE(Mean Absolute Error) are here:

```python
[-0.0103665  -0.00744911 -0.00795999 -0.01071204]
ExtraTreesRegressor: 
Mean Absolute Error 0.009122

[-0.01027481 -0.00744757 -0.00791814 -0.0113053 ]
RandomForestRegressor: 
Mean Absolute Error 0.009236

[-0.02346236 -0.03132696 -0.03031218 -0.02962982]
AdaBoostRegressor: 
Mean Absolute Error 0.028683

[-0.02025798 -0.03133608 -0.0315344  -0.04191494]
MLPRegressor: 
Mean Absolute Error 0.031261

[-0.01492791 -0.01556251 -0.01426113 -0.01773662]
LinearRegression: 
Mean Absolute Error 0.015622
```

#### 5. Data Trainning

Finally, the columns are follow:

```python
['districtL', 'districtS','floor', 'dis_mtr',
       'dis_school', 'dis_market', 'areaSize', 'year', 'month', 'day']
```

Do normalization for features and label

```python
# mean
floor           7.580124
dis_mtr        39.725909
dis_school      0.163729
dis_market      0.225913
areaSize      594.412054
dtype: float64
# std
floor           9.725491
dis_mtr       616.339621
dis_school      0.176334
dis_market      0.290479
areaSize      299.757712
dtype: float64
    
# Label after log and / 20
count    516229.000000
mean          0.764239
std           0.037887
min           0.460517
25%           0.742789
50%           0.763590
75%           0.784977
max           1.036163

Name: princeInHKD, dtype: float64        
```

The label after log (beofre / 20):

<img width="60%" height="60%" src="/Users/haomao/Library/Application Support/typora-user-images/image-20181206003755502.png"/>


There is the parameters for model, and the model is **LightGBM**

```python
params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression_l2',
    'metric': {'l2', 'l1'},
    'max_depth': model_param['depth'],
    'num_leaves': model_param['leaf'],
    'min_data_in_leaf': 20,
    'learning_rate': model_param['lr'],
    'feature_fraction': 1,
    'bagging_fraction': model_param['sample'],
    'bagging_freq': 1,
    'bagging_seed': model_param['seed'],
    'verbose': 0
}
```

#### 6. Results

Because the data value is relatively large, it is more intuitive to draw the image. The following three images are the comparison of the true value and the prediction value of the data volume of 100, 50, and 20 respectively.

![image-20181205235722249](/Users/haomao/Library/Application Support/typora-user-images/image-20181205235722249.png)

![image-20181205235943160](/Users/haomao/Library/Application Support/typora-user-images/image-20181205235943160.png)

![image-20181206000003529](/Users/haomao/Library/Application Support/typora-user-images/image-20181206000003529.png)

## Part Two,  Simple Dango Website

#### 1. Environment

| Name             | Version              |
| ---------------- | -------------------- |
| Operation System | Ubuntu 16.04 / MacOS |
| Python           | 3.6                  |
| Django           | 1.11.2               |
| Mysql            | 5.6                  |

#### 2. Tools Usage

| Tools / Package name                | Describtion                            |
| ----------------------------------- | -------------------------------------- |
| Django                              | Main website built by Django (Backend) |
| Admin LTE / JQuery / Bootstrap, etc | Web UI usage                           |
| Mysql                               | Store nearest information neaby estate |
| Google Map API                      | Estate visualization                   |
| Echart                              | Prediction visualization               |

#### 3. File folder structure

projectWeb:
* mainpages
  * data
  * static (most css and js file)
  * templates
    * backend (all html pages) 
  * myconf.py (self-config file)
  * url.py (registered urls)
  * views.py (processing logic)

* projectWeb
  * Fruits
    * settings.py

* manage.py

#### 4. Main pages gallery

Single prediction here, it means we only can predict one estate one time.
![image-20181205231353073](/Users/haomao/Library/Application Support/typora-user-images/image-20181205231353073.png)
The result of this estate in future 6 months
![image-20181205231426678](/Users/haomao/Library/Application Support/typora-user-images/image-20181205231426678.png)
Histogram
![image-20181205231502430](/Users/haomao/Library/Application Support/typora-user-images/image-20181205231502430.png)
Map around
![image-20181205231541338](/Users/haomao/Library/Application Support/typora-user-images/image-20181205231541338.png)




## References

[1] https://paperhive.org/help/markdown

[2] https://zh.wikipedia.org/wiki/Wikipedia:%E9%A6%96%E9%A1%B5

[3]  Data Mining -- Concepts and Techniques by Jiawei Han and Micheline Kamber. Morgan Kaufmann Publishers.