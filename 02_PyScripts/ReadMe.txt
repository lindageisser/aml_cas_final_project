###############################################################################
#                            ReadMe: 02_PyScripts                             #
###############################################################################
Author: L. Geisser
Date:   11/06/2026

X different Jupyter-Notebooks are generated with purpose to

    -   00_kontas2017_ImageMaskVisualization: 
        -------------------------------------
        Display images and masks (labels 0-4) from the data set kontas_2017 and
        computing the overall label 5 (consisting of labels 2-4).

    -   01_kontas2017_DataPreparation:
        ------------------------------
        Generate data set containing the original data from kontas_2017 and 
        augmented versions on pixel- or patch-basis.
        Quantification of the data set: cloud coverage per image and label
        distribution.
        Store final data set! (Important: Has to be run before all other
        following Jupyter-Notebooks!)

    -   02_kontas2017_RandomForest_Pixel_Hand:
        --------------------------------------
        Load prepared data set and compute hand-crafted features per pixel.
        Train a random forest for pixel-wise classification. 

    -   03_kontas2017_RandomForest_Patch_Hand:
        --------------------------------------
        Load prepared data set and compute hand-crafted features per patch.
        Train a random forest for patch-wise classification. 

    -   04_kontas2017_RandomForest_Patch_AE:
        ------------------------------------
        Load prepared data set and extract features from the latent space
        of a trained convolutional autoencoder per patch.
        Train a random forest for patch-wise classification. 
