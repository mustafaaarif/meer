from django import template

register = template.Library()

@register.filter
def get_employee_attendance(attendance_data, employee_id):
    return attendance_data.filter(employee=employee_id).first()
