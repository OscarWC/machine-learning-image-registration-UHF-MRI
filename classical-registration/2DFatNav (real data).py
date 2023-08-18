import SimpleITK as sitk
import os
import numpy as np
import timeit
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from IPython.display import clear_output

#number of images (not including the 'fixed' 000 image) + 1
n = 11
#data set
m = 33

#0
OUTPUT_DIR = 'folder1'

#timeit
start = timeit.default_timer()

#LOOP FROM HERE

for i in range(1,n):

    #2 Read Images

    fixed_image =  sitk.ReadImage(f"fatnavData/fn_{m}/000_fatNavRecon.png", sitk.sitkFloat32)
    moving_image = sitk.ReadImage(f"fatnavData/fn_{m}/00{i}_fatNavRecon.png", sitk.sitkFloat32)

    #interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));
    #3 Initial Alignment

    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                        moving_image,
                                                        sitk.Euler2DTransform(),
                                                        sitk.CenteredTransformInitializerFilter.GEOMETRY)

    moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]-1), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    #4 Registration - plotting the similarty metric's value

    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    registration_method.SetMetricAsMeanSquares()
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)

    # Interpolator settings.
    registration_method.SetInterpolator(sitk.sitkLinear)

    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()

    # Setup for the multi-resolution framework. In this attempt I'm not using this.
    #registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
    #registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
    #registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)

    """"# Connect all of the observers so that we can perform plotting during registration.
    registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
    registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
    registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations)
    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))
    """

    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                sitk.Cast(moving_image, sitk.sitkFloat32))

    #5 Post Registration Analysis

    #The metric value allows us to compare multiple registration runs as there is a probabilistic aspect to our registration, we are using random sampling to estimate the similarity metric.
    #Optimizer: This will help you understand whether termination is too early, either due to thresholds being too tight, early termination due to small number of iterations - numberOfIterations, or too loose, early termination due to large value for minimal change in similarity measure - convergenceMinimumValue)

    #print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

    #Now visually

    #moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2] - 1), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    #Now trying to get motion parameters out

    translation_parameters = final_transform.GetParameters()
    #comes out as [r, tx, ty]?
    print(translation_parameters)

    text_file = open(f"fatnavData/fn_{m}/reg_00{i}.txt", "a")
    #rotations kept in radians
    a = translation_parameters[0]
    #translation parameters
    b = translation_parameters[1]
    c = translation_parameters[2]

    #text_file.write('\n')

    text_file.write(f'rotation={a}\n')

    text_file.write(f'x translation={b}\n')
    text_file.write(f'y translation={c}\n')

    text_file.close()

stop = timeit.default_timer()

print('Time: ', stop - start)