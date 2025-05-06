from environment import Environment
from agent import Agent

def main():
    env = Environment('map.txt')
    agents = [Agent(i, pos, env) for i, pos in enumerate(env.start_positions)]
    for agent in agents:
        agent.plan(env.end_position)
    # 简单模拟移动
    for step in range(20):
        for agent in agents:
            agent.move()
            print(f"Agent {agent.id} at {agent.position}")

if __name__ == "__main__":
    main()