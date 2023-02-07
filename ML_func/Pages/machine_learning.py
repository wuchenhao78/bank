import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
# import warnings
import sklearn
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
# Set the character set to prevent Chinese garbled code
# from sklearn.linear_model.coordinate_descent import ConvergenceWarning
mpl.rcParams['font.sans-serif']=[u'simHei']
mpl.rcParams['axes.unicode_minus']=False
# warnings.filterwarnings(action = 'ignore', category=ConvergenceWarning)

def app():
    path = "crx.data"
    names = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
             'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16']
    df = pd.read_csv(path, header=None, names=names)
    st.write('---')
    st.subheader('1. Filtering the missing data')
    st.write("Number of data pieces before filtering:", len(df))

    df = df.replace("?", np.nan).dropna(how='any')
    st.write("Number of data pieces after filtering:", len(df))
    st.write('---')

    def parse(v, l):
        return [1 if i == v else 0 for i in l]

    def parseRecord(record):
        result = []
        a1 = record['A1']
        for i in parse(a1, ('a', 'b')):
            result.append(i)

        result.append(float(record['A2']))
        result.append(float(record['A3']))

        a4 = record['A4']
        for i in parse(a4, ('u', 'y', 'l', 't')):
            result.append(i)

        a5 = record['A5']
        for i in parse(a5, ('g', 'p', 'gg')):
            result.append(i)

        a6 = record['A6']
        for i in parse(a6, ('c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff')):
            result.append(i)

        a7 = record['A7']
        for i in parse(a7, ('v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o')):
            result.append(i)

        result.append(float(record['A8']))

        a9 = record['A9']
        for i in parse(a9, ('t', 'f')):
            result.append(i)

        a10 = record['A10']
        for i in parse(a10, ('t', 'f')):
            result.append(i)

        result.append(float(record['A11']))

        a12 = record['A12']
        for i in parse(a12, ('t', 'f')):
            result.append(i)

        a13 = record['A13']
        for i in parse(a13, ('g', 'p', 's')):
            result.append(i)

        result.append(float(record['A14']))
        result.append(float(record['A15']))

        a16 = record['A16']
        if a16 == '+':
            result.append(1)
        else:
            result.append(0)

        return result

    new_names = ['A1_0', 'A1_1',
                 'A2', 'A3',
                 'A4_0', 'A4_1', 'A4_2', 'A4_3',
                 'A5_0', 'A5_1', 'A5_2',
                 'A6_0', 'A6_1', 'A6_2', 'A6_3', 'A6_4', 'A6_5', 'A6_6', 'A6_7', 'A6_8', 'A6_9', 'A6_10', 'A6_11',
                 'A6_12', 'A6_13',
                 'A7_0', 'A7_1', 'A7_2', 'A7_3', 'A7_4', 'A7_5', 'A7_6', 'A7_7', 'A7_8',
                 'A8',
                 'A9_0', 'A9_1',
                 'A10_0', 'A10_1',
                 'A11',
                 'A12_0', 'A12_1',
                 'A13_0', 'A13_1', 'A13_2',
                 'A14', 'A15', 'A16']
    datas = df.apply(lambda x: pd.Series(parseRecord(x), index=new_names), axis=1)
    names = new_names

    st.subheader('2.Processing the data using one-hot encoding')
    st.write('Here shows the first 5 lines of the dataset after processing')
    st.write(datas.head(5))
    st.write('---')

    ## data segmentation
    X = datas[names[0:-1]]
    Y = datas[names[-1]]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

    X_train.describe().T


    ss = StandardScaler()
    ## Traning
    X_train = ss.fit_transform(X_train)
    X_test = ss.transform(X_test)

    pd.DataFrame(X_train).describe().T

    lr = LogisticRegressionCV(Cs=np.logspace(-4, 1, 50), fit_intercept=True, penalty='l2', solver='lbfgs', tol=0.01,
                              multi_class='ovr')
    lr.fit(X_train, Y_train)

    # Logistic
    st.subheader('3.Comparing LR and KNN')
    lr_r = lr.score(X_train, Y_train)
    lr_r_test = lr.score(X_test, Y_test)
    st.write("LR accuracy on the traning set: %.2f" % lr_r)

    lr_y_predict = lr.predict(X_test)
    y1 = lr.predict_proba(X_test)
    st.write("LR accuracy on the testing set: %.2f" % lr_r_test)

    st.write('###')

    ## KNN
    knn = KNeighborsClassifier(n_neighbors=20, algorithm='kd_tree', weights='distance')
    knn.fit(X_train, Y_train)

    knn_r = knn.score(X_train, Y_train)
    st.write("KNN accuracy on the traning set: %.2f" % knn_r)

    knn_y_predict = knn.predict(X_test)
    knn_r_test = knn.score(X_test, Y_test)
    st.write("KNN accuracy on the testing set: %.2f" % knn_r_test)

    ## 结果图像展示
    ## c. 图表展示
    x_len = range(len(X_test))
    fig = plt.figure(figsize=(14, 7), facecolor='w')
    plt.ylim(-0.1, 1.1)
    plt.plot(x_len, Y_test, 'ro', markersize=6, zorder=3, label=u'True Value')
    plt.plot(x_len, lr_y_predict, 'go', markersize=10, zorder=2,
             label=u'LR Prediction,$R^2$=%.3f' % lr.score(X_test, Y_test))
    plt.plot(x_len, knn_y_predict, 'yo', markersize=16, zorder=1,
             label=u'KNN Prediction,$R^2$=%.3f' % knn.score(X_test, Y_test))
    plt.legend(loc='center right')
    plt.xlabel(u'Data ID', fontsize=18)
    plt.ylabel(u'Approval or not(0: Y，1: N)', fontsize=18)
    plt.title(u'Comparison of LR and KNN', fontsize=20)
    st.pyplot(fig)

    st.write('---')