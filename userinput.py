import math
import numpy as np
import pandas as pd
import streamlit as st
from scipy import stats

inv_cost=0
inv_cost_2=0
inv_cost_3=0
inv_cost_4=0
inv_cost_5=0

operation_cost=0
operation_cost_2=0
operation_cost_3=0
operation_cost_4=0
operation_cost_5=0

###### input Section ####
st.set_page_config(page_title="Supply Chain Wizard",layout="wide")

add_selectbox = st.selectbox(
    "Please the product",
    ( "Product 1", "Product 2", "Product 3","Product 4", "Product 5")
)

#### prodcut 1  ######
if add_selectbox == "Product 1":  
    st.title("Product Detail Information")
    st.header("Product 1 Information")
    mean = 100 #can be changed to the analysis mean
    std = 200 #can be changed to the analysis standard deviation
    Total_demand = mean*365
    holding_cost = st.number_input("Please input the holding cost($/unit) of product 1")
    st.write("current holding cost of product 1 is $",holding_cost,"/unit")
    st.write("\n")
    bo_cost = st.number_input("Please input the back order cost($/unit) of product 1")
    st.write("current backorder cost of product 1 is $",bo_cost,"/unit")
    st.write("\n")
    
    
    logistic_option = st.selectbox(
         'What is the delivery method of product 1',
         ('Marine Shipping', 'Air Cargo'))
    st.write('You selected:', logistic_option)
    
    if logistic_option == 'Marine Shipping':
        shipping_time = 30
        shipping_cost = 0.05
    if logistic_option == 'Air Cargo':
        shipping_time = 2
        shipping_cost = 20
    st.write("Current shipping cost is $", shipping_cost,"/unit")
    st.write("Current shipping time is ", shipping_time,"days")
    if holding_cost != 0 and bo_cost != 0:        
        EOQ = np.sqrt(2*shipping_cost*mean/holding_cost)
        st.write("Most economical order size",int(EOQ),"units")
    
    
    st.write("\n")
    st.write("\n")
    if holding_cost != 0 and bo_cost != 0:        
        critical_ratio = bo_cost/(bo_cost+holding_cost)
        st.write("Most ecnomical fill rate", round(critical_ratio,2)*100,"%")
    service_level = st.slider('What is the fill Rate you want to achieve', 0, 100, 25)
    st.write("Current Fill rate is", service_level, '%')
    
    target_inv =  shipping_time*mean+stats.norm.ppf(service_level/100)*std
    order_size = shipping_time*mean
    average_inv = (target_inv + (stats.norm.ppf(service_level/100)*std))/2
    order_times = int(365/shipping_time)
    inv_cost = average_inv*shipping_time*order_times*holding_cost
    operation_cost = inv_cost+order_times*shipping_cost
    st.write("\n")
    st.write("\n")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory  of product 1", value=int(target_inv))
    col2.metric(label="Inventory cost of product 1", value=int(inv_cost))
    col3.metric(label="Operation cost of product 1", value=int(operation_cost))
    x = np.linspace(0,100,100)
    y_list = []
    for i in range(1,100):
        t_inv =  shipping_time*mean+stats.norm.ppf(i/100)*std
        a_inv = (t_inv + (stats.norm.ppf(i/100)*std))/2
        o_times = int(365/shipping_time)
        i_cost = a_inv*shipping_time*o_times*holding_cost
        y = i_cost+o_times*shipping_cost
        y_list.append(y)
    st.line_chart(y_list)



#### Product 2 #####
elif add_selectbox == "Product 2":
    st.title("Product Detail Information")
    st.header("Product 2 Information")
    mean_2 = 100 #can be change to the analysis result
    std_2 = 200 #can be change to the analysis result
    holding_cost_2 = st.number_input("Please input the holding cost($/unit) of product 2")
    st.write("current holding cost of product 1 is $",holding_cost_2,"/unit")
    st.write("\n")
    bo_cost_2 = st.number_input("Please input the back order cost($/unit) of product 2")
    st.write("current backorder cost of product 2 is $",bo_cost_2,"/unit")
    st.write("\n")
    
    
    logistic_option_2 = st.selectbox(
         'What is the delivery method of product 3',
         ('Marine Shipping', 'Air Cargo'))
    st.write('You selected:', logistic_option_2)
    
    if logistic_option_2 == 'Marine Shipping':
        shipping_time_2 = 30
        shipping_cost_2 = 0.05
    if logistic_option_2 == 'Air Cargo':
        shipping_time_2 = 2
        shipping_cost_2 = 20
    st.write("Current shipping cost is $", shipping_cost_2,"/unit")
    st.write("Current shipping time is ", shipping_time_2,"days")
    if holding_cost_2 != 0 and bo_cost_2 != 0:        
        EOQ_2 = np.sqrt(2*shipping_cost_2*mean_2/holding_cost_2)
        st.write("Most economical order size",int(EOQ_2),"units")
    
    
    st.write("\n")
    st.write("\n")
    if holding_cost_2 != 0 and bo_cost_2 != 0:        
        critical_ratio_2 = bo_cost_2/(bo_cost_2+holding_cost_2)
        st.write("Most ecnomical fill rate", round(critical_ratio_2,2)*100,"%")
    service_level_2 = st.slider('What is the fill Rate you want to achieve', 0, 100, 25)
    st.write("Current Fill rate is", service_level_2, '%')
    
    target_inv_2 =  shipping_time_2*mean_2+stats.norm.ppf(service_level_2/100)*std_2
    order_size_2 = shipping_time_2*mean_2
    average_inv_2 = (target_inv_2 + (stats.norm.ppf(service_level_2/100)*std_2))/2
    order_times_2 = int(365/shipping_time_2)
    inv_cost_2 = average_inv_2*shipping_time_2*order_times_2*holding_cost_2
    operation_cost_2 = inv_cost_2+order_times_2*shipping_cost_2
    st.write("\n")
    st.write("\n")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory  of product 2", value=int(target_inv_2))
    col2.metric(label="Inventory cost of product 2", value=int(inv_cost_2))
    col3.metric(label="Operation cost of product 2", value=int(operation_cost_2))


