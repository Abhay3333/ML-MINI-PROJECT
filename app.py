import streamlit as st
import modelling as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt


def display_project_details():
    st.subheader("Project Details")
    st.write("This ML-based app is developed for educational purposes. The objective of the app is detecting phishing websites using only content data, not URLs.")
    st.write("Below is the distribution of phishing and legitimate websites in the dataset:")
    with st.expander("Dataset Distribution"):
        # ----- FOR THE PIE CHART ----- #
        labels = 'Phishing', 'Legitimate'
        phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
        legitimate_rate = 100 - phishing_rate
        sizes = [phishing_rate, legitimate_rate]
        explode = (0.1, 0)
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
        # ----- !!!!! ----- #


def display_example_urls():
    st.subheader("Example Phishing URLs")
    st.write("_https://rtyu38.godaddysites.com/_")
    st.write("_https://karafuru.invite-mint.com/_")
    st.write("_https://defi-ned.top/h5/#/_")
    st.write("REMEMBER, PHISHING WEB PAGES HAVE SHORT LIFECYCLE! SO, THE EXAMPLES SHOULD BE UPDATED!")


def select_machine_learning_model():
    st.subheader("Select Machine Learning Model")
    choice = st.selectbox("Please select your machine learning model",
                          [
                              'Gaussian Naive Bayes', 'Support Vector Machine', 'Decision Tree', 'Random Forest',
                              'AdaBoost', 'Neural Network', 'K-Neighbours'
                          ]
                          )

    if choice == 'Gaussian Naive Bayes':
        model = ml.nb_model
        st.write('GNB model is selected!')
    elif choice == 'Support Vector Machine':
        model = ml.svm_model
        st.write('SVM model is selected!')
    elif choice == 'Decision Tree':
        model = ml.dt_model
        st.write('DT model is selected!')
    elif choice == 'Random Forest':
        model = ml.rf_model
        st.write('RF model is selected!')
    elif choice == 'AdaBoost':
        model = ml.ab_model
        st.write('AB model is selected!')
    elif choice == 'Neural Network':
        model = ml.nn_model
        st.write('NN model is selected!')
    else:
        model = ml.kn_model
        st.write('KN model is selected!')

    return model


def analyze_url(model, url):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code != 200:
            st.error("HTTP connection was not successful for the URL: {}".format(url))
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
            result = model.predict(vector)
            if result[0] == 0:
                st.success("This web page seems legitimate!", icon="✅")
            else:
                st.warning("Attention! This web page is a potential PHISHING!", icon="⚠️")

    except re.exceptions.RequestException as e:
        st.error("An error occurred: {}".format(e))


st.title('Phishing Website Detection using Machine Learning')

display_project_details()

display_example_urls()

selected_model = select_machine_learning_model()

url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    with st.spinner('Analyzing...'):
        analyze_url(selected_model, url)
