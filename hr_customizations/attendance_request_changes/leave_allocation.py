from __future__ import unicode_literals
import frappe, erpnext
from frappe import _
from frappe.utils import formatdate, format_datetime, getdate, get_datetime, nowdate, flt, cstr, add_days, today
from frappe.model.document import Document
from frappe.desk.form import assign_to
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.hr.utils import get_employee_leave_policy, check_frequency_hit, create_additional_leave_ledger_entry



def allocate_earned_leaves(*args, **kwargs):
	'''Allocate earned leaves to Employees'''
	e_leave_types = frappe.get_all("Leave Type",
		fields=["name", "max_leaves_allowed", "earned_leave_frequency", "rounding"],
		filters={'is_earned_leave' : 1})

	today = getdate()
	divide_by_frequency = {"Yearly": 1, "Half-Yearly": 6, "Quarterly": 4, "Monthly": 12}

	for e_leave_type in e_leave_types:
		print("lt")
		# import pdb;pdb.set_trace()
		leave_allocations = frappe.db.sql("""select name, employee, from_date, to_date from `tabLeave Allocation` where %s
			between from_date and to_date and docstatus=1 and leave_type=%s""", (today, e_leave_type.name), as_dict=1)

		for allocation in leave_allocations:
			print("la")
			# import pdb;pdb.set_trace()
			leave_policy = get_employee_leave_policy(allocation.employee)
			if not leave_policy:
				continue
			if not e_leave_type.earned_leave_frequency == "Monthly":
				if not check_frequency_hit(allocation.from_date, today, e_leave_type.earned_leave_frequency):
					continue
			annual_allocation = frappe.db.get_value("Leave Policy Detail", filters={
				'parent': leave_policy.name,
				'leave_type': e_leave_type.name
			}, fieldname=['annual_allocation'])
			if annual_allocation:
				print("aa")
				# import pdb;pdb.set_trace()
				earned_leaves = flt(annual_allocation) / divide_by_frequency[e_leave_type.earned_leave_frequency]
				if e_leave_type.rounding == "0.5":
					earned_leaves = round(earned_leaves * 2) / 2
				elif e_leave_type.rounding == "1":
					earned_leaves = round(earned_leaves)
				else:
					earned_leaves = earned_leaves

				l_allocation = frappe.get_doc('Leave Allocation', allocation.name)
				if l_allocation.total_leaves_allocated == 0:
					new_allocation = flt(l_allocation.total_leaves_allocated) + flt(earned_leaves)
					if new_allocation > e_leave_type.max_leaves_allowed and e_leave_type.max_leaves_allowed > 0:
						new_allocation = e_leave_type.max_leaves_allowed
					if new_allocation == l_allocation.total_leaves_allocated:
						continue
					l_allocation.db_set("total_leaves_allocated", new_allocation, update_modified=False)
					create_additional_leave_ledger_entry(l_allocation, earned_leaves, today)


def allocate_earned_leaves_cron(*args, **kwargs):
	'''Allocate earned leaves to Employees'''
	e_leave_types = frappe.get_all("Leave Type",
		fields=["name", "max_leaves_allowed", "earned_leave_frequency", "rounding"],
		filters={'is_earned_leave' : 1})

	today = getdate()
	divide_by_frequency = {"Yearly": 1, "Half-Yearly": 6, "Quarterly": 4, "Monthly": 12}

	for e_leave_type in e_leave_types:
		print("lt")
		# import pdb;pdb.set_trace()
		leave_allocations = frappe.db.sql("""select name, employee, from_date, to_date from `tabLeave Allocation` where %s
			between from_date and to_date and docstatus=1 and leave_type=%s""", (today, e_leave_type.name), as_dict=1)

		for allocation in leave_allocations:
			print("la")
			# import pdb;pdb.set_trace()
			leave_policy = get_employee_leave_policy(allocation.employee)
			if not leave_policy:
				continue
			if not e_leave_type.earned_leave_frequency == "Monthly":
				if not check_frequency_hit(allocation.from_date, today, e_leave_type.earned_leave_frequency):
					continue
			annual_allocation = frappe.db.get_value("Leave Policy Detail", filters={
				'parent': leave_policy.name,
				'leave_type': e_leave_type.name
			}, fieldname=['annual_allocation'])
			if annual_allocation:
				print("aa")
				# import pdb;pdb.set_trace()
				earned_leaves = flt(annual_allocation) / divide_by_frequency[e_leave_type.earned_leave_frequency]
				if e_leave_type.rounding == "0.5":
					earned_leaves = round(earned_leaves * 2) / 2
				elif e_leave_type.rounding == "1":
					earned_leaves = round(earned_leaves)
				else:
					earned_leaves = earned_leaves

				l_allocation = frappe.get_doc('Leave Allocation', allocation.name)
				new_allocation = flt(l_allocation.total_leaves_allocated) + flt(earned_leaves)
				if new_allocation > e_leave_type.max_leaves_allowed and e_leave_type.max_leaves_allowed > 0:
					new_allocation = e_leave_type.max_leaves_allowed
				if new_allocation == l_allocation.total_leaves_allocated:
					continue
				l_allocation.db_set("total_leaves_allocated", new_allocation, update_modified=False)
				create_additional_leave_ledger_entry(l_allocation, earned_leaves, today)