#### Product 3 #####
elif add_selectbox == "Product 3":
    st.title("Product Detail Information")
    st.header("Product 3 Information")
    mean_3 = 100 #can be change to the analysis result
    std_3 = 200 #can be change to the analysis result
    holding_cost_3 = st.number_input("Please input the holding cost($/unit) of product 3")
    st.write("current holding cost of product 3 is $",holding_cost_3,"/unit")
    st.write("\n")
    bo_cost_3 = st.number_input("Please input the back order cost($/unit) of product 3")
    st.write("current backorder cost of product 3 is $",bo_cost_3,"/unit")
    st.write("\n")
    
    
    logistic_option_3 = st.selectbox(
         'What is the delivery method of product 3',
         ('Marine Shipping', 'Air Cargo'))
    st.write('You selected:', logistic_option_3)
    
    if logistic_option_3 == 'Marine Shipping':
        shipping_time_3= 30
        shipping_cost_3 = 0.05
    if logistic_option_3 == 'Air Cargo':
        shipping_time_3 = 2
        shipping_cost_3 = 20
    st.write("Current shipping cost is $", shipping_cost_3,"/unit")
    st.write("Current shipping time is ", shipping_time_3,"days")
    if holding_cost_3 != 0 and bo_cost_3 != 0:        
        EOQ_3 = np.sqrt(2*shipping_cost_2*mean_3/holding_cost_3)
        st.write("Most economical order size",int(EOQ_2),"units")
    
    
    st.write("\n")
    st.write("\n")
    if holding_cost_3 != 0 and bo_cost_3 != 0:        
        critical_ratio_3 = bo_cost_3/(bo_cost_3+holding_cost_3)
        st.write("Most ecnomical fill rate", round(critical_ratio_3,2)*100,"%")
    service_level_3 = st.slider('What is the fill Rate you want to achieve', 0, 100, 25)
    st.write("Current Fill rate is", service_level_3, '%')
    
    target_inv_3 =  shipping_time_3*mean_3+stats.norm.ppf(service_level_3/100)*std_3
    order_size_3 = shipping_time_3*mean_3
    average_inv_3 = (target_inv_3 + (stats.norm.ppf(service_level_3/100)*std_3))/2
    order_times_3 = int(365/shipping_time_3)
    inv_cost_3 = average_inv_3*shipping_time_3*order_times_3*holding_cost_3
    operation_cost_3 = inv_cost_3+order_times_3*shipping_cost_3
    st.write("\n")
    st.write("\n")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory  of product 2", value=int(target_inv_3))
    col2.metric(label="Inventory cost of product 2", value=int(inv_cost_3))
    col3.metric(label="Operation cost of product 2", value=int(operation_cost_3))

