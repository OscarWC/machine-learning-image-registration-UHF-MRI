import SimpleITK as sitk
import os
import numpy as np
import timeit
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from IPython.display import clear_output

#number of images + 1
n = 101
#0
OUTPUT_DIR = 'folder1'

#timeit
start = timeit.default_timer()

#1 Utility Functions

# Callback invoked by the interact IPython method for scrolling through the image stacks of
# the two images (moving and fixed).
def display_images(fixed_image_z, moving_image_z, fixed_npa, moving_npa):
    # Create a figure with two subplots and the specified size.
    plt.subplots(1, 2, figsize=(10, 8))

    # Draw the fixed image in the first subplot.
    plt.subplot(1, 2, 1)
    plt.imshow(fixed_npa[fixed_image_z, :, :], cmap=plt.cm.Greys_r);
    plt.title('fixed image')
    plt.axis('off')

    # Draw the moving image in the second subplot.
    plt.subplot(1, 2, 2)
    plt.imshow(moving_npa[moving_image_z, :, :], cmap=plt.cm.Greys_r);
    plt.title('moving image')
    plt.axis('off')
    #plt.show()
    #plt.savefig('folder1/ImagesSideBySide')
    plt.close()


# Callback invoked by the IPython interact method for scrolling and modifying the alpha blending
# of an image stack of two images that occupy the same physical space.
def display_images_with_alpha(image_z, alpha, fixed, moving):
    img = (1.0 - alpha) * fixed[:, :, image_z] + alpha * moving[:, :, image_z]
    plt.imshow(sitk.GetArrayViewFromImage(img), cmap=plt.cm.Greys_r);
    plt.axis('off')
    #plt.show()
    #plt.savefig('folder1/ImagesOverlayed')
    plt.close()

# Callback invoked when the StartEvent happens, sets up our new data.
def start_plot():
    global metric_values, multires_iterations

    metric_values = []
    multires_iterations = []


# Callback invoked when the EndEvent happens, do cleanup of data and figure.
def end_plot():
    global metric_values, multires_iterations

    del metric_values
    del multires_iterations
    # Close figure, we don't want to get a duplicate of the plot latter on.
    plt.close()


# Callback invoked when the IterationEvent happens, update our data and display new figure.
def plot_values(registration_method):
    global metric_values, multires_iterations

    metric_values.append(registration_method.GetMetricValue())
    # Clear the output area (wait=True, to reduce flickering), and plot current data
    clear_output(wait=True)
    # Plot the similarity metric values
    plt.plot(metric_values, 'r')
    plt.plot(multires_iterations, [metric_values[index] for index in multires_iterations], 'b*')
    plt.xlabel('Iteration Number', fontsize=12)
    plt.ylabel('Metric Value', fontsize=12)
    plt.savefig('folder1/iteration_metricvalue1.1.png')


# Callback invoked when the sitkMultiResolutionIterationEvent happens, update the index into the
# metric_values list.
def update_multires_iterations():
    global metric_values, multires_iterations
    multires_iterations.append(len(metric_values))

#LOOP FROM HERE - top of the range is the same number (n) as i < n in the ImageJ generation loop - augmented images and modified parameters all in folder2

for i in range(1,n):

    #2 Read Images
    #MAKE SURE TO CHECK LABELS WHEN RE RUNNING
    fixed_image =  sitk.ReadImage("headmeshdilatedscaled1.2.tif", sitk.sitkFloat32)
    moving_image = sitk.ReadImage(f"folder2/00{i}_rt.tif", sitk.sitkFloat32)

    interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));
    #3 Initial Alignment

    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                        moving_image,
                                                        sitk.Euler3DTransform(),
                                                        sitk.CenteredTransformInitializerFilter.GEOMETRY)

    moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

    interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]-1), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));

    #4 Registration - plotting the similarty metric's value

    registration_method = sitk.ImageRegistrationMethod()

    # Similarity metric settings.
    #registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
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

    # Connect all of the observers so that we can perform plotting during registration.
    registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
    registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
    registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations)
    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))

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

    translation_parameters = final_transform.GetParameters() #RotX, RotY, RotZ, ShiftX, shiftY, shiftZ

    #comes out as [rx, ry, rz, tx, ty, tz] according to docs
    #print(translation_parameters)

    text_file = open(f"folder2/00{i}_augments.txt", "a")

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
    text_file.write(f'x rotation reg={b}\n')
    text_file.write(f'x translation reg={e}\n')

    text_file.write(f'y rotation reg={a}\n')
    text_file.write(f'y translation reg={d}\n')

    text_file.write(f'z rotation reg={c}\n')
    text_file.write(f'z translation reg={f}\n')

    text_file.close()

    #rename to show modification

    os.renames(f"folder2/00{i}_augments.txt", f"folder2/00{i}_augments_reg.txt")

stop = timeit.default_timer()

print('Time: ', stop - start)