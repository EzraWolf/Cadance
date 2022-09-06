
import datetime as dt


class Log(object):
    '''
    A simple logger made to streamline
    understandable and concise logging
    '''
    def __init__(
        self,
        name: str,
        message: str,
        path: str = 'logs'
    ) -> None:
        self._msg = message
        self._name = name
        self._path = f'{path}/{name}'

    def default(self, type: str = None, is_print: bool = False) -> None:
        '''
        The default / goto logging method.
        This function handles the blunt of the logging efforts.
        '''

        if type:
            if len(type) > 15:
                raise ValueError(
                    '<type> cannot be more than 15 characters long'
                )

            self._path += f'-{type.lower()}'

        self._path += '.log'

        _time: dt.datetime = dt.datetime.now()

        # 2022 Sep-22, 23h-14m-45s (UNIX TIMESTAMP)
        time_str: str = _time.strftime('%Y %a-%d, %Hh-%Mm-%Ss')
        time_str += f' ({int(_time.timestamp())})'

        self._msg = f'[{time_str}]: {self._msg.strip()}'

        # Create or open the logging
        # file and print if necessary
        with open(self._path, 'a') as f:
            f.write(f'{self._msg}\n')

        if is_print:

            # Fill the gaps between types with different lengths
            print('{:15} {}'.format(type.upper(), self._msg))

    def normal(self, is_print: bool = False) -> None:
        '''A preset for logging normal events'''
        self.default('normal', is_print)

    def warning(self, is_print: bool = False) -> None:
        '''A preset for logging warnings / small issues'''
        self.default('warning', is_print)

    def critical(self, is_print: bool = False) -> None:
        '''A preset for logging software-breaking issues'''
        self.default('critical', is_print)
