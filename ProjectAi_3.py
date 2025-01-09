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
