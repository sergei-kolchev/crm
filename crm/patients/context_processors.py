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
            {
                "url": "patients:patients",
                "name": "Журналы",
                "image_url": "images/noun-documentation-2912476.png",
            },
            {
                "url": "patients:patients",
                "name": "Отчеты",
                "image_url": "images/noun-statistics-1186479.png",
            },
            {
                "url": "patients:patients",
                "name": "Лекарственные препараты",
                "image_url": "images/noun-medical-1730851.png",
            },
            {
                "url": "patients:patients",
                "name": "Настройки",
                "image_url": "images/noun-settings-1084769.png",
            },
            {
                "url": "patients:patients",
                "name": "Ai",
                "image_url": "images/noun-ai-2956643.png",
            },
        ]
    }
