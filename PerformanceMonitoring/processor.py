import psutil
import GPUtil
import helpers as hlp
import constants
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
                cur_cpu_percent = round(proc.cpu_percent(interval=None) / psutil.cpu_count(), 2)
                cur_mem_percent = round(proc.memory_percent(), 2)
                if cur_cpu_percent > constants.CPU_THRESHOLD and cur_mem_percent > constants.MEMORY_THRESHOLD:
                    # Get process name, pid, cpu percent, memory percent, and priority.
                    process_name = proc.name()
                    process_id = proc.pid
                    process_cpu = cur_cpu_percent
                    process_memory = cur_mem_percent
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
                if self.last_iteration_cpu[key].process_id != "pycharm64.exe":
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
                print("Process added:", self.current_iteration_cpu[key].process_id, ":::",
                      self.current_iteration_cpu[key].process_cpu, ":::",
                      self.current_iteration_cpu[key].process_memory, ":::",
                      self.current_iteration_cpu[key].process_priority)

    def check_cpu_differences(self, key):

        last_iter_cpu = self.last_iteration_cpu[key].process_cpu
        current_iter_cpu = self.current_iteration_cpu[key].process_cpu

        if hlp.calculate_percentage_difference(last_iter_cpu,
                                               current_iter_cpu) > constants.CPU_PERCENTAGE_CHANGE_THRESHOLD:
            # Since the key exists in both dicts, we can do comparisons of their resources used
            if last_iter_cpu > current_iter_cpu:
                print(constants.CPU_DECREASED_UTILIZATION_MSG.format(key, self.last_iteration_cpu[key].process_id,
                                                                     hlp.calculate_percentage_difference
                                                                     (current_iter_cpu, last_iter_cpu),
                                                                     round(current_iter_cpu, 2)
                                                                     ))
            elif last_iter_cpu < current_iter_cpu:
                print(constants.CPU_INCREASED_UTILIZATION_MSG.format(key, self.last_iteration_cpu[key].process_id,
                                                                     hlp.calculate_percentage_difference
                                                                     (current_iter_cpu, last_iter_cpu),
                                                                     round(current_iter_cpu, 2)
                                                                     ))

    def check_memory_differences(self, key):

        last_iter_mem = self.last_iteration_cpu[key].process_memory
        current_iter_mem = self.current_iteration_cpu[key].process_memory

        if hlp.calculate_percentage_difference(last_iter_mem,
                                               current_iter_mem) > constants.MEMORY_PERCENTAGE_CHANGE_THRESHOLD:
            if last_iter_mem > current_iter_mem:
                print(constants.MEMORY_DECREASED_UTILIZATION_MSG.format(key, self.last_iteration_cpu[key].process_id,
                                                                        hlp.calculate_percentage_difference
                                                                        (current_iter_mem, last_iter_mem),
                                                                        round(current_iter_mem, 2)
                                                                        ))
            elif last_iter_mem < current_iter_mem:
                print(constants.MEMORY_INCREASED_UTILIZATION_MSG.format(key, self.last_iteration_cpu[key].process_id,
                                                                        hlp.calculate_percentage_difference
                                                                        (current_iter_mem, last_iter_mem),
                                                                        round(current_iter_mem, 2)
                                                                        ))

    def check_gpu_utilization(self):

        current_gpu_utilization = GPUtil.getGPUs()[0].load * 100

        if self.gpu_utilization is None:
            self.gpu_utilization = current_gpu_utilization
            return
        else:
            if current_gpu_utilization != 0 and self.gpu_utilization != 0 and \
                    hlp.calculate_percentage_difference(current_gpu_utilization, self.gpu_utilization) > \
                    constants.GPU_PERCENTAGE_CHANGE_THRESHOLD:
                if current_gpu_utilization > self.gpu_utilization:
                    print(constants.MEMORY_DECREASED_UTILIZATION_MSG.format(hlp.calculate_percentage_difference
                                                                          (self.gpu_utilization, current_gpu_utilization),
                                                                          round(current_gpu_utilization, 2)
                                                                          ))
                else:
                    print(constants.MEMORY_INCREASED_UTILIZATION_MSG.format(hlp.calculate_percentage_difference
                                                                          (self.gpu_utilization, current_gpu_utilization),
                                                                          round(current_gpu_utilization, 2)
                                                                          ))

        self.gpu_utilization = current_gpu_utilization
