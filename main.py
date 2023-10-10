import streamlit as st
import easyocr
import cv2
import os
import numpy as np
from mysql import connector
from streamlit_option_menu import option_menu
import mysql.connector
import time
import matplotlib.pyplot as plt
from PIL import Image
import re
import pandas as pd

page_bg_img ="""
<style>
[data-testid="stAppViewContainer"]{
       background: #3da7a3;
       background: -webkit-radial-gradient(circle, #3da7a3 0%, #004028 100%);
       background: radial-gradient(circle, #3da7a3 0%, #004028 100%);
       font-family:courier;
       color:#ffffff;
}
</style>
"""
sidepage_bg_img ="""
<style>
[data-testid="stSidebar"][aria-expanded="true"]{
        background: #004028;
 }        
</style>
"""

sidepadding_style ="""
<style>
[data-testid="stSidebar"][aria-expanded="true"]{
        padding-top:2rem;
        padding:0
 }       
</style>
"""


st.set_page_config(page_title="BizcardX",layout='wide')
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
padding_top = 0
st.markdown(page_bg_img,unsafe_allow_html=True)
st.markdown(sidepage_bg_img,unsafe_allow_html=True)
st.markdown(sidepadding_style,unsafe_allow_html=True)

#st.markdown(optiontext_style,unsafe_allow_html=True)
with st.spinner("Loading..."):
    time.sleep(2)
stSidebarContainer = st.sidebar  
with st.sidebar:
    original_title = '<p style="font-family:Courier; color:White; font-size: 30px;">BizcardX</p>'
    st.markdown(original_title,unsafe_allow_html=True)
    select = option_menu(
        menu_title = None,
        options = ["About","Upload & Extract Details","Modify"],
        icons =["house","cloud-upload","pencil-square"],
        default_index=0,
        orientation="vertical",
        styles={"container": {"padding": "0!important", "background-color": "","size":"cover", "width": "100%"},
            "icons": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "color":"#004028","font-family":"Courier","text-align": "center", "margin": "-2px", "--hover-color": "#3da7a3"},
            "nav-link-selected": {"background-color": "#3da7a3"},
            "icons-selected": {"color":"#fff"}})
    
image_path = "C:/Users/Natarajan/Desktop/Dhivya/DS/capstone/BizcardX/3.png"
img = cv2.imread(image_path) 
reader = easyocr.Reader(['en'],gpu = False)
result = reader.readtext(img)
#for i in result:
 # st.write(i[1])  

#Establishing Sqlite3 connectivity
con = mysql.connector.connect(host = "localhost",
                                user = "root",
                                password = "1234",
                                database = "bizcardx")

