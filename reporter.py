import platform
import psutil

my_system = platform.uname()

print(f"System: {my_system.system}")
print(f"Node Name: {my_system.node}")
print(f"Release: {my_system.release}")
print(f"Version: {my_system.version}")
print(f"Machine: {my_system.machine}")
print(f"Processor: {my_system.processor}")


print(f"Memory :{psutil.virtual_memory()}")
print(f"Memory :{psutil.virtual_memory()[0]}")
print(type(psutil.virtual_memory()[0]))
mem = psutil.virtual_memory()[0]
print(mem // 1024 // 1024)
print(type({psutil.virtual_memory()}))

print(psutil.boot_time())
print(int(psutil.boot_time()))

print(psutil.swap_memory())
print(psutil.disk_usage('/'))
print(psutil.disk_partitions())
print(psutil.disk_io_counters())

print(psutil.cpu_count())
print(psutil.cpu_percent())
print(psutil.cpu_times())
print(psutil.cpu_stats())

# print(psutil.test())