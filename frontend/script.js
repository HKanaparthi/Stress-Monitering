// Configuration
const API_BASE_URL = 'http://localhost:5001';

// DOM Elements - will be initialized after DOM loads
let assessmentSection, resultsSection, loadingOverlay, form, retakeBtn;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM elements
    assessmentSection = document.getElementById('assessment-section');
    resultsSection = document.getElementById('results-section');
    loadingOverlay = document.getElementById('loading-overlay');
    form = document.getElementById('stress-assessment-form');
    retakeBtn = document.getElementById('retake-assessment');

    // Force hide loading overlay on startup using both methods
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
        loadingOverlay.style.display = 'none';
        console.log('✅ Loading overlay forcibly hidden');
    }

    // Ensure assessment section is visible
    if (assessmentSection) {
        assessmentSection.classList.remove('hidden');
    }

    // Ensure results section is hidden
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }

    initializeRangeSliders();
    initializeEventListeners();

    console.log('🎉 Student Stress Monitor loaded successfully! Backend should be running on port 5001');
});

// Initialize range sliders with dynamic value display
function initializeRangeSliders() {
    const rangeInputs = document.querySelectorAll('input[type="range"]');

    rangeInputs.forEach(input => {
        const valueDisplay = input.nextElementSibling;

        // Update display when value changes
        input.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
        });

        // Set initial value
        valueDisplay.textContent = input.value;
    });
}

// Initialize event listeners
function initializeEventListeners() {
    // Form submission
    if (form) {
        form.addEventListener('submit', handleFormSubmission);
    } else {
        console.error('Form element not found!');
    }

    // Retake assessment button
    if (retakeBtn) {
        retakeBtn.addEventListener('click', function() {
            showAssessmentForm();
            if (form) form.reset();
            initializeRangeSliders(); // Reset slider displays
        });
    }
}

// Handle form submission
async function handleFormSubmission(e) {
    e.preventDefault();

    // Show loading
    showLoading();

    try {
        // Collect form data
        const formData = collectFormData();

        // Validate data
        if (!validateFormData(formData)) {
            throw new Error('Please fill in all required fields');
        }

        // Send prediction request
        const result = await sendPredictionRequest(formData);

        // Display results
        displayResults(result);

        // Show results section
        showResults();

    } catch (error) {
        console.error('Error:', error);
        let errorMessage = 'An error occurred while processing your assessment.';

        if (error.message.includes('fetch')) {
            errorMessage += ' Please make sure the backend server is running on port 5001.';
        }

        alert(errorMessage + ' Check the console for details.');
    } finally {
        hideLoading();
    }
}

// Collect form data
function collectFormData() {
    const formData = new FormData(form);
    const data = {};

    // Convert form data to object with proper data types
    for (let [key, value] of formData.entries()) {
        data[key] = parseInt(value);
    }

    return data;
}

// Validate form data
function validateFormData(data) {
    const requiredFields = [
        'anxiety_level', 'self_esteem', 'mental_health_history', 'depression',
        'headache', 'blood_pressure', 'sleep_quality', 'breathing_problem',
        'noise_level', 'living_conditions', 'safety', 'basic_needs',
        'academic_performance', 'study_load', 'teacher_student_relationship',
        'future_career_concerns', 'social_support', 'peer_pressure',
        'extracurricular_activities', 'bullying'
    ];

    return requiredFields.every(field => data.hasOwnProperty(field) && data[field] !== null);
}

// Send prediction request to API
async function sendPredictionRequest(data) {
    const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get prediction');
    }

    return await response.json();
}

// Display results
function displayResults(result) {
    // Update stress level indicator
    updateStressIndicator(result);

    // Display contributing factors
    displayContributingFactors(result.contributing_factors);

    // Display recommendations
    displayRecommendations(result.recommendations);
}

// Update stress level indicator
function updateStressIndicator(result) {
    const indicator = document.getElementById('stress-indicator');
    const label = document.getElementById('stress-label');
    const confidence = document.getElementById('stress-confidence');

    // Update text
    label.textContent = result.stress_label;
    confidence.textContent = `Confidence: ${result.confidence}%`;

    // Update styling based on stress level
    const stressLevel = result.stress_level;
    indicator.className = 'stress-indicator';

    if (stressLevel === 0) {
        indicator.classList.add('low-stress');
    } else if (stressLevel === 1) {
        indicator.classList.add('moderate-stress');
    } else {
        indicator.classList.add('high-stress');
    }
}

// Display contributing factors
function displayContributingFactors(factors) {
    const container = document.getElementById('contributing-factors');
    container.innerHTML = '';

    factors.forEach(factor => {
        const factorElement = createFactorElement(factor);
        container.appendChild(factorElement);
    });
}

// Create factor element
function createFactorElement(factor) {
    const div = document.createElement('div');
    div.className = 'factor-item';

    div.innerHTML = `
        <h4>${factor.factor}</h4>
        <p>Current level: ${factor.value} | Importance: ${(factor.importance * 100).toFixed(1)}%</p>
    `;

    return div;
}

// Display recommendations
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';

    recommendations.forEach(recommendation => {
        const recElement = createRecommendationElement(recommendation);
        container.appendChild(recElement);
    });
}

// Create recommendation element
function createRecommendationElement(recommendation) {
    const div = document.createElement('div');
    div.className = 'recommendation-item';

    div.innerHTML = `<p><i class="fas fa-check-circle"></i> ${recommendation}</p>`;

    return div;
}

// UI State Management
function showLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.style.display = 'flex';
        console.log('⏳ Loading overlay shown');
    }
}

function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.add('hidden');
        loadingOverlay.style.display = 'none';
        console.log('✅ Loading overlay hidden');
    }
}

function showAssessmentForm() {
    if (assessmentSection) {
        assessmentSection.classList.remove('hidden');
    }
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showResults() {
    if (assessmentSection) {
        assessmentSection.classList.add('hidden');
    }
    if (resultsSection) {
        resultsSection.classList.remove('hidden');
    }

    // Scroll to results
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Health check function (for debugging)
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('API Health:', data);
        return data.status === 'healthy';
    } catch (error) {
        console.error('API Health Check Failed:', error);
        return false;
    }
}

// Health check function available for manual testing
// To test: Open browser console and run checkAPIHealth()