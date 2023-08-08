{
    "name": "Estate",  # The name that will appear in the App list
    "version": "16.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "estate/web/static/src/css/estate_form.css",
        ],
    },
    "installable": True,
    "license": "LGPL-3",
}
