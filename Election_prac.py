import time

class Node:
    def __init__(self, id):
        self.id = id
        self.coordinator = None

    def initiate_ring_election(self, nodes):
        print(f"Node {self.id} starts the ring election")
        participants = []

        for node in nodes:
            if node.coordinator is None:
                participants.append(node.id)
            
        max_id = max(participants)
        for node in nodes:
            node.coordinator = max_id
        print(f"Node {max_id} becomes the coordinator(Ring)")
    
    def start_ring_election(self, nodes):
        if self.coordinator is None:
            print(f"Node {self.id} passes the election message.")
            time.sleep(1)
            self.initiate_ring_election(nodes)

    def start_bully_election(self, nodes):
        print(f"Node {self.id} starts Bully Election.")
        higher_nodes = [node for node in nodes if node.id > self.id]

        if not higher_nodes:
            for node in nodes:
                node.coordinator = self.id
                print(f"Node {self.id} becomes the coordinator")
                return

        for higher_node in sorted(higher_nodes, key=lambda x: x.id, reverse=True):
            higher_node.send_bully_message(nodes)
            
    def send_bully_message(self, nodes):
        print(f"Node {self.id} received message.")
        time.sleep(1)

        if not any(node.id > self.id for node in nodes):
            for node in nodes:
                node.coordinator = self.id
            print(f"Node {self.id} becomes coordinator(Bully)")

def main():
    nodes = [Node(1), Node(2), Node(3), Node(5), Node(4)]
    print("Starting Ring election: ")
    nodes[0].start_ring_election(nodes)
    print(f"Coordinator after Ring election is Node {nodes[0].coordinator}")

    for node in nodes:
        node.coordinator = None

    print("Starting bully election: ")
    nodes[0].start_bully_election(nodes)
    print(f"Coordinator after Bully election is Node {nodes[0].coordinator}")    

if __name__ == "__main__":
    main()
        