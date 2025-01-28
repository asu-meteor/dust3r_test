import json
import numpy as np
import cv2 

def matrix_to_euler_and_quaternion(matrix):
    # Extract rotation matrix (top-left 3x3)
    rotation_matrix = matrix[:3, :3]
    
    # Extract translation vector (last column, except the last row)
    tvec = matrix[:3, 3]
    
    # Convert rotation matrix to Euler angles (in radians)
    sy = np.sqrt(rotation_matrix[0, 0]**2 + rotation_matrix[1, 0]**2)
    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        y = np.arctan2(-rotation_matrix[2, 0], sy)
        z = np.arctan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    else:
        x = np.arctan2(-rotation_matrix[1, 2], rotation_matrix[1, 1])
        y = np.arctan2(-rotation_matrix[2, 0], sy)
        z = 0

    # Convert radians to degrees
    euler_angles_deg = np.degrees([x, y, z])
    
    # Convert rotation matrix to quaternion
    q_w = np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2]) / 2
    q_x = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / (4 * q_w)
    q_y = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / (4 * q_w)
    q_z = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / (4 * q_w)
    quaternion = [q_x, q_y, q_z, q_w]  # Unity uses [x, y, z, w] order

    return tvec, euler_angles_deg, quaternion

# Load json data
with open ('output.json') as f:
    data = json.load(f)

matrices = data['extrinsics']

# Convert to 4x4 matrices
results = []
for matrix in matrices:
    transformation_matrix = np.array(matrix)
    tvec, euler_angles, quaternion = matrix_to_euler_and_quaternion(transformation_matrix)

    results.append({
        'tvec': tvec.tolist(),
        'euler_angles': euler_angles.tolist(),
        'quaternion': quaternion
    })

# Save to json file
with open('output_euler_quaternion.json', 'w') as f:
    json.dump(results, f, indent=4)
    print('Saved to output_euler_quaternion.json')