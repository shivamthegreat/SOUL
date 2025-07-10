import psutil
import platform
import math

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def system_stats():
    # CPU Info
    cpu_usage = psutil.cpu_percent(interval=1)
    physical_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    cpu_name = platform.processor()

    # Memory Info
    virtual_mem = psutil.virtual_memory()
    memory_used = convert_size(virtual_mem.used)
    memory_total = convert_size(virtual_mem.total)

    # Disk Info (Assume main disk is C:)
    disk = psutil.disk_usage('/')
    disk_used = convert_size(disk.used)
    disk_total = convert_size(disk.total)

    # Battery Info
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "No battery detected"

    # Compose result
    final_res = (
        f"CPU: {cpu_name}\n"
        f"Usage: {cpu_usage}%\n"
        f"Cores: {physical_cores} physical / {total_cores} logical\n"
        f"Frequency: {round(cpu_freq.current, 2)} MHz\n\n"
        f"RAM: {memory_used} used out of {memory_total}\n"
        f"Disk: {disk_used} used out of {disk_total}\n"
        f"Battery Level: {battery_percent}%"
    )
    return final_res

# Example usage
#if __name__ == "__main__":
 #   print(system_stats())
