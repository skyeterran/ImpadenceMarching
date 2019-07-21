# ImpedenceMarching
Impedence Marching is a technique for measuring/storing the impact of a translucent volume's density on the amplitude of light passing through it.

As proof of concept, the script included takes a grayscale density map (named Heightmap.png, but this can be changed) and emulates directional light passing through the image as if it were a volume of varying density. It does this 4 times (top -> bottom, right -> left, bottom -> top, left -> right) and stores the resulting "impedence maps" as 4 grayscale images and one channel-packed RGBA image.

Hypothetically, you could use this technique to bake various directional shadowmaps into a volumetric texture so that you can shade the volume without performing costly realtime raymarching.

This technique is inspired by raymarching and voxel-based global illumination techniques, specifically in the context of volumes such as fog, smoke or clouds.
