import SimpleITK as sitk
import os
import numpy as np
import timeit
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from IPython.display import clear_output

#0
OUTPUT_DIR = 'folder1'

#timeit
start = timeit.default_timer()


#LOOP FROM HERE

numbers = [9, 10, 10, 4, 4, 4, 4, 4, 4, 10, 10, 4, 4, 4, 4, 4, 4, 4, 6, 6, 4, 4, 6, 6, 4, 4, 4, 4, 4, 6, 6, 6, 6]

for m in range(1, 34):
    k = m - 1
    for i in range(1, numbers[k] + 1):

        #2 Read Images

        fixed_image =  sitk.ReadImage(f"fatnavData/fn_{m}/000_fatNavRecon.tif", sitk.sitkFloat32)
        moving_image = sitk.ReadImage(f"fatnavData/fn_{m}/00{i}_fatNavRecon.tif", sitk.sitkFloat32)

        #interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));
        #3 Initial Alignment

        initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                            moving_image,
                                                            sitk.Euler3DTransform(),
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

        # Don't optimize in-place, we would possibly like to run this cell multiple times.
        registration_method.SetInitialTransform(initial_transform, inPlace=False)

        final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                    sitk.Cast(moving_image, sitk.sitkFloat32))

        #5 Post Registration Analysis

        #The metric value allows us to compare multiple registration runs as there is a probabilistic aspect to our registration, we are using random sampling to estimate the similarity metric.
        #Optimizer: This will help you understand whether termination is too early, either due to thresholds being too tight, early termination due to small number of iterations - numberOfIterations, or too loose, early termination due to large value for minimal change in similarity measure - convergenceMinimumValue)

        #print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
        #print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))

        #Now visually

        #moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

        #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2] - 1), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

        #Now trying to get motion parameters out

        translation_parameters = final_transform.GetParameters()
        #comes out as [rx, ry, rz, tx, ty, tz] according to docs
        #print(translation_parameters)

        text_file = open(f"fatnavData/fn_{m}/reg_3D_00{i}.txt", "a")

        #convert angles from radians to degrees
        a = translation_parameters[0] * (180/np.pi)
        b = translation_parameters[1] * (180/np.pi)
        c = translation_parameters[2] * (180/np.pi)
        #translation parameters
        d = translation_parameters[3]
        e = translation_parameters[4]
        f = translation_parameters[5]

        text_file.write('\n')
        #now need to assign in the correct MRI orientation (different to SimpleITK) for comparison
        text_file.write(f'x rotation={b}\n')
        text_file.write(f'x translation={e}\n')

        text_file.write(f'y rotation={a}\n')
        text_file.write(f'y translation={d}\n')

        text_file.write(f'z rotation={c}\n')
        text_file.write(f'z translation={f}\n')

        text_file.close()

stop = timeit.default_timer()

print('Time: ', stop - start)