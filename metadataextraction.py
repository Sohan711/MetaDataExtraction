import streamlit as st

# import streamlit.components.v1 as stc

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
from datetime import datetime

# opening file
# for images
from PIL import Image
import exifread
# for audio
import mutagen
# for pdf
from PyPDF2 import PdfReader
#database management
import sqlite3
conn = sqlite3.connect('data.db')
c=conn.cursor()
#table
def create_uploaded_filetable():
    c.execute('CREATE TABLE IF NOT EXISTS filestable(filename TEXT,filetype TEXT,filesize TEXT,uploadDate TIMESTAMP)')

#adding details 
def add_file_details(filename,filetype,filesize,uploadDate):
    c.execute('INSERT INTO filestable(filename,filetype,filesize,uploadDate) VALUES (?,?,?,?)',(filename,filetype,filesize,uploadDate))
    conn.commit()

#viewing the details
def view_all_data():
    c.execute('SELECT * FROM filestable')
    data = c.fetchall()
    return data

#Functions
@st.cache_data
def load_image(image_file):
    img = Image.open(image_file)
    return img
# function to get human readable time
def get_readable_time(mytime):
    return datetime.fromtimestamp(mytime).strftime('%Y-%m-%d-%H:%M')




metadata_wiki = """
Metadata is defined as the data providing information about one or more aspects of the data; it is used to summarize basic information
 about data which can make tracking and working with specific data easier
"""

