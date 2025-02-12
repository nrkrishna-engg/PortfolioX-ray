def apply_custom_style():
    return """
    <style>
    .stInfo {
        background-color: #f8f9fa !important;
        border: 2px solid #6c757d !important;
    }
    .stSuccess {
        background-color: #f8f9fa !important;
        border: 2px solid #28a745 !important;
    }
    /* Checkbox styling */
    .stCheckbox {
        position: relative;
        padding: 15px !important;
    }
    .stCheckbox label {
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        color: #0f1010 !important;
    }
    .stCheckbox input[type="checkbox"] {
        transform: scale(1.5);
        margin-right: 10px !important;
    }
    </style>
    """ 