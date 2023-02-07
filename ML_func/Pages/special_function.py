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
# from sklearn.pipeline import Pipeline
#from sklearn.neighbors import KNeighborsClassifier
# Set the character set to prevent Chinese garbled code
# from sklearn.linear_model.coordinate_descent import ConvergenceWarning
mpl.rcParams['font.sans-serif']=[u'simHei']
mpl.rcParams['axes.unicode_minus']=False
# warnings.filterwarnings(action = 'ignore', category=ConvergenceWarning)

def app():
    # define the types of user data
    ud_dict = {
        'A1': 'unknown',
        'A2': 0,
        'A3': 0,
        'A4': 'unknown',
        'A5': 'unknown',
        'A6': 'unknown',
        'A7': 'unknown',
        'A8': 0,
        'A9': 'unknown',
        'A10': 'unknown',
        'A11': 0,
        'A12': 'unknown',
        'A13': 'unknown',
        'A14': 0,
        'A15': 0,
    }
    # Let user input his/her information(data)
    option1 = st.selectbox(
        '1.What is your gender?',
        ['a', 'b']
    )
    st.write('You selected {}.'.format(option1))
    ud_dict['A1'] = option1
    # st.write(ud_dict['A1'])

    option2 = st.text_input('2.What is your age?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option2)
    ud_dict['A2'] = option2
    # st.write(ud_dict['A2'])

    option3 = st.text_input('3.What is your debt(k)?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option3)
    ud_dict['A3'] = option3
    # st.write(ud_dict['A3'])

    option4 = st.selectbox(
        '4.Are you married?',
        ['u', 'y', 'l', 't']
    )
    st.write('You selected {}.'.format(option4))
    ud_dict['A4'] = option4
    # st.write(ud_dict['A4'])

    option5 = st.selectbox(
        '5.What kind of bank customer are you?',
        ['g', 'p', 'gg']
    )
    st.write('You selected {}.'.format(option5))
    ud_dict['A5'] = option5
    # st.write(ud_dict['A5'])

    option6 = st.selectbox(
        '6.What is your education level?',
        ['c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff']
    )
    st.write('You selected {}.'.format(option6))
    ud_dict['A6'] = option6
    # st.write(ud_dict['A6'])

    option7 = st.selectbox(
        '7.what is your ethnicity?We do not mean to offend you, but simply analyze your data',
        ['v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o']
    )
    st.write('You selected {}.'.format(option7))
    ud_dict['A7'] = option7
    # st.write(ud_dict['A7'])

    option8 = st.text_input('8.What are your years of employment?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option8)
    ud_dict['A8'] = option8
    # st.write(ud_dict['A8'])

    option9 = st.selectbox(
        '9.Have you ever defaulted before?',
        ['t', 'f']
    )
    st.write('You selected {}.'.format(option9))
    ud_dict['A9'] = option9
    # st.write(ud_dict['A9'])

    option10 = st.selectbox(
        '10.Are you employed?',
        ['t', 'f']
    )
    st.write('You selected {}.'.format(option10))
    ud_dict['A10'] = option10
    # st.write(ud_dict['A10'])

    option11 = st.text_input('11.What is your credit score?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option11)
    ud_dict['A11'] = option11
    # st.write(ud_dict['A11'])

    option12 = st.selectbox(
        '12.Do you have a driver license?',
        ['t', 'f']
    )
    st.write('You selected {}.'.format(option12))
    ud_dict['A12'] = option12
    # st.write(ud_dict['A12'])

    option13 = st.selectbox(
        '13.What kind of citizen are you?',
        ['g', 'p', 's']
    )
    st.write('You selected {}.'.format(option13))
    ud_dict['A13'] = option13
    # st.write(ud_dict['A13'])

    option14 = st.text_input('14.What is your zip code?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option14)
    ud_dict['A14'] = option14
    # st.write(ud_dict['A14'])

    option15 = st.text_input('15.What is your monthly income?', placeholder="Please input a number (*^▽^*)")
    st.write('Your input is:', option15)
    ud_dict['A15'] = option15
    # st.write(ud_dict['A15'])

    # Change dictionary type to DataFrame
    ud = pd.DataFrame(ud_dict, index=[0])
    if st.button('If you have completed all the above questions, click me ^_^'):
        st.write(ud)


    # The machine learning part

    path = "crx.data"
    names = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8',
             'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16']
    df = pd.read_csv(path, header=None, names=names)
    # print ("Number of data:", len(df))
    df = df.replace("?", np.nan).dropna(how='any')

    # print ("After filtering:", len(df))

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

    # Data segmentation
    X = datas[names[0:-1]]
    Y = datas[names[-1]]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

    X_train.describe().T

    # Construction of logistic algorithm model
    lr = LogisticRegressionCV(Cs=np.logspace(-4, 1, 10),
                              fit_intercept=True, penalty='l2', solver='lbfgs', tol=0.01,
                              multi_class='ovr')
    lr.fit(X_train, Y_train)

    # Logistic algorithm effect output
    lr_r = lr.score(X_train, Y_train)
    '''
    print ("Accuracy：", lr_r)
    print ("Sparse feature ratio：%.2f%%"
      % (np.mean(lr.coef_.ravel() == 0) * 100))
    print ("Parameter：",lr.coef_)
    print ("Intercept：",lr.intercept_)
    '''

    if st.button('See your approvel result'):
        # Process the user data
        def ud_parseRecord(record):
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
            '''
            a16 = record['A16']
            if a16 == '+':
                result.append(1)
            else:
                result.append(0)
            '''
            return result

        ud_new_names = ['A1_0', 'A1_1',
                        'A2', 'A3',
                        'A4_0', 'A4_1', 'A4_2', 'A4_3',
                        'A5_0', 'A5_1', 'A5_2',
                        'A6_0', 'A6_1', 'A6_2', 'A6_3', 'A6_4', 'A6_5', 'A6_6', 'A6_7', 'A6_8', 'A6_9', 'A6_10',
                        'A6_11',
                        'A6_12', 'A6_13',
                        'A7_0', 'A7_1', 'A7_2', 'A7_3', 'A7_4', 'A7_5', 'A7_6', 'A7_7', 'A7_8',
                        'A8',
                        'A9_0', 'A9_1',
                        'A10_0', 'A10_1',
                        'A11',
                        'A12_0', 'A12_1',
                        'A13_0', 'A13_1', 'A13_2',
                        'A14', 'A15']

        ud_datas = ud.apply(lambda x: pd.Series(ud_parseRecord(x), index=ud_new_names), axis=1)
        # st.write(ud_datas)

        # forecast
        y1 = lr.predict(ud_datas)
        # Obtain the probability value (that is, the result value calculated by logistic algorithm)
        #y1 = lr.predict_proba(ud_datas)

        #st.write('Your result predicted by machine is: ', y1)
        if (y1 == 1):
            st.balloons()
            st.success("Congratulations! you are qualified to apply for a credit card")
        if (y1 == 0):
            st.error("Sorry, you are not qualified to apply for a credit card")

