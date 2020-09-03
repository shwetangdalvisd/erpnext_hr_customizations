import frappe
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, \
	comma_or, get_fullname, add_days, nowdate, get_datetime_str, today
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry as base_leave_ledger


def create_ledger_entry_for_intermediate_allocation_expiry(la, expiry_date, submit, lwp):
		''' splits leave application into two ledger entries to consider expiry of allocation '''
		args = dict(
			from_date=la.from_date,
			to_date=expiry_date,
			leaves=(date_diff(expiry_date, la.from_date) + 1) * -1,
			is_lwp=lwp,
			holiday_list=get_holiday_list_for_employee(la.employee),

		)
		base_leave_ledger(la, args, submit)

		if getdate(expiry_date) != getdate(la.to_date):
			start_date = add_days(expiry_date, 1)
			args.update(dict(
				from_date=start_date,
				to_date=la.to_date,
				leaves=date_diff(la.to_date, expiry_date) * -1
			))
			base_leave_ledger(la, args, submit)

def get_allocation_expiry(employee, leave_type, to_date, from_date):
	''' Returns expiry of carry forward allocation in leave ledger entry '''
	expiry =  frappe.get_all("Leave Ledger Entry",
		filters={
			'employee': employee,
			'leave_type': leave_type,
			'is_carry_forward': 1,
			'transaction_type': 'Leave Allocation',
			'to_date': ['between', (from_date, to_date)]
		},fields=['to_date'])
	return expiry[0]['to_date'] if expiry else None



def create_leave_ledger_entry(la, submit=True):
		if la.status != 'Approved' and submit:
			return

		expiry_date = get_allocation_expiry(la.employee, la.leave_type,
			la.to_date, la.from_date)

		lwp = frappe.db.get_value("Leave Type", la.leave_type, "is_lwp")

		if expiry_date:
			create_ledger_entry_for_intermediate_allocation_expiry(expiry_date, submit, lwp)
		else:
			args = dict(
				leaves=la.total_leave_days * -1,
				from_date=la.from_date,
				to_date=la.to_date,
				is_lwp=lwp,
				holiday_list=get_holiday_list_for_employee(la.employee)
			)
			base_leave_ledger(la, args, submit)

def cancel_leave(name):
	la = frappe.get_doc('Leave Application', name)

	create_leave_ledger_entry(la, submit=False)
	la.status = "Cancelled"
	la.docstatus = 1
	la.save()
	la.docstatus = 2
	la.save()
	return



def auto_reject_leaves():
	leave_applications = frappe.db.get_list('Leave Application',
		filters = {
			'status': 'Open',
			'from_date': ['<', today()] ,
		},
		fields = ['name'])
	for x in leave_applications:
		cancel_leave(x['name'])