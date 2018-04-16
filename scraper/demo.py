import xlrd
import json


def open_excel(filename):
    attendance_sheet = xlrd.open_workbook(
        filename, encoding_override="utf-8").sheet_by_index(0)
    return attendance_sheet


def parse_sheet(sheet):
    student_id_col_index = None
    week_one_attendance_col_index = None

    for i in range(sheet.ncols):
        if sheet.cell(0, i).value == 'stateid':
            student_id_col_index = i
            break

    for i in range(sheet.ncols):
        if sheet.cell(0, i).value == 'Wk1Total':
            week_one_attendance_col_index = i
            break

    return student_id_col_index + 2, week_one_attendance_col_index + 2


def find_student(sheet, student_id, student_id_col_index):
    for i in range(1, sheet.nrows):
        if int(sheet.cell(i, student_id_col_index).value) == student_id:
            return i


def get_student_attendance_totals(sheet, student_row_number,
                                  week_one_attendance_col_index):
    attendance_total = []
    for i in range(week_one_attendance_col_index - 2, sheet.ncols, 4):
        attendance_total.append(float(sheet.cell(student_row_number, i).value))
    return attendance_total


def to_json(attendance_totals):
    attendance_json = {}
    for i in range(len(attendance_totals)):
        attendance_json["{}".format(i + 1)] = attendance_totals[i]
    return json.dumps(attendance_json)


if __name__ == '__main__':
    sheet = open_excel('weekly_attendance.xlsx')
    id_attendance_tuple = parse_sheet(sheet)
    student_row_number = find_student(sheet, 13105, id_attendance_tuple[0])
    attendance_totals = get_student_attendance_totals(
        sheet, student_row_number, id_attendance_tuple[1])
    print(to_json(attendance_totals))
