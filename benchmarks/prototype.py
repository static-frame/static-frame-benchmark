import inspect

from types import SimpleNamespace

PREFIX_TIME = 'asv_time_'


def apply_prototype(cls_prototype):
    def decorator(cls):

        for name in dir(cls_prototype):
            if name.startswith(PREFIX_TIME):
                name_new = name.replace(PREFIX_TIME, 'time_')
                name_pretty = f"{name.replace(PREFIX_TIME, '')}-{cls.FIXTURE}"

                # NOTE: must bind Prototype func name at func def time
                def func_new(self, ns: SimpleNamespace, name_prototype=name):
                    return getattr(cls_prototype, name_prototype)(self, ns)

                func_new.pretty_name = name_pretty
                func_new.pretty_source = inspect.getsource(getattr(cls_prototype, name))

                setattr(cls, name_new, func_new)
        return cls
    return decorator
