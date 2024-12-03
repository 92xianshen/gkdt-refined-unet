"""
Wrapper of Refined UNet. 

tile-wise

2024.12.03: factory built, gkdt v2 included. 
"""
import tensorflow as tf

from .crf_computation import CRFComputation
from .gkdt_refined_unet_config import GKDTRefinedUNetConfig
from .linear2 import Linear2


class GKDTRefinedUNet(tf.Module):
    def __init__(
        self,
        config: GKDTRefinedUNetConfig = None,
        ugenerator_path: str = None,
        name: str = None,
    ):
        super().__init__(name)

        self.config = config
        self.crf_computation = CRFComputation(self.config)
        self.unary_generator = tf.saved_model.load(ugenerator_path)

        self.linear2 = Linear2()

        print("Activate modules...")
        
        self.unary_generator(
            tf.ones(
                shape=[1, self.config.height, self.config.width, self.config.num_bands, ], 
                dtype=tf.float32,
            )
        )
        self.linear2(
            tf.ones(
                shape=[self.config.height, self.config.width, self.config.n_channels], 
                dtype=tf.float32
            )
        )
        self.crf_computation.mean_field_approximation(
            tf.ones(
                shape=[self.config.height, self.config.width, self.config.num_classes],
                dtype=tf.float32,
            ),
            tf.ones(
                shape=[self.config.height, self.config.width, self.config.n_channels], 
                dtype=tf.float32
            ),
        )

        print("Modules activated.")

        # # - For code test
        # mf_unary = tf.ones(
        #     shape=[self.config.height, self.config.width, self.config.num_classes],
        #     dtype=tf.float32,
        # )
        # mf_ref = tf.ones(
        #     [self.config.height, self.config.width, self.config.n_channels], 
        #     dtype=tf.float32, 
        # )
        # print("mf_unary.shape: ", mf_unary.shape)
        # print("mf_ref.shape: ", mf_ref.shape)
        # self.crf_computation.mean_field_approximation(
        #     mf_unary, 
        #     mf_ref, 
        # )
        

    def inference(self, image: tf.Tensor) -> tf.Tensor:
        """
        Predict and refine.

        Args:
            image: 7-band input, [h, w, c], float32.

        Returns:
            rfn: [h, w],
        """

        unary = self.unary_generator(image[tf.newaxis, ...])[0]  # [H, W, N]
        ref = self.linear2(
            image[..., self.config.channel_start:self.config.channel_end:-1]
        )  # [H, W, C]

        rfn = self.crf_computation.mean_field_approximation(
            unary,
            ref,
        )

        return rfn
