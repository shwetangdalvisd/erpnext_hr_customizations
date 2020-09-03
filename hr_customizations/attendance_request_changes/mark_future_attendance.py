import frappe, erpnext
from frappe import _
from frappe.utils import  getdate
from erpnext.hr.doctype.attendance.attendance import Attendance


def validate(doc, method=None):
	Attendance.validate_attendance_date = customValidation


def customValidation(doc):
	'''
	   This method is to override validate_attendance_date so we can mark future attendance.
	'''
	date_of_joining = frappe.db.get_value("Employee", doc.employee, "date_of_joining")

	# leaves can be marked for future dates
	if date_of_joining and getdate(doc.attendance_date) < getdate(date_of_joining):
		frappe.throw(_("Attendance date can not be less than employee's joining date"))

