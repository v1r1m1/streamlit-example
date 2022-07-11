import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


class Model:
    def __init__(self):

        self.caption = "Top Cost Drivers"
        self.captionDescription = "These warehouses, users, and queries represent xx% of costs for your account within the last week"
        self.logo = "CapitalOneSOftware.jpg"

        self.dataFrame = self.get_dataframe("5000SalesRecords.csv")
        self.costly_queries = {
            "filename":"5000SalesRecords.csv",
            "caption":"Costly Queries",
            "region":"Asia",
            "Description":"Queries tied to these warehouses have been queuing for a long period of time.",
            "value": "32X",
            "value_description":"higher than average queries"}

        self.costly_users = {
            "filename":"5000SalesRecords.csv",
            "caption":"Costly Users",
            "region":"Europe",
            "Description": "Users consuming the most credits in the past week. This is for each warehouse. ",
            "value": "32\%",
            "value_description":"of 97K accounts total"

        }
        self.costly_warehouses = {
            "filename":"5000SalesRecords.csv",
            "caption":"Costly Warehouses",
            "region":"Central America and the Caribbean",
            "Description":"Queries tied to these warehouses have been queuing for a long period of tim.e",
            "value": "31\%",
            "value_description":"of 97K accounts total"

        }
        self.savings = {
            "question" : "How Much Could You Save?",
            "answer" : "Slingshot users saved and average of 1,234 credits",
            "value" : "# $20,579",
            "valueDescription" : "per month across all of their enterprise accounts.",
            "contactLink" : "Contact Sales",
            "contactDescription" : "to schedule a demo."

            }


    def get_dataframe(self,fileName):
        
        dataFrame = pd.read_csv(fileName,sep=",")

        #dataFrame = dataFrame[(dataFrame['Region'] == filterValue )]
        
        
        #dataFrame = dataFrame.drop_duplicates(subset = "Country").sample(n = 15)
        
        #st.write(dataFrame.head(10))

        #

       
        return dataFrame

    def cw_bar_matplotlib_chart(self,chart_details,dataFrame,range):
        
        self.color_palette_list = ['#8fdae5','#0e6fa4','#04326d', '#3a98d6','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#0c2c84']
        if range =="All":
            pd_gp= dataFrame.sort_values(by=['Unit Cost'], ascending=True)
        else:
            pd_gp= dataFrame.sort_values(by=['Unit Cost'], ascending=True).iloc[-range:]

        #st.write(pd_gp.head(3))
        #st.write(pd_gp)

        fig,ax = plt.subplots()
        hbars = ax.barh(pd_gp['Country'], pd_gp['Unit Cost'],color = self.color_palette_list)
        for i, (value, name,label) in enumerate(zip( pd_gp['Unit Cost'], pd_gp['Country'], pd_gp['Unit Cost'])):
            ax.text(s=name, x=1, y=i, color="w", verticalalignment="center", size=10)
            ax.text(value, i,label,ha='left')  
        ax.axis("off")


     
                
        return fig





