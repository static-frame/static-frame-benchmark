import inspect

from types import SimpleNamespace

PREFIX_TIME = 'asv_time_'

# NOTE: could not get setup_cache to work unless implemented explicitly on the derived class; could not populate it here dynamically either
# see https://github.com/airspeed-velocity/asv/issues/880

def apply_prototype(cls_prototype, group: str):
    def decorator(cls):

        # NOTE: approach to temporarily exercising only one module
        # if cls.__module__ != 'benchmarks.frame_method_go':
        #     return cls

        for name in dir(cls_prototype):
            if name.startswith(PREFIX_TIME):
                name_new = name.replace(PREFIX_TIME, 'time_')
                name_pretty = f"{name.replace(PREFIX_TIME, '')}-{cls.FIXTURE}"

                # NOTE: must bind Prototype func name at func def time
                def func_new(self, ns: SimpleNamespace, name_prototype=name):
                    return getattr(cls_prototype, name_prototype)(self, ns)

                func_new.pretty_name = name_pretty
                func_new.pretty_source = inspect.getsource(getattr(cls_prototype, name))

                # replacing module with a normalized group name; function name must start with "time"
                func_new.benchmark_name = f'{group}.{cls.__name__}.{name_new}'

                setattr(cls, name_new, func_new)
        return cls
    return decorator
