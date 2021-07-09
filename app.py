
import pickle
import streamlit as st
import pandas as pd

# loading the trained model
pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)

@st.cache()

# defining the function which will make the prediction using the data which the user inputs 
def prediction(df_cp):   
    
    df_cp.loc[ df_cp['totalIncome'] <= 6000, 'totalIncome'] = 0
    df_cp.loc[(df_cp['totalIncome'] > 6000) & (df_cp['totalIncome'] <= 11000), 'totalIncome'] = 1
    df_cp.loc[(df_cp['totalIncome'] > 11000) & (df_cp['totalIncome'] <= 17000), 'totalIncome'] = 2
    df_cp.loc[(df_cp['totalIncome'] > 17000) & (df_cp['totalIncome'] <= 33000), 'totalIncome'] = 3
    df_cp.loc[(df_cp['totalIncome'] > 33000) & (df_cp['totalIncome'] <= 49000), 'totalIncome'] = 4
    df_cp.loc[(df_cp['totalIncome'] > 49000) & (df_cp['totalIncome'] <= 65000), 'totalIncome'] = 5
    df_cp.loc[ df_cp['totalIncome'] > 65000, 'totalIncome'] = 6

    df_cp.loc[ df_cp['Loan_Amount_Term'] <= 120, 'Loan_Amount_Term'] = 0
    df_cp.loc[(df_cp['Loan_Amount_Term'] > 120) & (df_cp['Loan_Amount_Term'] <= 240), 'Loan_Amount_Term'] = 1
    df_cp.loc[(df_cp['Loan_Amount_Term'] > 240) & (df_cp['Loan_Amount_Term'] <= 360), 'Loan_Amount_Term'] = 2
    df_cp.loc[(df_cp['Loan_Amount_Term'] > 360) & (df_cp['Loan_Amount_Term'] <= 480), 'Loan_Amount_Term'] = 3
    
    #df_cp.Gender = df_cp.Gender.map({'Male': 1, 'Female':0})
    df_cp.Education = df_cp.Education.map({'Graduate': 1, 'Not Graduate':0})
    df_cp.Self_Employed = df_cp.Self_Employed.map({'No': 0, 'Yes':1})
    df_cp.Married = df_cp.Married.map({'Unmarried': 0, 'Married':1})
    df_cp.Dependents = df_cp.Dependents.map({'0': 0, '1':1, '2':2, '3+':3})
    df_cp.Property_Area = df_cp.Property_Area.map({'Rural': 0, 'Urban':1, 'Semiurban':2})
    df_cp.Credit_History = df_cp.Credit_History.map({'Unclear Debts': 0, 'No Unclear Debts':1})
    
    df_cp.LoanAmount = df_cp.LoanAmount/1000

        
    # Making predictions 
    prediction = classifier.predict(df_cp)
    
    print(prediction)
    if prediction == 0:
        pred = 'Rejected'
    else:
        pred = 'Approved'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page
    html_temp = """
    <div style ="background-color:yellow;padding:13px">
    <h1 style ="color:black;text-align:center;">Streamlit Loan Prediction ML App</h1>
    </div>
    """
    
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True)
    
    # following lines create boxes in which user can enter data required to make prediction 
    Gender = st.selectbox('Gender', ("Male", "Female"))
    Married = st.selectbox('Marital Status', ("Unmarried", "Married"))
    Education = st.selectbox('Education', ("Graduate", "Not Graduate"))
    Self_Employed = st.selectbox('Self Employed', ("Yes", "No"))
    Dependents = st.selectbox('Dependents', ("0","1","2","3+"))
    totalIncome = st.number_input("Applicants monthly total income (Applicant + Coapplicant if there is one)")
    Loan_Amount_Term = st.number_input("Loan Amount Term (days)")
    LoanAmount = st.number_input("Total loan amount")
    Property_Area = st.selectbox('Property Area', ("Urban", "Rural", "Semiurban"))
    Credit_History = st.selectbox('Credit_History', ("Unclear Debts","No Unclear Debts"))
    df = pd.DataFrame(data=[[Married,Education,Self_Employed,Dependents,totalIncome,Loan_Amount_Term,
                     LoanAmount,Property_Area,Credit_History]], columns=['Married','Education','Self_Employed'
                                                                        ,'Dependents', 'totalIncome', 'Loan_Amount_Term',
                                                                        'LoanAmount', 'Property_Area', 'Credit_History'])
    result = ""
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(df) 
        st.success('Your loan is {}'.format(result))
        print(LoanAmount)
     
if __name__=='__main__': 
    main()
