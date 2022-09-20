import psutil

def main():
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            processCPU = proc.cpu_percent()
            print(processName, ' ::: ', processID, ' ::: ', processCPU)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == '__main__':
    main()
