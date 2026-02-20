

from kubernetes import client, config
from tabulate import tabulate
import argparse


config.load_kube_config()
v1 = client.CoreV1Api()

def get_node_type(namespace=None):
    if namespace is not None:
        pods = v1.list_namespaced_pod(namespace=namespace, watch=False)
    else:
        pods = v1.list_pod_for_all_namespaces(watch=False)

    results = []
    for pod in pods.items:
        pod_name = pod.metadata.name
        ns_name = pod.metadata.namespace
        node_name = pod.spec.node_name if pod.spec.node_name else "N/A"
        if node_name and node_name != "N/A":
            try:
                node = v1.read_node(node_name)
                labels = node.metadata.labels
                node_type = labels.get('NodePoolType') or labels.get('NodeGroupType') or 'N/A'
                    
            except Exception as e:
                print(f"Error: {e}")
        
        results.append([ns_name, pod_name, node_name, node_type])
    return results

def print_table(results, filter_column=None, filter_value=None):
    headers = ["Namespace", "Pod", "Node", "Node_Type"]
    if filter_column and filter_value:
        column_index = {"Namespace": 0, "Pod": 1, "Node": 2, "Node_Type": 3}
        idx = column_index.get(filter_column)
        if idx is not None:
            results = [row for row in results if row[idx] == filter_value]
            print(f"Filtered by {filter_column} = {filter_value}\n")
    return tabulate(results, headers=headers, tablefmt="grid")

def get_args():
    parser = argparse.ArgumentParser(description="Get pods and their node pool/node group information")
    parser.add_argument("-n", "--namespace", type=str, help="Specific namespace to query (if not provided, queries all namespaces)")
    parser.add_argument("-f", "--filter-column", type=str, nargs=2, metavar=('COLUMN', 'VALUE'), help='Filter by column and value (e.g., -f "Node_Type" "system-vm")')
    return parser.parse_args()

def display_pods(namespace=None, filter_column=None, filter_value=None):
    if namespace:
        print(f"\nQuerying namespace: {namespace}\n")
    else:
        print("\nQuerying all namespaces...\n")
    
    results = get_node_type(namespace=namespace)
    return(print_table(results, filter_column=filter_column, filter_value=filter_value))

if __name__ == "__main__":
    args = get_args()
    filter_column=args.filter_column[0] if args.filter_column else None
    filter_value=args.filter_column[1] if args.filter_column else None
    if filter_column and filter_value:
        print(f"Filtering by {filter_column} = {filter_value}\n")
    print(display_pods(namespace=args.namespace, filter_column=filter_column, filter_value=filter_value))  
    