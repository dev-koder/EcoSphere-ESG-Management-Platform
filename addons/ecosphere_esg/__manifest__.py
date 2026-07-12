{
    "name": "EcoSphere: ESG Management",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "summary": "Environmental, Social, Governance & Gamification platform",
    "depends": ["base", "mail", "hr", "purchase", "hr_expense", "fleet",
                "base_automation", "product"],
    "data": [
        "security/ecosphere_esg_security.xml",
        "security/ir.model.access.csv",
        "views/esg_menus.xml",
        "views/esg_department_views.xml",
        "views/esg_category_views.xml",
    ],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "ecosphere_esg/static/src/scss/esg_dashboard.scss",
        ]
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
