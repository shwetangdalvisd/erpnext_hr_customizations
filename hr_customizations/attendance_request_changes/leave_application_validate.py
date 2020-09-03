import frappe
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_days, nowdate, get_datetime_str,today
from erpnext.hr.doctype.leave_application.leave_application import ( LeaveApplication, get_leave_balance_on, 

    get_number_of_leave_days, is_lwp) 

def validate(doc, method=None):
	'''This Validate method to restrict a user to apply for leaves upto two backdated days'''

	number_of_days=date_diff(today(),doc.from_date)
	if (number_of_days > 2 and doc.status not in ['Approved','Rejected', 'Cancelled']):
		frappe.throw("Leave Applications only upto 2 backdated days are allowed.")

def fix_balance_leave(doc):
	if doc.from_date and doc.to_date:
			doc.total_leave_days = get_number_of_leave_days(doc.employee, doc.leave_type,
				doc.from_date, doc.to_date, doc.half_day, doc.half_day_date)

			if doc.total_leave_days <= 0:
				frappe.throw(_("The day(s) on which you are applying for leave are holidays. You need not apply for leave."))


			if not is_lwp(doc.leave_type):
				doc.leave_balance = get_leave_balance_on(doc.employee, doc.leave_type, doc.from_date, doc.to_date,
					consider_all_leaves_in_the_allocation_period=True)
				if doc.status != "Rejected" and (doc.leave_balance < doc.total_leave_days or not doc.leave_balance):
					if frappe.db.get_value("Leave Type", doc.leave_type, "allow_negative"):
						frappe.msgprint(_("Note: There is not enough leave balance for Leave Type {0}")
							.format(doc.leave_type))
					else:
						frappe.throw(_("There is not enough leave balance for Leave Type {0}")
							.format(doc.leave_type))

def abc(doc, method=None):
	LeaveApplication.validate_balance_leaves = fix_balance_leave
