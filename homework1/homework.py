from itertools import chain

RESULT = []


def can_move(index, state, zero_index):
    """Check whether the empty sign could be moved."""
    if index < 0:
        return state[zero_index + index] == 1 and zero_index + index > -1
    return zero_index + index < len(state) and state[zero_index + index] == 2


def dfs(state, end=[], zero_index=0):
    """Do Depth-First Search recursively."""
    if state == end:
        return True
    for i in [-2, -1, 1, 2]:
        if can_move(i, state, zero_index):
            new_state = change_elements(state, zero_index, zero_index + i)
            if(dfs(new_state, end=end, zero_index=zero_index + i)):
                # print(new_state)
                RESULT.append(new_state)
                return True
    return False


def change_elements(items, old_index, new_index):
    """Switch places of two elements in list collection."""
    new_items = items[:]
    new_items[old_index], new_items[new_index] = new_items[new_index], new_items[old_index]
    return new_items


def define_start_and_goal(count, first=1, second=2):
    """Create start and end states."""
    if count:
        return list(chain([first] * count, [0], [second] * count))
    return []


def create_state(n):
    """Create start and end points."""
    count = n // 2
    start = define_start_and_goal(count, first=1, second=2)
    end = define_start_and_goal(count, first=2, second=1)
    return count, start, end


def call_dfs(n):
    """Call dfs algorithm with only n as frog's total count."""
    count, start, end = create_state(n)
    if dfs(start, end=end, zero_index=count):
        RESULT.append(start)
        for path in RESULT[::-1]:
            print(path)
        return True
    return False


if __name__ == '__main__':
    call_dfs(2)
