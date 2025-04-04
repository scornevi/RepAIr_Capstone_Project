
def custom_css():
    custom_css = """
    <style>
        .submit-button {
            background-color: #E69A8D !important; /* Coral Red */
            color: white !important;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .submit-button:hover {
            background-color: #D17F73 !important;
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
        }
        .feedback-buttons {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }
    </style>
    """
    return custom_css