def main_view(model):

    
    st.set_page_config(layout="wide", initial_sidebar_state = "collapsed" )
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    local_css("style/MultiColumn.css")

    dataFrame = model.dataFrame
    colNames = list(dataFrame)

    header_container = st.container()

    charts_container = st.container()

    with header_container:

        captionColumn,logoColumn = st.columns([5,2])
        with captionColumn:
            st.header(model.caption)
            st.write(model.captionDescription)
        with logoColumn:
            st.image(model.logo)
    

    
    with charts_container:

        col1,col2,col3= st.columns(3)

        with col1:
            st.header(model.costly_queries["region"] )
            st.subheader(model.costly_queries["caption"]  + "  ⓘ")
            st.write(model.costly_queries["Description"])
            value= model.costly_queries["value"]
            value_description = model.costly_queries["value_description"]
            value_descriptionModified= "\:".join([word+" " for word in value_description.split()])
            st.markdown(f'''### {value} ''')
            st.markdown(value_description)
            st.latex(rf'''\Huge ''' + rf'''{value}''' +rf'''\small '''+ rf'''{value_descriptionModified} ''')
             
            

            dataFrame1 = dataFrame[(dataFrame['Region'] == model.costly_queries["region"] )]

            dataFrame1 = dataFrame1.drop_duplicates(subset = "Country")#.sample(n = 15)
            if dataFrame1.shape[0] >10:
                dataFrame1 = dataFrame1.iloc[0:10]

           
            # Adding 3 of 10 to show all graphs on clicking.
            LengthOfDataFrame = len(dataFrame1.index)
            stringButton = "3 of "+ str(LengthOfDataFrame) + ", View all" + " for " + model.costly_queries["region"]
            container_2 = st.empty()
            viewAll = container_2.button(stringButton)
            #viewAll = st.button(stringButton)
            if viewAll == True:
                container_2.empty()
                container_2.button('"Show only three"')
                fig = model.cw_bar_matplotlib_chart(model.costly_queries,dataFrame1,"All")
            else:
                fig = model.cw_bar_matplotlib_chart(model.costly_queries,dataFrame1,3)

           
            st.pyplot(fig)
            #Create a dropdown menu to select the file
            options = dataFrame1    
            
            #st.write(options["Country"].unique())     
            option = st.selectbox('',['Select a Country'] + options["Country"].unique().tolist())
            #st.write('You selected:', option)
            for item in options.values.tolist():
                #st.write(item)
                for element in item:
                    if element == option:
                        for i in range(len(item)):
                            st.write(colNames[i] ,":", item[i] )

    

        with col2:

            st.header(model.costly_users["region"] )            
            st.subheader(model.costly_users["caption"]+ " ⓘ")
            st.write(model.costly_users["Description"])
            value= model.costly_users["value"]
            value_description = model.costly_users["value_description"]
            value_descriptionModified= "\:".join([word+" " for word in value_description.split()])
            st.markdown(f'''### {value} ''')
            st.markdown(value_description)
            st.latex(rf'''\Huge ''' + rf'''{value}''' +rf'''\small '''+ rf'''{value_descriptionModified} ''')
            
            dataFrame2 = dataFrame[(dataFrame['Region'] == model.costly_users["region"] )]
               
            dataFrame2 = dataFrame2.drop_duplicates(subset = "Country")#.sample(n = 15)
            if dataFrame2.shape[0] >10:
                dataFrame2 = dataFrame2.iloc[0:10]

            LengthOfDataFrame = len(dataFrame2.index)
            stringButton = "3 of "+ str(LengthOfDataFrame) + ", View all"+ " for " + model.costly_users["region"]

            container_2 = st.empty()
            viewAll = container_2.button(stringButton)
            #viewAll = st.button(stringButton)
            if viewAll == True:
                container_2.empty()
                container_2.button("Show only three")
                fig = model.cw_bar_matplotlib_chart(model.costly_users,dataFrame2,"All")
            else:
                fig = model.cw_bar_matplotlib_chart(model.costly_users,dataFrame2,3)
            
            st.pyplot(fig)

            #Create a dropdown menu to select the file
            options =     dataFrame2   
            #st.write(options["Country"].unique())     
            option = st.selectbox('',['Select a Country'] + options["Country"].unique().tolist())
            #st.write('You selected:', option)
            for item in options.values.tolist():
                #st.write(item)
                for element in item:
                    if element == option:
                        for i in range(len(item)):
                            st.write(colNames[i] ,":", item[i] )



        with col3:
            st.header(model.costly_warehouses["region"] )     
            st.subheader(model.costly_warehouses["caption"]+ " ⓘ")
            st.write(model.costly_warehouses["Description"])
            value= model.costly_warehouses["value"]
            value_description = model.costly_warehouses["value_description"]
            value_descriptionModified= "\:".join([word+" " for word in value_description.split()])
            st.markdown(f'''### {value} ''')
            st.markdown(value_description)
            st.latex(rf'''\Huge ''' + rf'''{value}''' +rf'''\small '''+ rf'''{value_descriptionModified} ''')
            
            dataFrame3 = dataFrame[(dataFrame['Region'] == model.costly_warehouses["region"] )]
               
            dataFrame3 = dataFrame3.drop_duplicates(subset = "Country")#.sample(n = 15)
            if dataFrame3.shape[0] >10:
                dataFrame3 = dataFrame3.iloc[0:10]

            #fig = model.cw_bar_chart(model.costly_warehouses,10)
            LengthOfDataFrame = len(dataFrame3.index)
            stringButton = "3 of "+ str(LengthOfDataFrame) + ", View all"+ " for " + model.costly_warehouses["region"]

            container_2 = st.empty()
            viewAll = container_2.button(stringButton)
            #viewAll = st.button(stringButton)
            if viewAll == True:
                container_2.empty()
                container_2.button("Show only three")
                fig = model.cw_bar_matplotlib_chart(model.costly_users,dataFrame3,"All")
            else:
                fig = model.cw_bar_matplotlib_chart(model.costly_users,dataFrame3,3)
            
            st.pyplot(fig)
            #Create a dropdown menu to select the file
            options =    dataFrame3
            #st.write(options["Country"].unique())     
            option = st.selectbox('',['Select a Country'] + options["Country"].unique().tolist())
            #st.write('You selected:', option)
            for item in options.values.tolist():
                #st.write(item)
                for element in item:
                    if element == option:
                        for i in range(len(item)):
                            st.write(colNames[i] ,":", item[i] )




            
       
##################################### start ################################



main_view(Model()) 
