'''

Question:

Write a tool that will connect to a Cassandra cluster and collect performance-related metrics.
The metrics to collect should include, but not be limited to:

Node CPU and memory usage
Read and write latencies
Number of pending compactions
Number of active connections
Storage space utilization

The output should be displayed on the command-line in key-value type of format

'''

'''

Answer:

I have implemented using python language
I have used python package "cassandra-driver"

Install the "cassandra-driver" library by running 

pip install cassandra-driver.

'''

## Importing Required Libraries
from cassandra.cluster import Cluster

## Connecting to the Cassandra Cluster
'''
This function takes a list of contact points (IP addresses or hostnames of the Cassandra cluster nodes) as input. 
It creates a Cluster object with the provided contact points and connects to the cluster using the connect() method. 
Finally, it returns the session object for executing queries.
'''


def connect_to_cluster(contact_points):
    cluster = Cluster(contact_points)
    session = cluster.connect()
    return session

## Collecting Node Metrics
'''

This function takes the session object as input and initializes an empty dictionary called metrics to store the collected metrics.
It then executes several CQL queries against system tables to gather the desired metrics.

Node CPU and memory usage: The query SELECT host_id, cpu_usage, memory_usage FROM system.node_metrics; retrieves the CPU and memory 
usage for each node in the cluster. The for loop iterates over the result rows and adds the metrics to the metrics dictionary with appropriate keys.

Read and write latencies: The query SELECT keyspace_name, table_name, read_latency, write_latency FROM system.size_estimates; fetches the read 
and write latencies for each keyspace and table. Similarly, the loop adds these metrics to the metrics dictionary.

Number of pending compactions: The query SELECT pending_compactions FROM system.compaction_history; retrieves the number of pending compactions. 
The loop adds this metric with the key "Pending Compactions".

Number of active connections: The query SELECT active_connections FROM system.views_builds_in_progress; fetches the number of active connections. 
The loop adds this metric with the key "Active Connections".

Storage space utilization: The query `SELECT keyspace_name, table_name, space_used_live FROM system.size_estimates;" retrieves the storage space 
utilization for each keyspace and table. The loop adds these metrics to the metrics dictionary.

'''


def collect_node_metrics(session):
    metrics = {}

    # Node CPU and memory usage
    result = session.execute("SELECT host_id, cpu_usage, memory_usage FROM system.node_metrics;")
    for row in result:
        metrics[f"Node {row.host_id} CPU Usage"] = row.cpu_usage
        metrics[f"Node {row.host_id} Memory Usage"] = row.memory_usage

    # Read and write latencies
    result = session.execute("SELECT keyspace_name, table_name, read_latency, write_latency FROM system.size_estimates;")
    for row in result:
        metrics[f"{row.keyspace_name}.{row.table_name} Read Latency"] = row.read_latency
        metrics[f"{row.keyspace_name}.{row.table_name} Write Latency"] = row.write_latency

    # Number of pending compactions
    result = session.execute("SELECT pending_compactions FROM system.compaction_history;")
    for row in result:
        metrics["Pending Compactions"] = row.pending_compactions

    # Number of active connections
    result = session.execute("SELECT active_connections FROM system.views_builds_in_progress;")
    for row in result:
        metrics["Active Connections"] = row.active_connections

    # Storage space utilization
    result = session.execute("SELECT keyspace_name, table_name, space_used_live FROM system.size_estimates;")
    for row in result:
        metrics[f"{row.keyspace_name}.{row.table_name} Storage Space Utilization"] = row.space_used_live

    return metrics


'''

This function takes the metrics dictionary as input and iterates over its items. For each key-value pair, it prints the metric in a key-value format.

'''

def display_metrics(metrics):
    for key, value in metrics.items():
        print(f"{key}: {value}")


'''

In the main block, we define the contact points, which are the IP addresses or hostnames of the Cassandra cluster nodes. 
Replace "127.0.0.1" with the appropriate contact points for your cluster.

We then call the connect_to_cluster() function to establish a session with the cluster. The session object is used as input 
for the collect_node_metrics() function, which retrieves the metrics from the Cassandra cluster and stores them in the metrics dictionary.

Finally, the display_metrics() function is called to print the metrics in a key-value format on the command line.

'''

if __name__ == "__main__":
    
    '''
    Update the contact points to match your Cassandra cluster
    specify your ip address in this contact points list
    '''
    contact_points = ["127.0.0.1"]

    session = connect_to_cluster(contact_points)
    metrics = collect_node_metrics(session)
    display_metrics(metrics)
''''''