c = con.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50) ,
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB,
                    CONSTRAINT mobile_unique UNIQUE (mobile_number)

                    )''')

if select == "About":
    header12 = '<p style="font-family:Courier; color:White; font-size: 26px;">BizcardX: Extracting Business Card Data with OCR</p>'
    st.markdown(header12,unsafe_allow_html=True)
    st.divider()
    col1 , col2 = st.columns([6,5],gap="medium")
    with col2:
       img = Image.open("C:\\Users\\Natarajan\\Desktop\\Dhivya\\DS\\capstone\\BizcardX\\img.jpg")
       new_image = img.resize((600, 550)) 
       # st.image(Image.open("C:\\Users\\Natarajan\\Desktop\\Dhivya\\DS\\capstone\\BizcardX\\img.jpg"),width=500,height = 500)
       st.image(new_image) 
    with col1:
       #header13 = '<p style="font-family:Courier; color:White; font-size: 26px;">About:</p>'
       #st.markdown(header13,unsafe_allow_html=True)
       st.write("##### Bizcard is a Python application designed to extract information from business cards.")
       st.write('##### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
       header14 = '<p style="font-family:Courier; color:White; font-size: 26px;">Technologies Used:</p>'
       st.markdown(header14,unsafe_allow_html=True)
       st.write("##### Python,easy OCR, Streamlit, MySQL, Pandas")

if select == "Upload & Extract Details":
    header1 = '<p style="font-family:Courier; color:White; font-size: 30px;">Upload a Business Card</p>'
    st.markdown(header1,unsafe_allow_html= True)
    uploaded_card = st.file_uploader("upload here",label_visibility="collapsed",type=["png","jpeg","jpg"])
   
    if uploaded_card is not None:

        def save_card(uploaded_card):
            uploaded_cards_dir = os.path.join(os.getcwd(), "uploaded_cards")
            with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())


        save_card(uploaded_card)

        def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)  
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            header2 = '<p style="font-family:Courier; color:White; font-size: 30px;">You have uploaded the card</p>'
            st.markdown(header2,unsafe_allow_html=True)
            st.image(uploaded_card) 
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                header3 = '<p style="font-family:Courier; color:White; font-size: 30px;">Image Processed and Data Extracted</p>'
                st.markdown(header3,unsafe_allow_html=True)
                #st.markdown("### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))
                # easy Optical Character Recognition
        saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
        result = reader.readtext(saved_img, detail=0, paragraph=False)
                
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData
        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                "image": img_to_binary(saved_img)
                }
        def get_data(res):
            for ind, i in enumerate(res):

                # To get WEBSITE_URL
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = res[4] + "." + res[5]

                # To get EMAIL ID
                elif "@" in i:
                    data["email"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["company_name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["area"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)

                # To get PINCODE
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])


        get_data(result)

        def create_df(data):
            df = pd.DataFrame(data)
            return df
        df = create_df(data)
        header9= '<p style="font-family:Courier; color:White; font-size: 30px;">Data Extracted</p>'
        st.markdown(header9,unsafe_allow_html=True)
        #st.success("### Data Extracted!")
        st.write(df)

        if st.button(":green[Upload to Database]"):
            for i, row in df.iterrows():
                # here %S means string values
                try:
                    
                    sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
                    c.execute(sql, tuple(row))
                    # the connection is not auto committed by default, so we must commit to save our changes
                    con.commit()
                    st.success("#### Uploaded to database successfully!")
                except:
                    st.warning("Data already exists in the database")    

        if st.button(":green[View updated data]"):
            c.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
            updated_df = pd.DataFrame(c.fetchall(),
                                          columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Area", "City", "State", "Pin_Code"])
            st.write(updated_df)

if select == "Modify": 
    header4 = '<p style="font-family:Courier; color:White; font-size: 30px;">You can view , alter or delete the extracted data in this app</p>'
    st.markdown(header4,unsafe_allow_html=True)

    #st.subheader(':blue[You can view , alter or delete the extracted data in this app]')
    st.markdown("""
        <style>
        div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
            font-family:Courier;
            font-size:20px;
            color:#ffffff;
                
        } 
        div[class*="stRadio"] > options > div[data-testid="stMarkdownContainer"] > p {
            font-family:Courier;
            font-size:20px;
            color:#ffffff;
                
        }      
      </style>  
    """,unsafe_allow_html=True)
    
    #option = ["View", "Alter","Delete"] 
    #st.radio(label='Select an option', options=option,horizontal=True)  
    option = st.radio("Select an Option",('View','Alter','Delete'),horizontal = True)
    
    if option == "View":
        c.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        view_df = pd.DataFrame(c.fetchall(),columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number","Email","Website", "Area", "City", "State", "Pin_Code"])
        header5 = '<p style="font-family:Courier; color:White; font-size: 20px;">The details of extracted card:</p>'
        st.markdown(header5,unsafe_allow_html=True)
        #st.subheader(':blue[The details of extracted card:]')                                            
        st.write(view_df)

    if option == "Alter":
        header6 = '<p style="font-family:Courier; color:White; font-size: 20px;">Alter the data here</p>'
        st.markdown(header6,unsafe_allow_html=True)
        #st.markdown(":blue[Alter the data here]")

        try:
            c.execute("SELECT card_holder FROM card_data")
            result = c.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                header6 = '<p style="font-family:Courier; color:White; font-size: 20px;">No card selected</p>'
                st.markdown(header6,unsafe_allow_html=True)
                #st.write("No card selected.")
            else:
                header7 = '<p style="font-family:Courier; color:White; font-size: 20px;">Update or Modify any data below</p>'
                st.markdown(header7,unsafe_allow_html=True)
                #st.markdown("#### Update or modify any data below")
                c.execute(
                "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                (selected_card,))
                result = c.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                company_name = st.text_input("Company_Name", result[0])
                card_holder = st.text_input("Card_Holder", result[1])
                designation = st.text_input("Designation", result[2])
                mobile_number = st.text_input("Mobile_Number", result[3])
                email = st.text_input("Email", result[4])
                website = st.text_input("Website", result[5])
                area = st.text_input("Area", result[6])
                city = st.text_input("City", result[7])
                state = st.text_input("State", result[8])
                pin_code = st.text_input("Pin_Code", result[9])


                if st.button(":green[Commit changes to DB]"):


                   # Update 
                    c.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code,
                    selected_card))
                    con.commit()
                    header10 = '<p style="font-family:Courier; color:White; font-size: 30px;">Information updated in database successfully.</p>'
                    st.markdown(header10,unsafe_allow_html=True)
                    #st.success("Information updated in database successfully.")

                if st.button(":green[View updated data]"):
                    c.execute(
                        "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
                    updated_df = pd.DataFrame(c.fetchall(),
                                            columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                    "Email",
                                                    "Website", "Area", "City", "State", "Pin_Code"])
                    st.write(updated_df)

        except:
            st.warning("There is no data available in the database")
           
    if option == "Delete": 
        st.markdown(
            """
            <style>
            .streamlit-selectbox label {
                color: #fffff;
                font-family:Courier;
                font-size: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
 
        header8 = '<p style="font-family:Courier; color:White; font-size: 20px;">Delete the data </p>'
        st.markdown(header8,unsafe_allow_html=True)      
        #st.subheader(":blue[Delete the data]")
        try:
            c.execute("SELECT card_holder FROM card_data")
            result = c.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                header13 =f"""<p style="font-family:Courier; color:White; font-size: 24px;">You have selected : {selected_card}'s card to delete </p>"""
                st.markdown(header13,unsafe_allow_html=True)
                
                #st.markdown(f"### You have selected :green[**{selected_card}'s**] card to delete")
                header15 = '<p style="font-family:Courier; color:White; font-size: 20px;">Proceed to delete this card? </p>'
                st.markdown(header15,unsafe_allow_html=True)
                #st.write("#### Proceed to delete this card?")
                if st.button(":green[Yes Delete Business Card]"):
                    c.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                    con.commit()
                    header11 = '<p style="font-family:Courier; color:White; font-size: 20px;">Business card information deleted from database successfully.</p>'
                    st.markdown(header11,unsafe_allow_html=True)
                    #st.success("Business card information deleted from database.")

            if st.button(":green[View updated data]"):
                c.execute(
                    "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
                updated_df = pd.DataFrame(c.fetchall(),
                                            columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                    "Email",
                                                    "Website", "Area", "City", "State", "Pin_Code"])
                st.write(updated_df)

        except:
            
            st.warning("There is no data available in the database")    

              
