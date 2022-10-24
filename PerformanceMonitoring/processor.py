import psutil

from PerformanceMonitoring.gui import show_data
from PerformanceMonitoring.process_data import ProcessData


class Processor:
    current_iteration_dict = {}
    process_dict = {}

    def process(self):
        Processor.get_processes(self)
        if not Processor.check_empty_dict(self):
            self.process_dict = self.current_iteration_dict
            return

        Processor.compare_current_iteration_to_last(self)
        Processor.compare_last_iteration_to_current(self)

        self.process_dict = self.current_iteration_dict

    def get_processes(self):

        self.current_iteration_dict = {}

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
                self.current_iteration_dict[process_id] = temp

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def compare_last_iteration_to_current(self):
        for key in self.process_dict:
            # If the key is in process_dict (last run) and not in current_iteration_dict, we know that the process
            # has dropped off.
            if key not in self.current_iteration_dict:
                print("Process removed: ", self.process_dict[key].process_id, ":::",
                      self.process_dict[key].process_cpu, ":::",
                      self.process_dict[key].process_memory, ":::", self.process_dict[key].process_priority)

            else:
                Processor.check_cpu_differences(self, key)
                Processor.check_memory_differences(self, key)

    def compare_current_iteration_to_last(self):
        for key in self.current_iteration_dict:
            # If the key is in current_iteration_dict (current run) and not in the last run dict then that means the
            # process has been added
            if key not in self.process_dict:
                print("Process added: ", self.current_iteration_dict[key].process_id, ":::",
                      self.current_iteration_dict[key].process_cpu, ":::",
                      self.current_iteration_dict[key].process_memory, ":::",
                      self.current_iteration_dict[key].process_priority)

    def check_cpu_differences(self, key):
        if self.process_dict[key].process_cpu != 0 and self.current_iteration_dict[key].process_cpu != 0:
            # Since the key exists in both dicts, we can do comparisons of their resources used
            if self.process_dict[key].process_cpu > self.current_iteration_dict[key].process_cpu:
                print("Process ", key, " with name ", self.process_dict[key].process_id,
                      "decreased its CPU utilization by ",
                      (self.process_dict[key].process_cpu - self.current_iteration_dict[key].process_cpu) /
                      self.current_iteration_dict[key].process_cpu * 100,
                      "percent.")
            elif self.process_dict[key].process_cpu < self.current_iteration_dict[key].process_cpu:
                print("Process ", key, " with name ", self.process_dict[key].process_id,
                      "increased its CPU utilization by ",
                      (self.current_iteration_dict[key].process_cpu - self.process_dict[key].process_cpu) /
                      self.process_dict[key].process_cpu * 100
                      , "percent.")

    def check_memory_differences(self, key):
        if self.process_dict[key].process_memory != 0 and self.current_iteration_dict[key].process_memory != 0:
            if self.process_dict[key].process_memory > self.current_iteration_dict[key].process_memory:
                print("Process ", key, " with name ", self.process_dict[key].process_id,
                      "decreased its memory utilization by ",
                      (self.process_dict[key].process_memory - self.current_iteration_dict[key].process_memory) /
                      self.current_iteration_dict[key].process_memory * 100,
                      "percent.")
            elif self.process_dict[key].process_memory < self.current_iteration_dict[key].process_memory:
                print("Process ", key, " with name ", self.process_dict[key].process_id,
                      "increased its memory utilization by ",
                      (self.current_iteration_dict[key].process_memory - self.process_dict[key].process_memory) /
                      self.process_dict[key].process_memory * 100
                      , "percent.")

    def check_empty_dict(self):
        return bool(self.process_dict)
