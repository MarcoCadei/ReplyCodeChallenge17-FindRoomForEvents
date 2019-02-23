import sys
from collections import namedtuple


Event = namedtuple("Event", ["name", "start", "end", "duration", "participants"])
Room = namedtuple("Room", ["name", "capacity"])
events = []
rooms = []
duration_events = []  # Duration of events in each room
open_time = []  # Opening time time of each room
close_time = []  # Closing time time of each room
E = 0
R = 0
max_capacity = 0
scores_room = [0] * R


def read(file):
    global E, R, events, rooms, max_capacity, duration_events, open_time, close_time
    E, R = (int(x) for x in file.readline().split())
    duration_events = [0] * R
    open_time = [0] * R
    close_time = [0] * R

    for _ in range(E):
        n, s, f, p = file.readline().split()
        s = int(s)
        f = int(f)
        p = int(p)
        events.append(Event(n, s, f, f-s, p))

    max_capacity = 0
    for _ in range(R):
        n, c = file.readline().split()
        c = int(c)
        rooms.append(Room(n, c))
        max_capacity = c if c > max_capacity else max_capacity


def check_constraints(solution, event, room):
    if rooms[room].capacity == 0:
        return False
    if events[event].participants > rooms[room].capacity:
        return False

    for i in range(E):
        if solution[i] == room and events[i].name != events[event].name:
            if not (events[event].start >= events[i].end > events[i].start or
                    events[event].end <= events[i].start < events[i].end):
                return False

    return True


def write(solution, file_name):
    file = open(file_name, "w")
    text = []
    for i in range(R):
        events_room = []
        for j in range(E):
            if solution[j] == i:
                events_room.append(events[j])

        events_room.sort(key=lambda x: x.start)
        events_name = [x.name for x in events_room]
        text.append(rooms[i].name + ":" + " ".join(events_name))

    file.write("\n".join(text))


def main():
    global events, scores_room, duration_events, open_time, close_time
    read(open(sys.argv[1]))
    # An array of len E, such that solution[E] = index of room allocated, -1 if not allocated
    # solution = [random.randint(0, R-1) for _ in range(E)]
    solution = [-1] * E
    # Sort the events for "importance"
    events.sort(key=lambda x: x.participants * x.duration, reverse=True)

    score = 0
    for i, event in enumerate(events):
        best_room = - 1
        for j in range(R):
            solution[i] = j
            if check_constraints(solution, i, j):
                # New score if i were to punt event in room j
                actual_score = event.participants / rooms[j].capacity * event.duration
                t3 = duration_events[j] + event.duration
                t1 = event.start if event.start < open_time[j] or open_time[j] == 0 else open_time[j]
                t2 = event.end if event.end > close_time[j] or close_time[j] == 0 else close_time[j]
                best_new_score = score + actual_score - rooms[j].capacity / max_capacity * (t2 - t1 - t3)
                if best_new_score > score:
                    best_room = j
                    score = best_new_score
                    duration_events[j] = t3
                    open_time[j] = t1
                    close_time[j] = t2

        solution[i] = best_room if best_room != -1 else -1

    write(solution, sys.argv[1].split(".")[0]+".out")


if __name__ == "__main__":
    main()
