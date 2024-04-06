import os
import time


def generate_subtitle_file(timepoints, mark_array, filename="subtitle.txt"):
    count = 0
    current = 0
    dir_path = os.environ["BASE_DIR_PATH"]
    filepath = f"{dir_path}/{filename}"
    for i in range(len(timepoints)):
        count += 1
        current += 1
        with open(filepath, "a", encoding="utf-8") as out:
            out.write(mark_array[int(timepoints[i].mark_name)] + " ")
        if i != len(timepoints) - 1:
            total_time = timepoints[i + 1].time_seconds
            time.sleep(total_time - timepoints[i].time_seconds)
        if current == 25:
            open(filepath, "w", encoding="utf-8").close()
            current = 0
            count = 0
        elif count % 7 == 0:
            with open(filepath, "a", encoding="utf-8") as out:
                out.write("\n")
    time.sleep(2)
    open(filepath, "w").close()
