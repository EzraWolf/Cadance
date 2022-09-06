
from .predict import predict

from .train import train

from .. import BaseNN


class CadancePredictor(BaseNN):
    '''
    The main neural network used to
    predict stock values
    '''

    def __init__(self) -> None:
        pass


__all__ = [

    # predict.py
    'predict',

    # train.py
    'train',
]