### Product 4 ###
elif add_selectbox == "Product 4":
    st.title("Product Detail Information")
    st.header("Product 4 Information")
    mean_4 = 100 #can be change to the analysis result
    std_4 = 200 #can be change to the analysis result
    holding_cost_4 = st.number_input("Please input the holding cost($/unit) of product 4")
    st.write("current holding cost of product 4 is $",holding_cost_4,"/unit")
    st.write("\n")
    bo_cost_4 = st.number_input("Please input the back order cost($/unit) of product 4")
    st.write("current backorder cost of product 4 is $",bo_cost_4,"/unit")
    st.write("\n")
    
    
    logistic_option_4 = st.selectbox(
         'What is the delivery method of product 4',
         ('Marine Shipping', 'Air Cargo'))
    st.write('You selected:', logistic_option_4)
    
    if logistic_option_4 == 'Marine Shipping':
        shipping_time_4= 30
        shipping_cost_4 = 0.05
    if logistic_option_4 == 'Air Cargo':
        shipping_time_4 = 2
        shipping_cost_4 = 20
    st.write("Current shipping cost is $", shipping_cost_4,"/unit")
    st.write("Current shipping time is ", shipping_time_4,"days")
    if holding_cost_4 != 0 and bo_cost_4 != 0:        
        EOQ_4 = np.sqrt(2*shipping_cost_4*mean_4/holding_cost_4)
        st.write("Most economical order size",int(EOQ_4),"units")
    
    
    st.write("\n")
    st.write("\n")
    if holding_cost_4 != 0 and bo_cost_4 != 0:        
        critical_ratio_4 = bo_cost_4/(bo_cost_4+holding_cost_4)
        st.write("Most ecnomical fill rate", round(critical_ratio_4,2)*100,"%")
    service_level_4 = st.slider('What is the fill Rate you want to achieve', 0, 100, 25)
    st.write("Current Fill rate is", service_level_4,'%')
    
    target_inv_4 =  shipping_time_4*mean_4+stats.norm.ppf(service_level_4/100)*std_4
    order_size_4 = shipping_time_4*mean_4
    average_inv_4 = (target_inv_4 + (stats.norm.ppf(service_level_4/100)*std_4))/2
    order_times_4 = int(365/shipping_time_4)
    inv_cost_4 = average_inv_4*shipping_time_4*order_times_4*holding_cost_4
    operation_cost_4 = inv_cost_4+order_times_4*shipping_cost_4
    st.write("\n")
    st.write("\n")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory  of product 4", value=int(target_inv_4))
    col2.metric(label="Inventory cost of product 4", value=int(inv_cost_4))
    col3.metric(label="Operation cost of product 4", value=int(operation_cost_4))

### Product 5 ###
elif add_selectbox == "Product 5":
    st.title("Product Detail Information")
    st.header("Product 5 Information")
    mean_5 = 100 #can be change to the analysis result
    std_5 = 200 #can be change to the analysis result
    holding_cost_5 = st.number_input("Please input the holding cost($/unit) of product 5")
    st.write("current holding cost of product 4 is $",holding_cost_5,"/unit")
    st.write("\n")
    bo_cost_5 = st.number_input("Please input the back order cost($/unit) of product 5")
    st.write("current backorder cost of product 5 is $",bo_cost_5,"/unit")
    st.write("\n")
    
    
    logistic_option_5 = st.selectbox(
         'What is the delivery method of product 5',
         ('Marine Shipping', 'Air Cargo'))
    st.write('You selected:', logistic_option_5)
    
    if logistic_option_5 == 'Marine Shipping':
        shipping_time_5= 30
        shipping_cost_5 = 0.05
    if logistic_option_5 == 'Air Cargo':
        shipping_time_5 = 2
        shipping_cost_5 = 20
    st.write("Current shipping cost is $", shipping_cost_5,"/unit")
    st.write("Current shipping time is ", shipping_time_5,"days")
    if holding_cost_5 != 0 and bo_cost_5 != 0:        
        EOQ_5 = np.sqrt(2*shipping_cost_5*mean_5/holding_cost_5)
        st.write("Most economical order size",int(EOQ_5),"units")
    
    
    st.write("\n")
    st.write("\n")
    if holding_cost_5 != 0 and bo_cost_5 != 0:        
        critical_ratio_5 = bo_cost_5/(bo_cost_5+holding_cost_5)
        st.write("Most ecnomical fill rate", round(critical_ratio_5,2)*100,"%")
    service_level_5 = st.slider('What is the fill Rate you want to achieve', 0, 100, 25)
    st.write("Current Fill rate is", service_level_5,'%')
    
    target_inv_5 =  shipping_time_5*mean_5+stats.norm.ppf(service_level_5/100)*std_5
    order_size_5 = shipping_time_5*mean_5
    average_inv_5 = (target_inv_5 + (stats.norm.ppf(service_level_5/100)*std_5))/2
    order_times_5 = int(365/shipping_time_5)
    inv_cost_5 = average_inv_5*shipping_time_5*order_times_5*holding_cost_5
    operation_cost_5 = inv_cost_5+order_times_5*shipping_cost_5
    st.write("\n")
    st.write("\n")
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Target inventory  of product 5", value=int(target_inv_5))
    col2.metric(label="Inventory cost of product 5", value=int(inv_cost_5))
    col3.metric(label="Operation cost of product 5", value=int(operation_cost_5))

##### Out Put Section #####
inv_all = inv_cost + inv_cost_2+ inv_cost_3 + inv_cost_4+ inv_cost_5
operation_all = operation_cost + operation_cost_2 + operation_cost_3 + operation_cost_4 + operation_cost_5
