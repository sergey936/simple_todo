from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(BaseException):

    @property
    def message(self):
        return 'Application Exception'
