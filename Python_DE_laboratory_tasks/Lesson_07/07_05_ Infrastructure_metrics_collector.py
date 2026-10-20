# Telemetry data stream from cluster servers
system_telemetry = [
("srv_01", 12.5, 64, "online"),
("srv_02", 85.0, 92, "online"),
("srv_03", 0.0, 0, "offline"),
("srv_04", 45.2, 78, "online"),
("srv_05", 95.1, 99, "active")
]

# Implementation of a metrics aggregation pipeline
active_network_nodes = []
average_cpu = []
max_ram = []

for node_name, cpu_load, ram_usage, status in system_telemetry:
    if status != "offline":
        active_network_nodes.append(node_name)
        average_cpu.append(cpu_load)
        max_ram.append(ram_usage)

telemetry_dict = dict(active_nodes_count=len(active_network_nodes), 
                    metrics=dict(average_cpu=round(sum(average_cpu)/len(active_network_nodes), 2), 
                    max_ram=max(max_ram)))

# Result output
print(f"Active nodes in the network: {active_network_nodes}")
print(f"Final telemetry report: {telemetry_dict}")
