class MemoryAllocation:
    def __init__(self, memory_blocks):
        self.memory_blocks = memory_blocks
        self.last_allocated_index = 0

    def best_fit(self, process_size):
        best_index = -1
        min_size = float('inf')
        
        for i, block in enumerate(self.memory_blocks):
            if block >= process_size and block < min_size:
                min_size = block
                best_index = i

        if best_index != -1:
            self.memory_blocks[best_index] -= process_size
            return f"Allocated at index {best_index} with {min_size} size block"
        else:
            return "Not allocated"

    def first_fit(self, process_size):
        for i, block in enumerate(self.memory_blocks):
            if block >= process_size:
                self.memory_blocks[i] -= process_size
                return f"Allocated at index {i} with {block} size block"
        return "Not allocated"

    def next_fit(self, process_size):
        n = len(self.memory_blocks)
        for i in range(self.last_allocated_index, n + self.last_allocated_index):
            index = i % n
            if self.memory_blocks[index] >= process_size:
                self.memory_blocks[index] -= process_size
                self.last_allocated_index = (index + 1) % n
                return f"Allocated at index {index} with {self.memory_blocks[index] + process_size} size block"
        return "Not allocated"

    def worst_fit(self, process_size):
        worst_index = -1
        max_size = -1

        for i, block in enumerate(self.memory_blocks):
            if block >= process_size and block > max_size:
                max_size = block
                worst_index = i

        if worst_index != -1:
            self.memory_blocks[worst_index] -= process_size
            return f"Allocated at index {worst_index} with {max_size} size block"
        else:
            return "Not allocated"

# Example Usage
memory_blocks = [100, 500, 200, 300, 600]
allocator = MemoryAllocation(memory_blocks)

processes = [212, 417, 112, 426]
strategies = ['best_fit', 'first_fit', 'next_fit', 'worst_fit']

for strategy in strategies:
    print(f"\nMemory allocation using {strategy} strategy:")
    allocator.memory_blocks = [100, 500, 200, 300, 600]  # Reset memory blocks for each strategy
    allocator.last_allocated_index = 0  # Reset last index for next_fit
    for process in processes:
        result = getattr(allocator, strategy)(process)
        print(f"Process size {process}: {result}")