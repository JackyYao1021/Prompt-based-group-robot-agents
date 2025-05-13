import re
from collections import defaultdict
import pandas as pd

def parse_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split content into maze trials
    maze_trials = content.split('maze ')[1:]
    
    parsed_trials = []
    for trial in maze_trials:
        # Extract maze number
        maze_num = int(trial.split('\n')[0])
        
        # Extract excavator paths
        paths = {}
        for line in trial.split('\n'):
            if line.startswith('excavator E') and 'path:' in line:
                excavator = line.split('excavator ')[1].split(' ')[0]
                path_str = line.split('path: ')[1]
                path = eval(path_str) 
                paths[excavator] = path
        
        parsed_trials.append({
            'maze_num': maze_num,
            'paths': paths
        })
    
    return parsed_trials

def detect_region_conflicts(trial):
    paths = trial['paths']
    region_conflicts = []
    
    max_path_length = max(len(path) for path in paths.values())
    
    position_occupancy = defaultdict(list)
    for excavator, path in paths.items():
        for t, pos in enumerate(path):
            position_occupancy[pos].append((excavator, t))
    
    for position, occupancy_list in position_occupancy.items():
        if len(occupancy_list) <= 1:
            continue

        occupancy_list.sort(key=lambda x: x[1])
        
        for i in range(len(occupancy_list)):
            for j in range(i+1, len(occupancy_list)):
                excavator_i, time_i = occupancy_list[i]
                excavator_j, time_j = occupancy_list[j]
                
                if time_i == time_j:
                    region_conflicts.append({
                        'type': 'RC',
                        'position': position,
                        'time_step': time_i,
                        'excavators': [excavator_i, excavator_j]
                    })
    
    return region_conflicts

def detect_opening_conflicts(trial):
    paths = trial['paths']
    opening_conflicts = []
    
    for excavator_i, path_i in paths.items():
        for t in range(1, len(path_i)):
            prev_pos_i = path_i[t-1]
            curr_pos_i = path_i[t]
            
            if prev_pos_i != curr_pos_i:
                for excavator_j, path_j in paths.items():
                    if excavator_i == excavator_j or t >= len(path_j):
                        continue
                        
                    prev_pos_j = path_j[t-1] if t-1 < len(path_j) else None
                    curr_pos_j = path_j[t]
                    
                    if prev_pos_j and prev_pos_j != curr_pos_j:
                        if curr_pos_i == prev_pos_j and prev_pos_i == curr_pos_j:
                            opening_conflicts.append({
                                'type': 'OC',
                                'positions': (prev_pos_i, curr_pos_i),
                                'time_step': t,
                                'excavators': [excavator_i, excavator_j]
                            })
    
    return opening_conflicts

def conflict_detection(task_assign_method):
    trials = parse_file(f'results/experiment_2/{task_assign_method}.txt')
    
    total_rc = 0
    total_oc = 0
    
    for trial in trials:
        region_conflicts = detect_region_conflicts(trial)
        opening_conflicts = detect_opening_conflicts(trial)
        
        print(f"\nMaze {trial['maze_num']}:")
        
        print("Region Conflicts (RC):")
        if region_conflicts:
            print(f"  Found {len(region_conflicts)} region conflicts:")
            for conflict in region_conflicts:
                print(f"  Time step {conflict['time_step']}: Excavators {', '.join(conflict['excavators'])} "
                      f"conflict at position {conflict['position']}")
            total_rc += len(region_conflicts)
        else:
            print("  No region conflicts found")
            
        print("Opening Conflicts (OC):")
        if opening_conflicts:
            print(f"  Found {len(opening_conflicts)} opening conflicts:")
            for conflict in opening_conflicts:
                print(f"  Time step {conflict['time_step']}: Excavators {', '.join(conflict['excavators'])} "
                      f"swap positions between {conflict['positions'][0]} and {conflict['positions'][1]}")
            total_oc += len(opening_conflicts)
        else:
            print("  No opening conflicts found")
    
    print(f"\nSummary:")
    print(f"Total Region Conflicts: {total_rc}")
    print(f"Total Opening Conflicts: {total_oc}")
    print(f"Total Conflicts: {total_rc + total_oc}")
    
    return total_rc, total_oc

if __name__ == "__main__":
    methods = ["random", "nearest", "simple_hungarian", "hungarian", "bid"]
    
    df = pd.DataFrame(columns=methods)
    
    for method in methods:
        total_rc, total_oc = conflict_detection(method)
        df[method] = [total_rc, total_oc, total_rc + total_oc]
    
    print(df.to_latex())
