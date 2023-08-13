# machine-learning-image-registration-UHF-MRI

Image artefacts caused by subject motion are one of the dominant issues restricting image quality for ultrahigh field magnetic resonance imaging (MRI). Motion correction of MRI head scans has been achieved to an
extent through the FatNav approach. The FatNav approach takes multiple low-resolution images, called
navigators, across the high-resolution host sequence. Host images are realigned retrospectively (after
acquisition) using motion parameters between navigators. Motion parameters are extracted through classical
image registration, a technique that takes two images of the same object and calculates the transform between
them. All motion related artefacts cannot be avoided due to the correction taking place retrospectively. Rapid
growth in machine learning over the past two decades invites the development of a learning-based image
registration technique. Such a technique may provide both increased registration speed whilst achieving
comparable or improved accuracy over the classical method. A rapid, robust, learning-based technique could
allow the FatNav approach to be implemented prospectively (during acquisition), giving potential for
improved motion correction. Synthetic datasets composed of FatNav-like head images were generated for use
in both classical and learning-based registration methods. Classical registration was tested using the
framework SimpleITK to give a reference point for speed and accuracy. Learning-based image registration
was developed using a pre-built network from Project MONAI, a learning-based framework for various
workflows in healthcare. Training and testing of this network was predominantly completed in 2D. The
network was accurate in y translation and rotation parameters but not so in x translation. Computation was
faster than classical registration by two orders of magnitude. Learning-based image registration in 3D was
also developed and tested, showing encouraging results but with accuracy at this stage far from what is
required. These results demonstrate the potential for developing a rapid, robust, learning-based 3D image
registration method for implementation in the FatNav approach.
