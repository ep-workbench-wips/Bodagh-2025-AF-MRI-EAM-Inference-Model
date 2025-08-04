import numpy as np
import openep

"""
Bodagh 2025 AF-MRI-EAM Inference Model

Predicts an atrial fibrillation catheter ablation outcome using mean left atrial bipolar voltage, 
magnetic resonance imaging-derived left atrial ejection fraction and patient clinical parameters 
(age, hypertension, weight).

This model is for demonstration only and is not intended for clinical use.

NOTE:
    Set DEBUG=False for running in EP Workbench and DEBUG=True if run locally.
"""

DEBUG = False

if DEBUG:
    # If running locally DEBUG=true, then manually change the inputs here:
    DEBUG = True
    case = openep.load_openep_mat('path/to/file.openep')
    voltage = case.fields.bipolar_voltage
    age_at_ablation = 60
    atrial_ef = 45
    is_hypertension = True
    weight = 65
else:
    # If run within EP Workbench software's WIP environment
    # The arguments are pulled from the widget.json
    case = cases[case_1]

def init_data():
    """
    Initializes the feature data and model coefficients for prediction.

    Returns:
        tuple:
            data (dict): Feature values required for prediction, including:
                - 'Meanvoltage' (float): Mean bipolar voltage.
                - 'Age_at_ablation' (float): Age at ablation.
                - 'aef' (float): Atrial ejection fraction.
                - 'hypertension' (int): Hypertension status (0 = no, 1 = yes).
                - 'weight' (float): Patient weight in kilograms.
            coefficients (dict): Linear model coefficients, including the intercept
                and weights for each feature.
    """
    voltage = case.fields.bipolar_voltage
    hypertension = int(is_hypertension)

    data = {
        'Meanvoltage': np.nanmean(voltage),
        'Age_at_ablation': age_at_ablation,
        'aef': atrial_ef,
        'hypertension': hypertension,
        'weight': weight
    }

    coefficients = {
        'Intercept': 4.017039,
        'aef': -0.015067,
        'hypertension': 0.596453,
        'Age_at_ablation': -0.032148,
        'Meanvoltage': -0.865168,
        'weight': -0.009764
    }
    return data, coefficients

def predict_outcome(data, coefficients):
    """
    Calculates the predicted outcome score using patient and voltage features with
    a predefined linear model.

    Parameters:
        data (dict): Dictionary containing the following keys:
            - 'aef' (float): Atrial ejection fraction.
            - 'hypertension' (int): Hypertension status (0 = no, 1 = yes).
            - 'Age_at_ablation' (float): Patient age at the time of ablation.
            - 'Meanvoltage' (float): Mean bipolar voltage from EP mapping.
            - 'weight' (float): Patient weight in kilograms.

        coefficients (dict): Linear model coefficients, including:
            - 'Intercept' (float)
            - Coefficients for each feature matching the keys in `data`.

    Returns:
        float: Predicted outcome score based on the linear model.
    """
    # Start with intercept
    prediction = np.full(1, coefficients['Intercept'])

    # Add each variable's contribution
    for variable, coef in coefficients.items():
        if variable != 'Intercept':
            prediction += coef * data[variable]

    return prediction

def main():
    data, coefficients = init_data()
    prediction = predict_outcome(data, coefficients)
    print(prediction)

if __name__ == '__main__':
    main()