import frappe, erpnext
from frappe import _
from frappe.utils import  getdate
from erpnext.hr.doctype.attendance_request.attendance_request import AttendanceRequest


def validate(doc, method=None):
	AttendanceRequest.validate = customValidation


def customValidation(doc):
	'''
		This validation method was written in order to 
		eliminate the restriction of requesting attendance of future dates.
		The emphasis is to modify the validate_dates method in default validate method.
	'''
	date_of_joining, relieving_date = frappe.db.get_value("Employee", doc.employee, ["date_of_joining", "relieving_date"])
	if getdate(doc.from_date) > getdate(doc.to_date):
		frappe.throw(_("To date can not be less than from date"))

	elif date_of_joining and getdate(doc.from_date) < getdate(date_of_joining):
		frappe.throw(_("From date can not be less than employee's joining date"))

	elif relieving_date and getdate(doc.to_date) > getdate(relieving_date):
		frappe.throw(_("To date can not greater than employee's relieving date"))

	if doc.half_day:
		if not getdate(doc.from_date)<=getdate(doc.half_day_date)<=getdate(doc.to_date):
			frappe.throw(_("Half day date should be in between from date and to date"))


