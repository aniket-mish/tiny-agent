import time
from llm import call_llm

class BaseNode:
    def __init__(self):
        self.params = {}
        self.successors = {}

    def next(self, node, action="default"):
        self.successors[action] = node
        return node

    def prep(self, shared):
        pass
    
    def exec(self, prep_res):
        response = call_llm(prep_res)
        return response

    def post(self, shared, prep_res, exec_res):
        pass

    def _run(self, shared):
        p = self.prep(shared)
        e = self._exec(shared, p)
        return self.post(shared, p, e)


class Node(BaseNode):
    def __init__(self, max_retries=3, wait=0):
        super().__init__()
        self.max_retries = max_retries
        self.wait = wait

    def _exec(self, prep_res):
        for self.cur_retry in range(self.max_retries):
            try:
                return self.exec(prep_res)
            except Exception as e:
                if self.wait > 0:
                    time.sleep(self.wait)
                if self.cur_retry == self.max_retries - 1:
                    return self.exec_fallback(prep_res, e)

    def exec_fallback(self, prep_res, e):
        raise e


class Flow(BaseNode):
    def _orch(self, shared, params=None):
        while cur:
            last_action = cur._run(shared)
            cur = self.get_next_node(cur, last_action)

    def get_next_node(self, cur, action):
        return cur.successors.get(action or "default")