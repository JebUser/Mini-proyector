
login_style = """
    <style>
        [data-testid="stForm"] {
            background: #b3d7ff;
            padding: 30px;
            border-radius: 20px;
        }
        [data-testid="stForm"] h2 {
            text-align: center;
            color: black; /* Optional: Change header color */
        }
        h1 {
            color: #007BFF;
            text-align: center;
        }
        [data-testid="stForm"] input {
            width: 90% !important; /* Adjust width of inputs */
            border-radius: 10px !important; /* Rounded corners */
            padding: 10px !important; /* Inner padding */
            margin-bottom: 10px !important; /* Space between inputs */
        }
        [data-testid="stTitle"]{
            color: red; /* Change the header text color */
            text-align: center; /* Center the header text */
            margin-bottom: 20px; /* Add some space below the header */
        }
        .element-container:has(#button-after) {
            display: none;
        }
        .element-container:has(#button-after) + div button {
            background-color: #007BFF;
            width: 20%;
            border-radius: 8px;
            margin: 0;
        }
    </style>
    """