import streamlit as st
import time

def app():
    with st.container():
        st.subheader('Hello, this is the website for our Machine Learning Function :smile:')
        st.write(
            'You can choose in the sidebar on the left'
        )
        st.write('###')
        st.write(
            """
            This website contains:
            - A homepage introduce our working
            - A function page in which you can try our prediction function
            - A data page in which you can see the data and the result of our ML work
            """
        )

    with st.container():
        st.write("---")# Split line
        l_col, r_col = st.columns(2)
        with l_col:
            st.image('Images/1.png', width = 200)
        with r_col:
            st.write('###')
            st.write('This is also the topic from the book: Learning From Data')
            st.write('[Click here to learn more...](https://www.csie.ntu.edu.tw/~htlin/mooc/)')

    with st.container():
        st.write('---')
        l_col1, r_col1 = st.columns(2)
        with l_col1:
            st.write('###')
            st.image('Images/2.png', width = 200)
        with r_col1:
            st.write('###')
            st.write('The data set we use is downloaded from UCI machine learning repository')
            st.write('[Click here to learn more...](http://archive.ics.uci.edu/ml/datasets/Credit+Approval)')
        st.write('###')
        st.write('###')
        st.write('---')





