import psutil
from PerformanceMonitoring.process_data import ProcessData


def main():

    # Main dict to keep track of our processes.
    process_dict = {}

    # Loop to keep the GUI and the collection of processes continuing.
    while True:

        # Grabs the CURRENT iteration of processes that will be compared to process_dict
        current_iteration_dict = {}

        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name, pid, cpu percent, memory percent, and priority.
                process_name = proc.name()
                process_id = proc.pid
                process_cpu = proc.cpu_percent()
                process_memory = proc.memory_percent()
                process_score = proc.nice()

                # Store into temp object to be added to dictionary of current iteration.
                temp = ProcessData(process_name, process_cpu, process_memory, process_score)

                current_iteration_dict[process_id] = temp

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Since we now have all the processes from the LAST iteration and all the processes from the current
        # iteration, we can now compare their differences to analyze what has changed.

        # If this is our first iteration (AKA process_dict is empty), give it data from current and dont do
        # comparisons
        if not bool(process_dict):
            process_dict = current_iteration_dict
            continue

        for key in process_dict:
            # If the key is in process_dict (last run) and not in current_iteration_dict, we know that the process
            # has dropped off.
            if key not in current_iteration_dict:
                print("Process removed: ", process_dict[key].process_id, ":::", process_dict[key].process_cpu, ":::",
                      process_dict[key].process_memory, ":::", process_dict[key].process_priority)
            else:
                # Since the key exists in both dicts, we can do comparisons of their resources used
                if process_dict[key].process_cpu > current_iteration_dict[key].process_cpu:
                    print("Process ", key, " with name ", process_dict[key].process_id, "decreased its CPU utilization"
                                                                                        "by ",
                          process_dict[key].process_cpu - current_iteration_dict[key].process_cpu, "percent.")

        for key in current_iteration_dict:
            # If the key is in current_iteration_dict (current run) and not in the last run dict then that means the
            # process has been added
            if key not in process_dict:
                print("Process added: ", current_iteration_dict[key].process_id, ":::",
                      current_iteration_dict[key].process_cpu, ":::", current_iteration_dict[key].process_memory, ":::",
                      current_iteration_dict[key].process_priority)

        process_dict = current_iteration_dict


if __name__ == '__main__':
    main()
