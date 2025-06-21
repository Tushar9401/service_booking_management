import frappe

def execute(filters=None):
    columns = [
        {"label": "Booking ID", "fieldname": "name", "fieldtype": "Link", "options": "Service Booking", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data", "width": 150},
        {"label": "Email", "fieldname": "customer_email", "fieldtype": "Data", "width": 200},
        {"label": "Service Type", "fieldname": "service_type", "fieldtype": "Data", "width": 150},
        {"label": "Preferred DateTime", "fieldname": "preferred_datetime", "fieldtype": "Datetime", "width": 180},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
    ]

    conditions = ""
    if filters.get("service_type"):
        conditions += f" AND service_type = %(service_type)s"
    if filters.get("status"):
        conditions += f" AND status = %(status)s"

    data = frappe.db.sql(f"""
        SELECT
            name, customer, customer_email, service_type,
            preferred_datetime, status, company
        FROM
            `tabService Booking`
        WHERE
            1=1 {conditions}
        ORDER BY
            modified DESC
    """, filters, as_dict=True)

    return columns, data
