from flow.utils import load_nii
from flow.co_registration import reorient_image
from flow.normalization import normalize_image
from flow.brain_extraction import extract_brain
import os

reference_image_path = '../paciente_pre_procesado/UPENN-GBM-00001_11_T1.nii' # temporal reference for reorientation
input_image_path = '../paciente_no_pre_procesado/UPENN-GBM-00096_11_T1_unstripped.nii'
output_path = './outputs'

reference_nifti_image = load_nii(reference_image_path)
input_nifti_image = load_nii(input_image_path)

reoriented_nifti_image = reorient_image(reference_nifti_image, input_nifti_image)
normalized_nifti_image = normalize_image(reoriented_nifti_image)

# save the reoriented and normalized image to a temporary folder
temp_output_path = os.path.join(output_path, 'temp.nii')
normalized_nifti_image.to_filename(temp_output_path)

print(f"Saving reoriented and normalized image to {temp_output_path}")