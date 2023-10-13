from qiskit import IBMQ, BasicAer
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute
import itertools

dogs = ['abut', 'betty', 'coco']
friends_enemies = f"\tabut-betty are friends; coco-abut and coco-betty are enemies."

# create a quantum register of 3 qubits
q = QuantumRegister(3)
# create a classical register of 3 bits
c = ClassicalRegister(3)
# Create a Quantum Circuit
qc = QuantumCircuit(q, c)
# add a hadamard gate on qubit
qc.h(q)
# measure the circuit
qc.measure(q, c)

# visualize the result
qc.draw()

# allocate rooms for dogs for a given config
# '101' -> [[betty], [abut, coco]]
# return a list of rooms
def get_rooms(config):
    room1 = []
    room2 = []
    conf = [int(x) for x in config]
    index = 0
    for i in conf:
        dog = dogs[index]
        if i == 0:
            room1.append(dog)
        elif i == 1:
            room2.append(dog)
        index += 1
    return [room1, room2]

# Calculate and generate a sorted dictionary with the score as the key and collection of configs as its value
# return a tuple from the dictionary with the highest score
def get_result(config_map):
    all_configs = config_map.keys()
    result = {}
    for config in all_configs:
        rooms = get_rooms(config)
        total_score = 0
        for room in rooms:
            for a, b in itertools.combinations(room, 2):
                if a == 'abut' and b == 'betty':
                    total_score += 1
                else:
                    total_score -= 1
        if total_score in result.keys():
            result[total_score].append(config)
        else:
            result[total_score] = [config]
    return sorted(result.items(), reverse=True)[0]
    
    def print_result(config, all_configs):
    print(f"All dogs: {dogs}")
    print(friends_enemies)
    print("All rooms: 0 -> room 1;  1-> room 2")
    print("\nAll configurations:")
    print(*all_configs, sep=", ")
    # score = config[0]
    best_configs = config[1]
    print("\nBest configuration(s):")
    index = 1
    for c in best_configs:
        rooms = get_rooms(c)
        room1 = ', '.join(rooms[0])
        room2 = ', '.join(rooms[1])
        print(f"\t - Option {index} ({c}):  {room1} stay in room 1. {room2} stay in room 2")
        index += 1
        
        print("Running on local simulator: qasm_simulator")
job = execute(qc, backend=BasicAer.get_backend('qasm_simulator'))
temp = job.result().get_counts(qc)
result = get_result(temp)
print_result(result, temp)

# IBMQ.save_account('token')
# IBMQ.load_account()
# provider = IBMQ.enable_account('you_token')
provider = IBMQ.get_provider('ibm-q')
provider.backends()
backend = provider.get_backend('ibmq_qasm_simulator')
job = execute(qc, backend)
print("Running on", backend.name())
temp = job.result().get_counts(qc)
result = get_result(temp)
print_result(result, temp)
