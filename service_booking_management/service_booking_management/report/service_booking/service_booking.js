frappe.query_reports["Service Booking"] = {
    "filters": [
        {
            "fieldname": "service_type",
            "label": "Service Type",
            "fieldtype": "Select",
            "options": ["", "Therapy", "Spa", "Others"],  // customize these
            "default": ""
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": ["", "Requested", "Approved", "Completed"],
            "default": ""
        }
    ]
};
