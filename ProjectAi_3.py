class ScheduleCSP:
    def __init__(self, instructors, classrooms, time_slots):
        self.instructors = instructors
        self.classrooms = classrooms
        self.time_slots = time_slots
        self.variables = list(instructors.keys())
        self.domains = {
            course: [(room, time, instructor) for room in classrooms for time in time_slots for instructor in instructors[course]]
            for course in self.variables
        }
        self.assignment = {}

    def is_consistent(self, course, value):
        room, time, instructor = value
        for assigned_course, assigned_value in self.assignment.items():
            assigned_room, assigned_time, assigned_instructor = assigned_value

            if time == assigned_time and room == assigned_room:
                return False

            if time == assigned_time and instructor == assigned_instructor:
                return False

        return True
 def select_unassigned_variable(self):
        return min(
            (var for var in self.variables if var not in self.assignment),
            key=lambda var: len(self.domains[var])
        )

    def order_domain_values(self, var):
        return sorted(self.domains[var], key=lambda value: self.conflicts(var, value))

    def conflicts(self, course, value):
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
        room, time, instructor = value
        temp_domains = {var: list(domain) for var, domain in self.domains.items()}
        for var in self.variables:
            if var != course and var not in self.assignment:
                temp_domains[var] = [val for val in self.domains[var] if self.is_consistent(var, val)]
        return temp_domains

    def backtrack(self):
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
        return self.backtrack()
