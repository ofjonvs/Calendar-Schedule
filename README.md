# Calendar-Schedule

Creates a schedule with 2d array, seperated by weeks and days. Uses hashmaps, regex, arrays, file input/output

Has recurring events (for a day in the week), deadline, single day event, and todo list options.

Displays a complete schedule with time ranges for each event. Displays total free time for each day, deadlines for each day, all upcoming deadlines and deadlines for each day

command line arguments: add 1 for std output. add 2 for redirection to a file

Format:

Reccurring: reccurring (monday, tuesday, wednesday, thursday, friday, saturday or sunday) "event name" (hour):(minute) (AM or PM) (hour):(minute) (AM or PM)

Single day event: event (month number)/(day) (hour):(minute) (AM or PM) (hour):(minute) (AM or PM)

Deadline: deadline (month number)/(day) "deadline name"

To do: todo "name" (time in minutes)
