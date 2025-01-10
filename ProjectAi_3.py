class ScheduleCSP:
    # کلاس مربوط به مسئله ارضای محدودیت برای زمان‌بندی کلاس‌ها
    def __init__(self, instructors, classrooms, time_slots):
        # مقداردهی اولیه با ورودی‌های مربوط به اساتید، کلاس‌ها و زمان‌بندی‌ها
        self.instructors = instructors
        self.classrooms = classrooms
        self.time_slots = time_slots
        self.variables = list(instructors.keys())  # متغیرها که همان دروس هستند
        self.domains = {
            course: [(room, time, instructor) for room in classrooms for time in time_slots for instructor in instructors[course]]
            for course in self.variables
        }  # دامنه مقادیر ممکن برای هر درس
        self.assignment = {}  # تخصیص فعلی مقادیر به متغیرها

    def is_consistent(self, course, value):
        # بررسی سازگاری مقدار تخصیص داده شده به یک متغیر با تخصیص‌های قبلی
        room, time, instructor = value
        for assigned_course, assigned_value in self.assignment.items():
            assigned_room, assigned_time, assigned_instructor = assigned_value

            # بررسی اینکه هیچ دو کلاسی همزمان در یک اتاق برگزار نشوند
            if time == assigned_time and room == assigned_room:
                return False

            # بررسی اینکه هیچ استادی همزمان دو درس را تدریس نکند
            if time == assigned_time and instructor == assigned_instructor:
                return False

        return True

    def select_unassigned_variable(self):
        # انتخاب متغیری که کمترین مقادیر ممکن (MRV) را دارد
        return min(
            (var for var in self.variables if var not in self.assignment),
            key=lambda var: len(self.domains[var])
        )

    def order_domain_values(self, var):
        # مرتب‌سازی مقادیر دامنه برای یک متغیر بر اساس کمترین تضاد (LCV)
        return sorted(self.domains[var], key=lambda value: self.conflicts(var, value))

    def conflicts(self, course, value):
        # محاسبه تعداد تضادهای ایجاد شده توسط یک مقدار
        room, time, instructor = value
        conflicts = 0
        for assigned_course, assigned_value in self.assignment.items():
            assigned_room, assigned_time, assigned_instructor = assigned_value
            if time == assigned_time and room == assigned_room:
                conflicts += 1
            if time == assigned_time and instructor == assigned_instructor:
                conflicts += 1
        return conflicts

    def forward_checking(self, course, value):
        # کاهش دامنه مقادیر ممکن با استفاده از تکنیک بررسی پیشرو
        room, time, instructor = value
        temp_domains = {var: list(domain) for var, domain in self.domains.items()}
        for var in self.variables:
            if var != course and var not in self.assignment:
                temp_domains[var] = [val for val in self.domains[var] if self.is_consistent(var, val)]
        return temp_domains

    def backtrack(self):
        # الگوریتم بازگشت به عقب برای حل مسئله
        if len(self.assignment) == len(self.variables):
            return self.assignment

        var = self.select_unassigned_variable()
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                self.assignment[var] = value
                original_domains = self.domains
                self.domains = self.forward_checking(var, value)

                result = self.backtrack()
                if result:
                    return result

                self.assignment.pop(var)
                self.domains = original_domains

        return None

    def solve(self):
        # شروع فرآیند حل مسئله
        return self.backtrack()

if __name__ == "__main__":
    # تعریف ورودی‌های مسئله
    instructors = {
        "AI": ["Dr.Moosavi", "Dr.Shahabi"],
        "Physics": ["Dr.Pouzesh"],
        "Chemistry": ["Dr.Fathi"],
        "Music": ["Dr.Shokoohi", "Dr.Mortazavi"],
        "Cinema": ["Dr.Mortazavi", "Dr.Khosravani"],
        "Algebra": ["Dr.Pourbagheri"]
    }

    classrooms = ["Room1", "Room2", "Room3"]
    time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00"]

    csp = ScheduleCSP(instructors, classrooms, time_slots)
    solution = csp.solve()

    # چاپ نتیجه زمان‌بندی در صورت یافتن
    if solution:
        print("Scheduling Solution:")
        for course, (room, time, instructor) in solution.items():
            print(f"{course}: {room} at {time} with {instructor}")
    else:
        print("No solution found.")
