import frappe
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_days, nowdate, get_datetime_str
from erpnext.hr.doctype.leave_application.leave_application import LeaveApplication


def notify_leave_approvers(doc):

	if doc.leave_approver:
		args = doc.as_dict()
		template = frappe.db.get_single_value('HR Settings', 'leave_approval_notification_template')
		if not template:
			frappe.msgprint(_("Please set default template for Leave Approval Notification in HR Settings."))
			return
		email_template = frappe.get_doc("Email Template", template)
		message = frappe.render_template(email_template.response, args)
		message_cc = frappe.db.get_value("Employee", filters={'user_id': doc.leave_approver}, fieldname=['leave_approver'])
		
		notify(
			# for post in messages
			message=message,
			message_to= doc.leave_approver,
			message_cc= message_cc,
			# for email
			subject= email_template.subject,
			follow_up= doc.follow_via_email,
		)

def notify(**kwargs):
	if  cint(kwargs['follow_up']):
		contact = kwargs['message_to']
		sender      	    = dict()
		sender['email']     = frappe.get_doc('User', frappe.session.user).email
		sender['full_name'] = frappe.utils.get_fullname(sender['email'])
		try:
			frappe.sendmail(
				recipients = contact,
				subject = kwargs['subject'],
				message = kwargs['message'],
				cc = kwargs['message_cc'],
			)
			frappe.msgprint(_("Email sent to - {0} ,cc - {1}").format(contact, kwargs['message_cc']))
		except frappe.OutgoingEmailError:
			pass


#Validate method to add a restriction on self approvals.
def validate(doc, method=None):
	if doc.employee  == frappe.session.user:
		frappe.throw("System does not allow you to approve the request")

def on_update(doc, method=None):
	LeaveApplication.on_update = customUpdate

def customUpdate(doc):
	if doc.status == "Open" and doc.docstatus < 1:
		# notify leave approver about creation
		notify_leave_approvers(doc)
