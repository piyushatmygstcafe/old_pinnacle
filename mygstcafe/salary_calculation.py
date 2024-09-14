from datetime import datetime, time

def calculate_monthly_salary(employee_data, total_working_days):
    
    for emp_id, data in employee_data.items():
        basic_salary = data.get("basic_salary", 0)
        attendance_records = data.get("attendance_records", [])
        
        per_day_salary = round(basic_salary / total_working_days, 2)
        
        # Initialize counters
        total_salary = 0
        total_late_deductions = 0
        full_days = 0
        half_days = 0
        quarter_days = 0
        three_four_quarter_days = 0
        total_absents = 0
        lates = 0
        overtime_salry = 0
        actual_working_days = 0
        
        for record in attendance_records:
            attendance_date = record["attendance_date"]
            in_time = record["in_time"]
            out_time = record["out_time"]
            
            ideal_check_in_time = datetime.combine(attendance_date,time(10,0))
            ideal_check_out_time = datetime.combine(attendance_date,time(19,0))
            overtime_threshold = datetime.combine(attendance_date,time(19,30))
            
            if in_time is not None and out_time is not None:
                temp_in = in_time.time()
                check_in = datetime.combine(attendance_date,temp_in)
                temp_out = out_time.time()
                check_out = datetime.combine(attendance_date,temp_out)
                total_working_time = check_out - check_in
                total_working_hours = total_working_time.total_seconds() / 3600 
                
                if 7.875 <= total_working_hours <= 10.125:
                    overtime_salry = 0
                    if total_working_hours > 9 and check_out > overtime_threshold:
                        extra_time = check_out - ideal_check_out_time
                        overtime = extra_time.total_seconds() / 60
                        min_overtime_salary = per_day_salary / 540
                        overtime_salry = overtime * min_overtime_salary    
                    full_days += 1
                    actual_working_days += 1
                    total_salary += per_day_salary + overtime_salry
                
                elif 5.625 <= total_working_hours < 7.875:
                    quarter_days += 1
                    actual_working_days += 1
                    total_salary += 0.75 * per_day_salary
                
                elif 3.375 <= total_working_hours < 5.625:
                    half_days += 1
                    actual_working_days += 1
                    total_salary += 0.5 * per_day_salary
                
                elif 1.125 <= total_working_hours < 3.375:
                    three_four_quarter_days += 1
                    actual_working_days += 1
                    total_salary += 0.25 * per_day_salary
                
                else:
                    overtime_salry = 0
                    if total_working_hours > 10.125 and check_out > overtime_threshold:
                        extra_time = check_out - ideal_check_out_time
                        overtime = extra_time.total_seconds() / 60
                        min_overtime_salary = per_day_salary / 540
                        overtime_salry = overtime * min_overtime_salary 
                
                if check_in > ideal_check_in_time:
                    lates += 1
                    late_deduction = 0.10 * per_day_salary
                    total_late_deductions += late_deduction
            else:
                total_absents += 1
                total_salary += 0
        
        total_salary -= total_late_deductions
        
        data["salary_information"] = {
            "basic_salary": basic_salary,
            "per_day_salary": per_day_salary,
            "standard_working_days": total_working_days,
            "actual_working_days": actual_working_days,
            "full_days": full_days,
            "half_days": half_days,
            "quarter_days": quarter_days,
            "three_four_quarter_days": three_four_quarter_days,
            "total_salary": round(total_salary,2),
            "total_late_deductions": total_late_deductions,
            "absent": total_absents,
            "lates": lates,
            "overtime": round(overtime_salry,2),
        }
    
    return employee_data
