# Copyright (c) 2025, Tushar Thakkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json

class ServiceBooking(Document):
  def before_save(self):
    if self.status == "Approved":
        if not self.customer_email:
            frappe.throw("Customer Email is required when status is Approved.")

        previous_doc = self.get_doc_before_save()
        if previous_doc and previous_doc.status != "Approved":
            # Compose and send email
            message = f"""
                <p>Dear {self.customer},</p>
                <p>Your booking at <strong>{self.company}</strong>, with reference number <strong>{self.name}</strong>, 
                for the service <strong>{self.service_type}</strong> on <strong>{self.preferred_datetime}</strong> has been approved.</p>
                <p>Thank you for choosing our service!</p><br>
                <p>Regards,<br>{self.company}</p>
            """

            frappe.sendmail(
                recipients=[self.customer_email],
                subject="Booking Approved",
                message=message,
                reference_doctype=self.doctype,
                reference_name=self.name
            )

            frappe.msgprint("Confirmation email has been sent to the customer.")

           
            webhook_url = "https://webhook.site/827fbc1a-1b17-4bcb-ba94-d73be9a2c7a1"
            payload = {
                "booking_id": self.name,
                "customer": self.customer,
                "email": self.customer_email,
                "service_type": self.service_type,
                "preferred_datetime": self.preferred_datetime,
                "status": self.status,
                "company": self.company
            }
            

            try:
                response = requests.post(
                    webhook_url,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )
                

                if response.status_code == 200:
                    frappe.msgprint("Booking details sent to webhook successfully.")
                else:
                    frappe.log_error("Webhook Error", f"Failed with {response.status_code}: {response.text}")
            except Exception:
                frappe.log_error("Webhook Exception", frappe.get_traceback())

        if self.status == "Approved":
            # Prepare payload
            payload = {
                "booking_id": self.name,
                "customer": self.customer,
                "email": self.customer_email,
                "service_type": self.service_type,
                "preferred_datetime": self.preferred_datetime,
                "status": self.status,
                "company": self.company
            }

            try:
                # Replace with your actual webhook URL
                webhook_url = "https://webhook.site/your-dummy-url"  # or https://requestbin.io/
                
                response = requests.post(
                    webhook_url,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    frappe.msgprint("Booking details sent to webhook successfully.")
                else:
                    frappe.log_error(
                        title="Webhook Error",
                        message=f"Failed to send booking. Status: {response.status_code}, Response: {response.text}"
                    )
            except Exception as e:
                frappe.log_error("Webhook Exception", frappe.get_traceback())


