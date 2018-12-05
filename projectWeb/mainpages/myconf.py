import pandas as pd

numerical_col = ['floor','dis_mtr','dis_school','dis_market','areaSize']
date_col = ['year','month','day']
numerical_mean = [7.58012432e+00, 3.97259090e+01, 1.63729354e-01, 2.25912642e-01,5.94412054e+02]
numerical_std = [9.72549053e+00, 6.16339621e+02, 1.76333788e-01, 2.90479185e-01,2.99757712e+02]
label_normalization = 20

def get_normal():
    mean = pd.Series(index=numerical_col,data = numerical_mean)
    std = pd.Series(index=numerical_col,data = numerical_std)

    return mean,std,label_normalization

# print(get_normal())