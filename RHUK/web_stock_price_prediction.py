import streamlit as st
import pandas as pd
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
import yfinance as yf
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime



st.set_page_config(
    page_title="Stock Market Price Prediction",
    layout="wide"
)


def set_bg(image_url):

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
            linear-gradient(
                rgba(0,0,0,0.35),
                rgba(0,0,0,0.35)
            ),
            url("{image_url}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        header {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        /* SIDEBAR */

        section[data-testid="stSidebar"] {{
            background: rgba(0,0,0,0.92);
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}

        .stSelectbox label {{
            color: white !important;
            font-weight: bold;
            font-size: 20px !important;
        }}

        .stSelectbox div[data-baseweb="select"] {{
            background-color: white !important;
            border-radius: 10px;
            border: 2px solid #144272;
        }}

        .stSelectbox div[data-baseweb="select"] * {{
            color: black !important;
            font-weight: bold !important;
        }}

        div[data-baseweb="popover"] * {{
            color: black !important;
            font-weight: bold !important;
        }}

        /* WHITE TEXT */

        h1, h2, h3, h4, h5, h6,
        p, span, div {{
            color: white !important;
        }}

        /* INPUT LABELS */

        label {{
            color: white !important;
            font-size: 15px !important;
            font-weight: 700 !important;
        }}

        /* INPUT BOX */

        .stTextInput > div > div > input {{

            height: 50px;

            border-radius: 12px;

            border: 1px solid #999;

            background: rgba(255,255,255,0.96);

            color: black !important;

            padding-left: 14px;

            font-size: 16px;
        }}

        /* BUTTON */

        .stButton button {{

            width: 100%;

            height: 50px;

            border-radius: 12px;

            border: none;

            background: #144272;

            color: white;

            font-size: 18px;

            font-weight: bold;
        }}

        .stButton button:hover {{

            background: #205295;

            color: white;
        }}

        .stCheckbox label {{
            color: white !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT,
    password TEXT
)
""")

conn.commit()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""


if not st.session_state.logged_in:

    set_bg(
        "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a"
    )



menu = st.sidebar.selectbox(
    "Menu",
    ["Login", "Signup"]
)

if menu == "Login" and not st.session_state.logged_in:

    left, center, right = st.columns([1.5,1,1.5])

    with center:

        # LOGO

        col1, col2, col3 = st.columns([1,1,1])

        with col2:

            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=140
            )

    

        st.markdown(
            """
            <div style="
                background:#144272;
                padding:14px;
                border-radius:14px;
                margin-top:10px;
                margin-bottom:25px;
                text-align:center;
            ">
                <h2 style="
                    color:white;
                    margin:0;
                    font-size:30px;
                    font-weight:bold;
                ">
                    LOGIN
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        email = st.text_input(
            "Email Address"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        remember = st.checkbox(
            "Remember Me"
        )

        if st.button("LOGIN"):

            cursor.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, password)
            )

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.user = email

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Email or Password"
                )



if menu == "Signup" and not st.session_state.logged_in:

    left, center, right = st.columns([1.5,1,1.5])

    with center:

        # LOGO

        col1, col2, col3 = st.columns([1,1,1])

        with col2:

            st.image(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
                width=140
            )

        

        st.markdown(
            """
            <div style="
                background:#144272;
                padding:14px;
                border-radius:14px;
                margin-top:10px;
                margin-bottom:25px;
                text-align:center;
            ">
                <h2 style="
                    color:white;
                    margin:0;
                    font-size:26px;
                    font-weight:bold;
                ">
                    CREATE ACCOUNT
                </h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        email = st.text_input(
            "Email Address"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("CREATE ACCOUNT"):

            if password != confirm_password:

                st.error(
                    "Passwords do not match"
                )

            else:

                cursor.execute(
                    "SELECT * FROM users WHERE email=?",
                    (email,)
                )

                user = cursor.fetchone()

                if user:

                    st.error(
                        "User already exists"
                    )

                else:

                    cursor.execute(
                        "INSERT INTO users VALUES (?, ?)",
                        (email, password)
                    )

                    conn.commit()

                    st.success(
                        "Account Created Successfully"
                    )

                    st.info(
                        "Now Login"
                    )



if st.session_state.logged_in:

    set_bg(
        "https://images.unsplash.com/photo-1642790106117-e829e14a795f"
    )

    st.sidebar.success(
        f"Logged in as {st.session_state.user}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user = ""

        st.rerun()

    
    

    st.title(
        "📊 Stock Market Price Prediction"
    )

    

    col1, col2, col3 = st.columns([1,2,5])

    with col2:

        stock = st.text_input(
            "Enter Stock Symbol",
            "GOOG"
        )

    

    end = datetime.now()

    start = datetime(
        end.year - 20,
        end.month,
        end.day
    )


    google_data = yf.download(
        stock,
        start,
        end
    )

    

    model = load_model(
        "Lastest_stock_price_model.keras"
    )

    

    st.subheader(
        "Stock Data"
    )

    st.write(
        google_data
    )

    

    google_data['MA_for_250_days'] = (
        google_data['Close']
        .rolling(250)
        .mean()
    )

    google_data['MA_for_200_days'] = (
        google_data['Close']
        .rolling(200)
        .mean()
    )

    google_data['MA_for_100_days'] = (
        google_data['Close']
        .rolling(100)
        .mean()
    )



    def plot_graph(
        figsize,
        values,
        full_data,
        extra_data=0,
        extra_dataset=None
    ):

        fig = plt.figure(
            figsize=figsize
        )

        plt.plot(
            values,
            'orange'
        )

        plt.plot(
            full_data.Close,
            'blue'
        )

        if extra_data:

            plt.plot(
                extra_dataset
            )

        plt.legend()

        return fig

   

    st.subheader(
        'Close Price and MA250'
    )

    st.pyplot(
        plot_graph(
            (15, 6),
            google_data['MA_for_250_days'],
            google_data
        )
    )

  

    st.subheader(
        'Close Price and MA200'
    )

    st.pyplot(
        plot_graph(
            (15, 6),
            google_data['MA_for_200_days'],
            google_data
        )
    )


    st.subheader(
        'Close Price and MA100'
    )

    st.pyplot(
        plot_graph(
            (15, 6),
            google_data['MA_for_100_days'],
            google_data
        )
    )

   

    st.subheader(
        'Close Price with MA100 & MA250'
    )

    st.pyplot(
        plot_graph(
            (15, 6),
            google_data['MA_for_100_days'],
            google_data,
            1,
            google_data['MA_for_250_days']
        )
    )

  

    splitting_len = int(
        len(google_data) * 0.7
    )

    x_test = google_data[['Close']].iloc[
        splitting_len:
    ]



    scaler = MinMaxScaler(
        feature_range=(0, 1)
    )

    scaled_data = scaler.fit_transform(
        x_test[['Close']]
    )

    x_data = []
    y_data = []

    for i in range(
        100,
        len(scaled_data)
    ):

        x_data.append(
            scaled_data[i-100:i]
        )

        y_data.append(
            scaled_data[i]
        )

    x_data = np.array(x_data)

    y_data = np.array(y_data)

 

    predictions = model.predict(
        x_data
    )

    inv_pre = scaler.inverse_transform(
        predictions
    )

    inv_y_test = scaler.inverse_transform(
        y_data
    )

    ploting_data = pd.DataFrame(
        {
            'Original Test Data':
                inv_y_test.reshape(-1),

            'Predicted Data':
                inv_pre.reshape(-1)
        },
        index=google_data.index[
            splitting_len + 100:
        ]
    )

    st.subheader(
        "Original vs Predicted Values"
    )

    st.write(
        ploting_data
    )


    st.subheader(
        'Original vs Predicted Close Price'
    )

    fig = plt.figure(
        figsize=(15, 6)
    )

    plt.plot(
        pd.concat(
            [
                google_data.Close[
                    :splitting_len + 100
                ],
                ploting_data
            ],
            axis=0
        )
    )

    plt.legend([
        "Data Not Used",
        "Original Test Data",
        "Predicted Data"
    ])

    st.pyplot(fig)

    st.success(
        "Stock Prediction Loaded Successfully"
    )