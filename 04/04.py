"""
    { 'MM-DD': (#id, [(dormido, despierta)]) }
    {
        '11-01': (10, [05, 30], [25, 55]),
    }
"""

import re

JOURNAL_LINE = re.compile(r'\[\d+-(\d+)-(\d+) (\d+):(\d+)\] (.*)')
SHIFT_LINE = re.compile(r'Guard #(\d+) begins shift')

days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def parse_journal(file):
    journal = [x[:-1] for x in open(file).readlines()]
    journal.sort()
    events = [JOURNAL_LINE.match(line) for line in journal]
    for event in events:
        month, day = int(event[1]), int(event[2])
        hour, minute = int(event[3]), int(event[4])
        message = event[5]
        yield (month, day, hour, minute, message)

def get_shift_data(month, day, hour, minute, event):
    if hour == 23:
        day += 1
    if day > days_in_month[month-1]:
        day = 1
        month += 1
    group = SHIFT_LINE.match(event)
    return ('{:02d}-{:02d}'.format(month, day), int(group[1]))

def build_shifts_db(events):
    shifts_db = dict([get_shift_data(*event) for event in start_events])
    return {k: (v, [], []) for k, v in shifts_db.items()}

journal = list(parse_journal('input.txt'))
start_events = [ev for ev in journal if 'begins shift' in ev[4]]
shifts_db = build_shifts_db(start_events)

asleep = [ev for ev in journal if 'falls asleep' in ev[4]]
for sleep_event in asleep:
    key = '{:02d}-{:02d}'.format(sleep_event[0], sleep_event[1])
    shifts_db[key][1].append(sleep_event[3])

awakes = [ev for ev in journal if 'wakes up' in ev[4]]
for awake_event in awakes:
    key = '{:02d}-{:02d}'.format(awake_event[0], awake_event[1])
    shifts_db[key][2].append(awake_event[3])

sleeps_count = {}
for key, value in shifts_db.items():
    guard_id, sleeps, awakes = value
    minutes = sleeps_count.get(guard_id, 0)
    for i in range(len(sleeps)):
        minutes += (awakes[i] - sleeps[i])
    sleeps_count[guard_id] = minutes

total_minutes, winner_guard = 0, None
for guard, minutes in sleeps_count.items():
    if minutes > total_minutes:
        winner_guard = guard
        total_minutes = minutes

shifts_for_winner = [s for s in shifts_db.values() if s[0] == winner_guard]

minutes = [0 for _ in range(60)]
for shift in shifts_for_winner:
    _, sleeps, awakes = shift
    for i in range(len(sleeps)):
        sleep, awake = sleeps[i], awakes[i]
        for min in range(sleep, awake):
            minutes[min] += 1

winner_minute = minutes.index(max(minutes))


ex2_minutes = [{} for _ in range(60)]
for shift in shifts_db.values():
    guard, sleeps, awakes = shift
    for i in range(len(sleeps)):
        sleep, awake = sleeps[i], awakes[i]
        for min in range(sleep, awake):
            times = ex2_minutes[min].get(guard, 0)
            ex2_minutes[min][guard] = times + 1

maximum, maximum_guard, maximum_minute = 0, None, None
for i in range(60):
    minute = ex2_minutes[i]
    for guard, total in minute.items():
        if total > maximum:
            maximum = total
            maximum_guard = guard
            maximum_minute = i

print(maximum, maximum_guard, maximum_minute)
print(maximum_guard * maximum_minute)
