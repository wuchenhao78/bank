import streamlit as st
from multipage import MultiPage
from Pages import special_function, basic_function, machine_learning

st.set_page_config(page_title='Bank System App', page_icon=":smile:",layout='wide')
st.title('Bank System')
# instantiation
app = MultiPage()
# add applications
app.add_page('Home Page', basic_function.app)
app.add_page('Machine Learning', machine_learning.app)
app.add_page('Credit Card Approval', special_function.app)

# run
if __name__ == '__main__':
    app.run()
