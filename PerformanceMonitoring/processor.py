import psutil
import GPUtil
import helpers as hlp
from PerformanceMonitoring.process_data import ProcessData


class Processor:
    current_iteration_cpu = {}
    last_iteration_cpu = {}
    gpu_utilization = None

    def process(self):

        Processor.get_processes(self)

        if not bool(self.last_iteration_cpu):
            self.last_iteration_cpu = self.current_iteration_cpu
            return

        if len(GPUtil.getGPUs()) != 0:
            Processor.check_gpu_utilization(self)

        Processor.compare_current_iteration_to_last(self)
        Processor.compare_last_iteration_to_current(self)

        self.last_iteration_cpu = self.current_iteration_cpu

    def get_processes(self):

        self.current_iteration_cpu = {}

        # Iterate over all running process
        for proc in psutil.process_iter():
            try:
                # Get process name, pid, cpu percent, memory percent, and priority.
                process_id = proc.pid
                process_name = proc.name()
                process_cpu = proc.cpu_percent(interval=None)
                process_memory = proc.memory_percent()
                process_score = proc.nice()

                # Store into temp object to be added to dictionary of current iteration.
                temp = ProcessData(process_name, process_cpu, process_memory, process_score)
                self.current_iteration_cpu[process_id] = temp

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def compare_last_iteration_to_current(self):
        for key in self.last_iteration_cpu:
            # If the key is in the last run and not in current_iteration_dict, we know that the process
            # has dropped off.
            if key not in self.current_iteration_cpu:
                print("Process removed: ", self.last_iteration_cpu[key].process_id, ":::",
                      self.last_iteration_cpu[key].process_cpu, ":::",
                      self.last_iteration_cpu[key].process_memory, ":::",
                      self.last_iteration_cpu[key].process_priority)

            else:
                Processor.check_cpu_differences(self, key)
                Processor.check_memory_differences(self, key)

    def compare_current_iteration_to_last(self):
        for key in self.current_iteration_cpu:
            # If the key is in current_iteration_dict (current run) and not in the last run dict then that means the
            # process has been added
            if key not in self.last_iteration_cpu:
                print("Process added: ", self.current_iteration_cpu[key].process_id, ":::",
                      self.current_iteration_cpu[key].process_cpu, ":::",
                      self.current_iteration_cpu[key].process_memory, ":::",
                      self.current_iteration_cpu[key].process_priority)

    def check_cpu_differences(self, key):

        last_iter_cpu = self.last_iteration_cpu[key].process_cpu / psutil.cpu_count()
        current_iter_cpu = self.current_iteration_cpu[key].process_cpu / psutil.cpu_count()

        if last_iter_cpu != 0 and current_iter_cpu != 0:
            # Since the key exists in both dicts, we can do comparisons of their resources used
            if last_iter_cpu > current_iter_cpu > 5:
                print("Process ", key, " with name ", self.last_iteration_cpu[key].process_id,
                      "decreased its CPU utilization by ",
                      hlp.calculate_percentage_difference
                      (last_iter_cpu, current_iter_cpu),
                      "percent. It's current CPU usage is",
                      round(current_iter_cpu, 1),
                      " percent.")
            elif last_iter_cpu < current_iter_cpu > 5:
                print("Process ", key, " with name ", self.last_iteration_cpu[key].process_id,
                      "increased its CPU utilization by ",
                      hlp.calculate_percentage_difference
                      (current_iter_cpu, last_iter_cpu),
                      "percent. It's current CPU usage is",
                      round(current_iter_cpu, 1),
                      " percent.")

    def check_memory_differences(self, key):

        last_iter_mem = self.last_iteration_cpu[key].process_memory
        current_iter_mem = self.current_iteration_cpu[key].process_memory

        if last_iter_mem != 0 and current_iter_mem != 0:
            if last_iter_mem > current_iter_mem > 5:
                print("Process ", key, " with name ", self.last_iteration_cpu[key].process_id,
                      "decreased its memory utilization by ",
                      hlp.calculate_percentage_difference
                      (last_iter_mem, current_iter_mem),
                      "percent. It's current memory usage is",
                      round(current_iter_mem, 1),
                      " percent.")
            elif last_iter_mem < self.current_iteration_cpu[key].process_memory > 5:
                print("Process ", key, " with name ", self.last_iteration_cpu[key].process_id,
                      "increased its memory utilization by ",
                      hlp.calculate_percentage_difference
                      (current_iter_mem, last_iter_mem),
                      "percent. It's current memory usage is",
                      round(current_iter_mem, 1),
                      " percent.")

    def check_gpu_utilization(self):

        current_gpu_utilization = GPUtil.getGPUs()[0].load * 100

        if self.gpu_utilization is None:
            self.gpu_utilization = current_gpu_utilization
            return
        else:
            if current_gpu_utilization != 0 and self.gpu_utilization != 0:
                if current_gpu_utilization > self.gpu_utilization:
                    if hlp.calculate_percentage_difference(current_gpu_utilization, self.gpu_utilization) > 100:
                        print("GPU utilization has increased by",
                              hlp.calculate_percentage_difference
                              (current_gpu_utilization, self.gpu_utilization),
                              "percent. It's current utilization is",
                              round(current_gpu_utilization, 1),
                              " percent."
                              )
                elif current_gpu_utilization < self.gpu_utilization:
                    if hlp.calculate_percentage_difference(self.gpu_utilization, current_gpu_utilization) > 100:
                        print("GPU utilization has decreased  by",
                              hlp.calculate_percentage_difference
                              (self.gpu_utilization, current_gpu_utilization),
                              "percent. It's current utilization is",
                              round(current_gpu_utilization, 1),
                              " percent."
                              )

        self.gpu_utilization = current_gpu_utilization
