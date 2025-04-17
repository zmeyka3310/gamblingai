import os
def shutup():
    """
    Make Tensorflow less verbose
    """
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    os.environ['GRPC_VERBOSITY'] = 'NONE'

    # noinspection PyPackageRequirements
    import tensorflow as tf
    from tensorflow.python.util import deprecation

    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    # Monkey patching deprecation utils to shut it up! Maybe good idea to disable this once after upgrade
    # noinspection PyUnusedLocal
    def deprecated(date, instructions, warn_once=True):  # pylint: disable=unused-argument
        def deprecated_wrapper(func):
            return func
        return deprecated_wrapper

    deprecation.deprecated = deprecated