def main():
    st.title("MetaData Extraction App")
    

    menu = ["Home","Image","Audio","DocumentFiles","DataAnalytics","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    create_uploaded_filetable()

    if choice == "Home":
        st.subheader("Home")
        st.image(load_image("Resources/Images/data.png"))
        st.write(metadata_wiki)

        #expander and columns
        col1,col2,col3 = st.columns(3)
        with col1:
            with st.expander('Get Image Metadata 📷'):
                st.info("Image MetaData")
                st.markdown("📷")
                st.text("Upload JPEG,PJPG,PNG Images")
                
        
        with col2:
            with st.expander('Get Audio Metadata 🔉'):
                st.info("Audio MetaData")
                st.markdown("🔉")
                st.text("Upload MP3,Ogg Images")

        with col3:
            with st.expander('Get DocumentFile Metadata'):
                st.info("DocumentFiles MetaData")
                st.markdown("📄📁")
                st.text("Upload PDF,Docx ocumentFiless")

    elif choice == "Image":
        st.subheader("Image MetaData Extraction")
        image_file = st.file_uploader("Upload Image",type=["png", "jpg", "jpeg"])
        if image_file is not None:
            #Binary byte
            # st.write(type(image_file))
            # st.write(dir(image_file))
            with st.expander("File stats"):
                file_details = {
                    "FileName": image_file.name,
                    "FileSize": image_file.size,
                    "FileType": image_file.type,
                }
                st.write(file_details)

                statinfo = os.stat(image_file.readable())
                st.write(statinfo)
                stats_details = {
                    "Accessed_Time": get_readable_time(statinfo.st_atime),
                    "Creation_Time": get_readable_time(statinfo.st_ctime),
                    "Modified_Time": get_readable_time(statinfo.st_mtime),
                }
                st.write(stats_details)
                # combining all datails
                file_details_combined = {
                    "FileName": image_file.name,
                    "FileSize": image_file.size,
                    "FileType": image_file.type,
                    "Accessed_Time": get_readable_time(statinfo.st_atime),
                    "Creation_Time": get_readable_time(statinfo.st_ctime),
                    "Modified_Time": get_readable_time(statinfo.st_mtime),
                }
                
                df_img_details_default = pd.DataFrame(list(file_details_combined.items()), columns=["Meta Tags", "Value"])
                st.dataframe(df_img_details_default)

                #track details
                add_file_details(image_file.name,image_file.type,image_file.size,datetime.now())

            # with st.expander("View Image"):
            #     img = load_image(image_file)
            #     st.image(img,width=250)


            fcol1, fcol2 = st.columns(2)

            with fcol1:
                with st.expander("View Image"):
                    img = load_image(image_file)
                    st.image(img,width=250)
                

            with fcol2:
                with st.expander("Default(JEPG)"):
                    st.info("Using Pillow")
                    img = load_image(image_file)
                    img_details = {"format":img.format,
                                   "format_desc":img.format_description,
                                   "size":img.size,"height":img.height,
                                   "info":img.info}
                    st.write(img_details)

                    df_img_details_default = pd.DataFrame(list(file_details.items()), columns=["Meta Tags", "Value"])
                    st.dataframe(df_img_details_default)
                    

            


    elif choice == "Audio":

        st.subheader("Audio MetaData Extraction")
        # File Upload
        audio_file = st.file_uploader("Upload Audio", type=["mp3", "ogg"])

        if audio_file is not None:

            # Layouts
            col1, col2 = st.columns(2)

            with col1:
                st.audio(audio_file.read())

            with col2:
                with st.expander("File Stats"):
                    file_details = {
                        "FileName": audio_file.name,
                        "FileSize": audio_file.size,
                        "FileType": audio_file.type,
                    }
                    st.write(file_details)

                    statinfo = os.stat(audio_file.readable())
                    # st.write(statinfo)
                    stats_details = {
                        "Accessed_Time": get_readable_time(statinfo.st_atime),
                        "Creation_Time": get_readable_time(statinfo.st_ctime),
                        "Modified_Time": get_readable_time(statinfo.st_mtime),
                    }
                    st.write(stats_details)

                    # Combine All Details
                    file_details_combined = {
                        "FileName": audio_file.name,
                        "FileSize": audio_file.size,
                        "FileType": audio_file.type,
                        "Accessed_Time": get_readable_time(statinfo.st_atime),
                        "Creation_Time": get_readable_time(statinfo.st_ctime),
                        "Modified_Time": get_readable_time(statinfo.st_mtime),
                    }

                    # Convert to DataFrame
                    df_file_details = pd.DataFrame(
                        list(file_details_combined.items()),
                        columns=["Meta Tags", "Value"],
                    )
                    st.dataframe(df_file_details)

                    #track details
                    add_file_details(audio_file.name,audio_file.type,audio_file.size,datetime.now())


                   

    elif choice == "DocumentFiles":
        st.subheader("DoucumentFiles MetaData Extraction")
        # FIle Upload
        text_file = st.file_uploader("Upload File", type=["PDF"])
        if text_file is not None:
            dcol1, dcol2 = st.columns(2)

            with dcol1:
                with st.expander("File Stats"):
                    file_details = {
                        "FileName": text_file.name,
                        "FileSize": text_file.size,
                        "FileType": text_file.type,
                    }
                    st.write(file_details)

                    statinfo = os.stat(text_file.readable())

                    stats_details = {
                        "Accessed_Time": get_readable_time(statinfo.st_atime),
                        "Creation_Time": get_readable_time(statinfo.st_ctime),
                        "Modified_Time": get_readable_time(statinfo.st_mtime),
                    }
                    st.write(stats_details)

                    # Combine All Details
                    file_details_combined = {
                        "FileName": text_file.name,
                        "FileSize": text_file.size,
                        "FileType": text_file.type,
                        "Accessed_Time": get_readable_time(statinfo.st_atime),
                        "Creation_Time": get_readable_time(statinfo.st_ctime),
                        "Modified_Time": get_readable_time(statinfo.st_mtime),
                    }

                    # Convert to DataFrame
                    df_file_details = pd.DataFrame(
                        list(file_details_combined.items()),
                        columns=["Meta Tags", "Value"],
                    )
                    st.dataframe(df_file_details)
                    #track details
                    add_file_details(text_file.name,text_file.type,text_file.size,datetime.now())


                    
            with dcol2:
                with st.expander("Metadata"):
                    pass
                    # pdf_file = PdfReader(text_file)
                    # pdf_info = pdf_file.metadata()
                    # st.write(pdf_info)
                    # Convert to DataFrame
                    # df_file_details_with_pdf = pd.DataFrame(
                    #     list(pdf_info.items()), columns=["Meta Tags", "Value"]
                    # )

                    # st.dataframe(df_file_details_with_pdf)        

                    
                    
    elif choice == "DataAnalytics":
        st.subheader("DataAnalytics")
        all_uploaded_files = view_all_data()
        df = pd.DataFrame(
            all_uploaded_files,
            columns=["FileName", "FileType", "FileSize", "Upload_Time"],
        )

        # Monitor All Uploads
        with st.expander("Monitor"):
            st.success("View All Uploaded Files")
            st.dataframe(df)

        # Stats of Uploaded Files
        with st.expander("Distribution of FileTypes"):
            fig = plt.figure()
            sns.countplot(df["FileType"])
            st.pyplot(fig)

    

    else:
        st.subheader("About")
        st.write("Welcome to [Data Extraction App], your comprehensive data extraction solution designed to streamline information gathering effortlessly. We understand the pivotal role data plays in decision-making, and our app is crafted to empower users to extract, organize, and analyze data efficiently.Our team has meticulously developed this app with user-centricity in mind. Whether you're a researcher, business analyst, or enthusiast seeking to harness the power of data, [Data Extraction App] offers an intuitive interface coupled with powerful extraction algorithms to simplify the process.With [Data Extraction App], extract structured data from diverse sources—be it websites, documents, or spreadsheets—transforming raw information into actionable insights. Our goal is to make complex data extraction a seamless experience, allowing you to focus on analysis and decision-making.Join thousands of users who rely on [Data Extraction App] for its reliability, accuracy, and versatility in handling various data formats. As we evolve, we remain committed to innovation, ensuring our app stays at the forefront of data extraction technology Start your data journey with [Data Extraction App] today and unlock the potential within your data haystacks. Feel free to tailor this according to the specific features, unique selling points, or target audience of your app")

if __name__ == "__main__":
    main()