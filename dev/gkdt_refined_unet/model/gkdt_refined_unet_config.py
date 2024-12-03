import tensorflow as tf


class GKDTRefinedUNetConfig(tf.Module):
    def __init__(
        self,
        height: int,
        width: int,
        num_bands: int, 
        channel_start: int, 
        channel_end: int, 
        n_channels: int,
        num_classes: int,
        theta_alpha: float = 80.0,
        theta_beta: float = 0.0625,
        theta_gamma: float = 3.0,
        bilateral_compat: float = 10.0,
        spatial_compat: float = 3.0,
        num_iterations: int = 10,
        name=None,
    ):
        super().__init__(name)

        self.height = tf.constant(height, dtype=tf.int32)
        self.width = tf.constant(width, dtype=tf.int32)
        self.num_bands = tf.constant(num_bands, dtype=tf.int32)
        self.channel_start = tf.constant(channel_start, dtype=tf.int32)
        self.channel_end = tf.constant(channel_end, dtype=tf.int32)
        self.n_channels = tf.constant(n_channels, dtype=tf.int32)
        self.num_classes = tf.constant(num_classes, dtype=tf.int32)

        self.theta_alpha = tf.constant(theta_alpha, dtype=tf.float32)
        self.theta_beta = tf.constant(theta_beta, dtype=tf.float32)
        self.theta_gamma = tf.constant(theta_gamma, dtype=tf.float32)

        self.bilateral_compat = tf.constant(bilateral_compat, dtype=tf.float32)
        self.spatial_compat = tf.constant(spatial_compat, dtype=tf.float32)
        self.compatibility = tf.constant(-1, dtype=tf.float32)
        self.num_iterations = tf.constant(num_iterations, dtype=tf.int32)

        # # Non-critical parameter
        # self.bilateral_range_padding = tf.constant(2, dtype=tf.int32)
        # self.bilateral_space_padding = tf.constant(2, dtype=tf.int32)
        # self.spatial_space_padding = tf.constant(2, dtype=tf.int32)
        # self.n_iters = tf.constant(2, dtype=tf.int32)  # conv iteration in the filters
