from PerformanceMonitoring.processor import Processor


def main():
    proc = Processor()
    # Loop to keep  the collection of processes continuing.
    while True:

        proc.process()


if __name__ == '__main__':
    main()
