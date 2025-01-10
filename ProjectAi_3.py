if __name__ == "__main__":
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

    if solution:
        print("Scheduling Solution:")
        for course, (room, time, instructor) in solution.items():
            print(f"{course}: {room} at {time} with {instructor}")
    else:
        print("No solution found.")
