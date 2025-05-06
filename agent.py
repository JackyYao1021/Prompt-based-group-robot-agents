class Agent:
    def __init__(self, id, start_pos, env):
        self.id = id
        self.position = start_pos
        self.env = env
        self.path = []

    def plan(self, goal):
        # 调用搜索算法
        from search_algorithms import bfs
        self.path = bfs(self.env, self.position, goal)

    def move(self):
        if self.path:
            self.position = self.path.pop(0)