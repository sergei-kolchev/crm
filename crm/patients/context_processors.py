def get_patients_context(request):
    return {
        "main_menu": [
            {
                "url": "patients:patients",
                "name": "Картотека пациентов",
                "image_url": "images/noun-hospital-1891627.png",
            },
            {
                "url": "hospitalizations:current",
                "name": "Находящиеся на лечении",
                "image_url": "images/noun-medical-1730855.png",
            },
        ]
    }
