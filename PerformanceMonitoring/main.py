import psutil

from PerformanceMonitoring.process_data import ProcessData


def main():
    process_dict = {}

    while True:

        current_iteration_dict = {}

        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                process_name = proc.name()
                process_id = proc.pid
                process_cpu = proc.cpu_percent()
                process_memory = proc.memory_percent()
                process_score = proc.nice()

                temp = ProcessData(process_name, process_cpu, process_memory, process_score)

                current_iteration_dict[process_id] = temp

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not bool(process_dict):
            process_dict = current_iteration_dict
            continue

        for key in process_dict:
            if key not in current_iteration_dict:
                print("Process removed: ", process_dict[key].process_id, ":::", process_dict[key].process_cpu, ":::",
                      process_dict[key].process_memory, ":::", process_dict[key].process_priority, ":::")

        for key in current_iteration_dict:
            if key not in process_dict:
                print("Process added: ", process_dict[key].process_id, ":::", process_dict[key].process_cpu, ":::",
                      process_dict[key].process_memory, ":::", process_dict[key].process_priority, ":::")

        process_dict = current_iteration_dict


if __name__ == '__main__':
    main()
