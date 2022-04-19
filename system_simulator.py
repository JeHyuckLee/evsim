from system_executor import SysExecutor
from definition import SingletonType


class SystemSimulator(object):
    __metaclass__ = SingletonType
    _engine = {}

    @staticmethod
    #이름, 모드(리얼, 가상), 스탭을 받아 SysExecutor객체 생성해 engine딕셔너리에 등록
    def register_engine(sim_name, sim_mode='VIRTUAL_TIME', time_step=1):
        SystemSimulator._engine[sim_name] = SysExecutor(
            time_step, sim_name, sim_mode)

    #등록해놓은 엔진 목록 반환
    @staticmethod
    def get_engine_map():
        return SystemSimulator._engine

    #등록해놓은 엔진 목록 중 이름을 지정하여 가져옴 
    @staticmethod
    def get_engine(sim_name):
        return SystemSimulator._engine[sim_name]

    @staticmethod
    def is_terminated(sim_name):
        return SystemSimulator._engine[sim_name].is_terminated()

    @staticmethod
    def set_learning_module(sim_name, learn_module):
        SystemSimulator._engine[sim_name].set_learning_module(learn_module)
        pass

    @staticmethod
    def get_learning_module(sim_name):
        return SystemSimulator._engine[sim_name].get_learning_module()

    @staticmethod
    def is_terminated(sim_name):
        return SystemSimulator._engine[sim_name].is_terminated()

    @staticmethod
    def exec_simulation_instance(instance_path):
        sim_instance = None
        with open(instance_path, 'rb') as f:
            sim_instance = dill.load(f)
            SystemSimulator._engine[sim_instance.get_name()] = sim_instance
            sim_instance.simulate()
        pass

    def __init__(self):
        pass
