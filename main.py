
import argparse

import tensorflow as tf

# from flair.models import TextClassifier
# from flair.data import Sentence


def main() -> None:
    # classifier = TextClassifier.load('en-sentiment')
    # sentence = Sentence('Angry words. This is a negative sentence.')
    # classifier.predict(sentence)
    # print sentence with predicted labels
    # print('Sentence above is: ', sentence.labels)

    print(tf.config.list_physical_devices('GPU'))


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument(
        '-t',
        '--train',
        dest='is_train',
        type=bool,
        required=False,
        default=False,
        help=''
    )

    main()
