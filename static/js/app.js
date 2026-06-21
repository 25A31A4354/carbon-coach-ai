/**
 * CarbonCoach AI - App Controller
 * Manages assessment wizard navigation, backend analysis API requests, 
 * radial progress animations, and dynamic SVG simulation rendering.
 */

/**
 * Application Constants
 * @constant
 * @type {Object}
 */
const CONFIG = {
    TOTAL_STEPS: 4,
    RADIAL_CIRCUMFERENCE: 314,
    RADIAL_SPEED_MS: 15,
    CHART_WIDTH: 400,
    CHART_HEIGHT: 220,
    CHART_BOTTOM: 160,
    MAX_BAR_HEIGHT: 125,
    REQUIRED_CATEGORIES: ['transport', 'food', 'energy', 'shopping']
};

document.addEventListener('DOMContentLoaded', () => {
    // App State
    let currentStep = 1;
    const answers = {
        transport: 'walking',
        food: 'mixed',
        energy: 'ac_under_2',
        shopping: 'rarely'
    };

    // DOM Elements
    const views = {
        landing: document.getElementById('landing-view'),
        assessment: document.getElementById('assessment-view'),
        results: document.getElementById('results-view')
    };

    // Buttons
    const btnStart = document.getElementById('btn-start');
    const btnNext = document.getElementById('btn-next');
    const btnPrev = document.getElementById('btn-prev');
    const btnReset = document.getElementById('btn-reset');
    const btnAcceptMission = document.getElementById('btn-accept-mission');

    // Wizard components
    const stepNumText = document.getElementById('current-step-num');
    const progressBarFill = document.querySelector('.progress-bar-fill');
    const errorBanner = document.getElementById('error-banner');

    // Results components
    const leakTitle = document.getElementById('leak-title');
    const leakNameEl = document.getElementById('leak-name-inline');
    const leakExplanation = document.getElementById('leak-explanation');
    const impactPercentText = document.getElementById('impact-percent');
    const radialBar = document.getElementById('radial-bar');
    const missionDescription = document.getElementById('mission-description');
    const missionMotivation = document.getElementById('mission-motivation');
    const missionCard = document.getElementById('mission-card');
    const missionCheckbox = document.getElementById('mission-checkbox');
    const overallCurrentScoreText = document.getElementById('overall-current-score');
    const overallFutureScoreText = document.getElementById('overall-future-score');
    const severityText = document.getElementById('impact-severity-text');
    const severityFill = document.getElementById('impact-severity-fill');
    const successMessageBlock = document.querySelector('.success-message');
    
    // Cached Results DOM nodes for efficiency
    const pOppEl = document.getElementById('persona-opportunity-text');
    const savingsCarbonImpactEl = document.getElementById('savings-carbon-impact');
    const savingsDifficultyEl = document.getElementById('savings-difficulty');
    const savingsAmountEl = document.getElementById('savings-amount');
    const missionReasoningEl = document.getElementById('mission-reasoning');
    const personaName = document.getElementById('persona-name');
    const personaDesc = document.getElementById('persona-desc');
    const currentPatternText = document.getElementById('current-pattern-text');
    const futureInsightEl = document.getElementById('future-insight');
    const streakCountEl = document.getElementById('streak-count');
    const missionsCompletedEl = document.getElementById('missions-completed');

    // Initialize Event Listeners
    initEventListeners();

    /**
     * Bind all necessary event listeners on page load
     */
    function initEventListeners() {
        btnStart.addEventListener('click', () => switchView('assessment'));
        btnPrev.addEventListener('click', handlePrev);
        btnNext.addEventListener('click', handleNext);
        btnReset.addEventListener('click', handleReset);
        btnAcceptMission.addEventListener('click', handleAcceptMission);
        missionCheckbox.addEventListener('click', handleAcceptMission);

        // Watch radio inputs to capture answers in real-time
        document.querySelectorAll('.option-card input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                const category = e.target.name;
                answers[category] = e.target.value;
            });
        });
    }

    /**
     * Switch between major application views.
     * @param {string} targetViewId - The ID mapping for the view (landing, assessment, results).
     */
    function switchView(targetViewId) {
        Object.keys(views).forEach(key => {
            views[key].classList.remove('active');
        });
        
        const targetView = views[targetViewId];
        if (targetView) {
            targetView.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    /**
     * Advance wizard to next step or trigger submission if on the final step.
     */
    function handleNext() {
        if (currentStep < CONFIG.TOTAL_STEPS) {
            document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.remove('active');
            currentStep++;
            document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.add('active');
            updateWizardProgress();
        } else {
            submitAssessment();
        }
    }

    /**
     * Move wizard back to previous step.
     */
    function handlePrev() {
        if (currentStep > 1) {
            document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.remove('active');
            currentStep--;
            document.querySelector(`.wizard-step[data-step="${currentStep}"]`).classList.add('active');
            updateWizardProgress();
        }
    }

    /**
     * Update progress indicators, UI text, and button states in the wizard.
     */
    function updateWizardProgress() {
        const percentage = (currentStep / CONFIG.TOTAL_STEPS) * 100;
        progressBarFill.style.width = `${percentage}%`;
        stepNumText.textContent = currentStep;
        
        if (currentStep === 1) {
            btnPrev.classList.add('disabled');
            btnPrev.setAttribute('disabled', 'true');
        } else {
            btnPrev.classList.remove('disabled');
            btnPrev.removeAttribute('disabled');
        }
        
        btnNext.textContent = currentStep === CONFIG.TOTAL_STEPS ? 'View Blueprint' : 'Next';
    }

    /**
     * Reset the application state and return to the beginning of the assessment.
     */
    function handleReset() {
        currentStep = 1;
        localStorage.removeItem('carbonCoach_missionAccepted');
        
        missionCard.classList.remove('mission-complete');
        missionCheckbox.classList.remove('active');
        btnAcceptMission.style.display = 'block';
        successMessageBlock.style.display = 'none';
        
        document.querySelectorAll('.wizard-step').forEach(step => {
            step.classList.remove('active');
            const defaultRadio = step.querySelector('input[type="radio"]:checked') || step.querySelector('input[type="radio"]');
            if (defaultRadio) {
                defaultRadio.checked = true;
                answers[defaultRadio.name] = defaultRadio.value;
            }
        });
        
        document.querySelector('.wizard-step[data-step="1"]').classList.add('active');
        updateWizardProgress();
        switchView('assessment');
    }

    /**
     * Validates that all required fields are filled out in the answers payload.
     * @param {Object} data The answer payload to check.
     * @returns {boolean} True if payload is valid, false otherwise.
     */
    function validatePayload(data) {
        return CONFIG.REQUIRED_CATEGORIES.every(category => data.hasOwnProperty(category) && typeof data[category] === 'string');
    }

    /**
     * Orchestrates assessment submission, network requests, validation, and transition to dashboard.
     */
    async function submitAssessment() {
        if (!validatePayload(answers)) {
            console.error('Validation failed: Missing or invalid inputs.');
            showErrorBanner('Invalid submission. Please complete all fields.');
            return;
        }

        try {
            if (errorBanner) errorBanner.style.display = 'none';
            setButtonLoadingState(btnNext, true);
            
            const result = await fetchAssessmentResult(answers);
            renderResults(result);
            switchView('results');
        } catch (error) {
            console.error('Error analyzing responses:', error);
            showErrorBanner('Failed to analyze data. Please try again.');
        } finally {
            setButtonLoadingState(btnNext, false);
        }
    }

    /**
     * Sends the collected user answers to the analysis API.
     * @param {Object} payload Payload dictionary to POST.
     * @returns {Promise<Object>} API response json.
     * @throws Will throw error if network fails or API returns non-OK response.
     */
    async function fetchAssessmentResult(payload) {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`API request failed with status: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * Sets button state for loading (disables button and adds dot animation).
     * @param {HTMLElement} btn The button element.
     * @param {boolean} isLoading True to set loading state, false to remove it.
     */
    function setButtonLoadingState(btn, isLoading) {
        if (isLoading) {
            btn.classList.add('disabled');
            btn.innerHTML = 'Analyzing... <span class="badge-dot" style="animation: pulse 1s infinite"></span>';
        } else {
            btn.classList.remove('disabled');
            btn.textContent = 'View Blueprint';
        }
    }

    /**
     * Helper to show the error banner cleanly.
     * @param {string} msg Text to display in the banner.
     */
    function showErrorBanner(msg) {
        if (errorBanner) {
            errorBanner.textContent = msg;
            errorBanner.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }

    /**
     * Populates the Results Dashboard with backend simulation data.
     * @param {Object} data Application analysis response data.
     */
    function renderResults(data) {
        if (leakNameEl) leakNameEl.textContent = data.leak_name || 'General';
        
        if (data.persona) {
            if (personaName) personaName.textContent = data.persona.name || 'Conscious Consumer';
            if (personaDesc) personaDesc.textContent = data.persona.description || '';
            if (pOppEl) pOppEl.textContent = data.persona.opportunity || '';
        }
        
        // Savings Impact Engine updates
        if (savingsCarbonImpactEl && data.impact_severity) {
            savingsCarbonImpactEl.textContent = data.impact_severity;
        }
        if (savingsDifficultyEl && data.difficulty_level) {
            savingsDifficultyEl.textContent = data.difficulty_level;
        }
        if (savingsAmountEl && data.estimated_savings) {
            savingsAmountEl.textContent = data.estimated_savings;
        }
        
        if (missionReasoningEl && data.mission_reasoning) {
            missionReasoningEl.textContent = data.mission_reasoning;
        }

        leakTitle.textContent = data.leak_name || 'Your Biggest Carbon Leak';
        leakExplanation.textContent = data.reason || 'We identified key areas where emissions are high.';
        missionDescription.textContent = data.weekly_mission || 'Implement the recommended changes.';
        
        if (missionMotivation) {
            missionMotivation.textContent = data.motivation || 'Small changes add up to global impact.';
        }
        
        if (severityText && severityFill) {
            const severity = data.impact_severity || 'Low';
            severityText.textContent = severity;
            severityText.className = 'severity-' + severity.toLowerCase();
            const widthPct = severity === 'High' ? '100%' : severity === 'Medium' ? '60%' : '30%';
            
            // Avoid reflow by using requestAnimationFrame
            requestAnimationFrame(() => {
                severityFill.style.width = '0%';
                requestAnimationFrame(() => {
                    severityFill.style.width = widthPct;
                });
            });
        }
        
        if (data.simulation) {
            if (overallCurrentScoreText) overallCurrentScoreText.textContent = data.simulation.total_current;
            if (overallFutureScoreText) overallFutureScoreText.textContent = data.simulation.total_future;
            
            if (currentPatternText) {
                currentPatternText.textContent = (data.impact_severity === 'High' ? 'High impact pattern' : data.impact_severity === 'Medium' ? 'Moderate impact pattern' : 'Low impact pattern');
            }
        }
        
        if (futureInsightEl && data.future_insight) {
            futureInsightEl.textContent = data.future_insight;
        }
        
        animateImpactPercent(data.impact_pct || 0);
        
        if (localStorage.getItem('carbonCoach_missionAccepted') === 'true') {
            applyMissionAcceptedState();
        }
        
        updateStreakUI();
    }

    /**
     * Animates the percentage counter for the impact reduction.
     * @param {number} targetPercentage Final percentage mapping.
     */
    function animateImpactPercent(targetPercentage) {
        let count = 0;
        if (!impactPercentText) return;
        
        const counterInterval = setInterval(() => {
            if (count >= targetPercentage) {
                clearInterval(counterInterval);
            } else {
                count++;
                impactPercentText.textContent = `${count}%`;
            }
        }, CONFIG.RADIAL_SPEED_MS);
    }

    /**
     * User Action: Accept the Weekly Mission. 
     * Saves user intent to localStorage to persist completed state.
     */
    function handleAcceptMission() {
        if (localStorage.getItem('carbonCoach_missionAccepted') === 'true') return;
        
        localStorage.setItem('carbonCoach_missionAccepted', 'true');
        
        // Streak Logic update
        let today = new Date().toISOString().split('T')[0];
        let lastDate = localStorage.getItem('carbonCoach_lastMissionDate');
        
        if (lastDate !== today) {
            let streak = parseInt(localStorage.getItem('carbonCoach_streak')) || 0;
            let missions = parseInt(localStorage.getItem('carbonCoach_missions')) || 0;
            
            let yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
            if (lastDate && lastDate !== yesterday) {
                streak = 1; // reset
            } else {
                streak += 1; // increment
            }
            missions += 1;
            
            localStorage.setItem('carbonCoach_streak', streak);
            localStorage.setItem('carbonCoach_missions', missions);
            localStorage.setItem('carbonCoach_lastMissionDate', today);
            
            updateStreakUI();
        }

        applyMissionAcceptedState();
    }
    
    function updateStreakUI() {
        if (streakCountEl) {
            streakCountEl.textContent = parseInt(localStorage.getItem('carbonCoach_streak')) || 0;
        }
        if (missionsCompletedEl) {
            missionsCompletedEl.textContent = parseInt(localStorage.getItem('carbonCoach_missions')) || 0;
        }
    }

    /**
     * Update UI nodes to reflect that the mission has been accepted.
     */
    function applyMissionAcceptedState() {
        missionCheckbox.classList.add('active');
        missionCard.classList.add('mission-complete');
        btnAcceptMission.style.display = 'none';
        successMessageBlock.style.display = 'block';
        successMessageBlock.classList.add('animate-slide-up');
    }
});
