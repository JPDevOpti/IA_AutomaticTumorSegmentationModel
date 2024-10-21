import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
from skimage.metrics import structural_similarity as ssim

#Directory root for preprocessed and original images

preprocessed_dir = ''
original_dir = ''

#Load Nifti image format function 
def load_nifti_image(file_path):
    img = nib.load(file_path)
    return img.get_fdata()

#Basic statistics function
def calculate_statistics(image_data):
    mean_intensity = np.mean(image_data)
    std_intensity = np.std(image_data)
    min_intensity = np.min(image_data)
    max_intensity = np.max(image_data)
    
    return mean_intensity, std_intensity, min_intensity, max_intensity

def plot_histogram(image_data, title="Intensities Histogram"):
    plt.hist(image_data.flatten(), bins=100, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel('Intensidad')
    plt.ylabel('Frecuencia')
    plt.show()

#Kolmogorov-Smirnov test to compare distributions.
def ks_test(original_data, preprocessed_data):
    ks_stat, p_value = ks_2samp(original_data.flatten(), preprocessed_data.flatten())
    return ks_stat, p_value

# Smoothing analysis using Fourier transform.
def fourier_analysis(original_data, preprocessed_data):
   # Fourier transform of the original and preprocessed image
    original_fft = np.fft.fftn(original_data)
    preprocessed_fft = np.fft.fftn(preprocessed_data)
    
    
    # Frequency magnitudes
    original_magnitude = np.abs(original_fft)
    preprocessed_magnitude = np.abs(preprocessed_fft)
    
    # Plot the magnitude of the frequencies on a logarithmic scale
    plt.loglog(np.sort(original_magnitude.flatten())[::-1], label='Original')
    plt.loglog(np.sort(preprocessed_magnitude.flatten())[::-1], label='Preprocesada')
    plt.title('Transformada de Fourier - Magnitud de Frecuencias')
    plt.legend()
    plt.show()

# Registry analysis using structural similarity.
def registration_analysis(original_data, preprocessed_data):
    # Normalize the data to avoid problems with different ranges
    original_norm = (original_data - np.min(original_data)) / (np.max(original_data) - np.min(original_data))
    preprocessed_norm = (preprocessed_data - np.min(preprocessed_data)) / (np.max(preprocessed_data) - np.min(preprocessed_data))
    
    # Calculate the structural similarity index (SSIM)
    ssim_index = ssim(original_norm, preprocessed_norm, data_range=preprocessed_norm.max() - preprocessed_norm.min())
    
    return ssim_index

# Initialize lists to store statistical and smoothing/logging results
stats_preprocessed = []
stats_original = []
ks_results = []
ssim_results = []

# Iterate through all the images in the preprocessed image directory
for file_name in os.listdir(preprocessed_dir):
    if file_name.endswith('.nii'):
        # Path to the preprocessed image and its original counterpart
        preprocessed_path = os.path.join(preprocessed_dir, file_name)
        original_path = os.path.join(original_dir, file_name)
        
        # Load the images
        preprocessed_data = load_nifti_image(preprocessed_path)
        original_data = load_nifti_image(original_path)
        
        # Calculate basic statistics
        preprocessed_stats = calculate_statistics(preprocessed_data)
        original_stats = calculate_statistics(original_data)
        
        # Store the statistics
        stats_preprocessed.append(preprocessed_stats)
        stats_original.append(original_stats)
        
        # Perform the Kolmogorov-Smirnov test
        ks_stat, p_value = ks_test(original_data, preprocessed_data)
        ks_results.append((ks_stat, p_value))
        
        # Plot the histogram of the preprocessed image
        plot_histogram(preprocessed_data, title=f'Histogram of {file_name} - Preprocessed')
        
        # Plot the histogram of the original image
        plot_histogram(original_data, title=f'Histogram of {file_name} - Original')
        
        # Smoothing analysis via Fourier
        print(f"Smoothing analysis (Fourier) for {file_name}:")
        fourier_analysis(original_data, preprocessed_data)
        
        # Registration analysis using SSIM
        ssim_index = registration_analysis(original_data, preprocessed_data)
        ssim_results.append(ssim_index)
        print(f"SSIM index for {file_name}: {ssim_index}")
        
        # Display KS test results for each image
        print(f"Image: {file_name}")
        print(f"Preprocessed statistics (Mean, Std. Dev, Min, Max): {preprocessed_stats}")
        print(f"Original statistics (Mean, Std. Dev, Min, Max): {original_stats}")
        print(f"KS test (Statistic, p-value): {ks_stat}, {p_value}\n")

# Global summary
print("### GLOBAL SUMMARY ###")
print("Preprocessed statistics for all images:", stats_preprocessed)
print("Original statistics for all images:", stats_original)
print("KS test results (Statistic, p-value):", ks_results)
print("SSIM indices (Registration):", ssim_results)