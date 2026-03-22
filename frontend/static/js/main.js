// Tab Navigation
        function switchTab(tabId) {
            if (tabId === 'dashboard') {
                document.getElementById('view-dashboard').style.display = 'block';
                document.getElementById('view-checkurl').style.display = 'none';
                document.getElementById('tab-dashboard').classList.add('active');
                document.getElementById('tab-checkurl').classList.remove('active');
            } else {
                document.getElementById('view-dashboard').style.display = 'none';
                document.getElementById('view-checkurl').style.display = 'flex';
                document.getElementById('tab-checkurl').classList.add('active');
                document.getElementById('tab-dashboard').classList.remove('active');
            }
        }

        // URL Prediction Logic
        function checkUrl() {
            const urlInput = document.getElementById('urlInput').value.trim();
            if(!urlInput) {
                alert("Please enter a valid URL, e.g., https://example.com");
                return;
            }
            
            const btn = document.getElementById('checkBtn');
            const resultBox = document.getElementById('urlResult');
            const resultReasons = document.getElementById('resultReasons');
            
            btn.innerText = "Checking...";
            btn.disabled = true;
            resultBox.style.display = "none";
            document.getElementById('urlFeaturesContainer').style.display = "none";
            resultReasons.innerHTML = "";

            fetch('/api/v1/predict_url', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ url: urlInput })
            })
            .then(res => res.json())
            .then(data => {
                btn.innerText = "Check Now";
                btn.disabled = false;
                resultBox.style.display = "block";
                
                if(data.status === "error") {
                    document.getElementById('resultIcon').innerText = "⚠️";
                    document.getElementById('resultText').innerText = "Missing Models";
                    document.getElementById('resultText').style.color = "var(--danger-red)";
                    let errorMessage = document.createElement("li");
                    errorMessage.innerText = "The Machine Learning models have not been trained yet! Please go to Recruiter Mode and click 'Run Complete Pipeline' first.";
                    resultReasons.appendChild(errorMessage);
                    return;
                }

                if(data.prediction === "Legitimate") {
                    document.getElementById('resultIcon').innerText = "✅";
                    document.getElementById('resultText').innerText = "Safe Website";
                    document.getElementById('resultText').style.color = "var(--success-green)";
                } else {
                    document.getElementById('resultIcon').innerText = "❌";
                    document.getElementById('resultText').innerText = "Phishing Detected";
                    document.getElementById('resultText').style.color = "var(--danger-red)";
                }

                if(data.reasons && data.reasons.length > 0) {
                    data.reasons.forEach(reason => {
                        let li = document.createElement("li");
                        li.innerText = reason;
                        li.style.marginBottom = "4px";
                        resultReasons.appendChild(li);
                    });
                } else {
                    let li = document.createElement("li");
                    li.innerText = "Error analyzing components.";
                    resultReasons.appendChild(li);
                }

                if (data.features) {
                    const featuresContainer = document.getElementById('urlFeaturesContainer');
                    const featuresTableDiv = document.getElementById('urlFeaturesTable');
                    
                    let html = '<table><thead><tr><th>Feature Name</th><th>Value</th><th>Justification</th></tr></thead><tbody>';
                    
                    for (const [key, val] of Object.entries(data.features)) {
                        let badgeClass = '';
                        let textReason = 'Neutral / Informational';
                        
                        if (val === -1) {
                            badgeClass = 'background: #ffebee; color: #c62828; padding: 2px 6px; border-radius: 4px;';
                            textReason = 'Phishing Indicator / Suspicious';
                        } else if (val === 1) {
                            badgeClass = 'background: #e8f5e9; color: #2e7d32; padding: 2px 6px; border-radius: 4px;';
                            textReason = 'Safe / Standard Property';
                        } else {
                            badgeClass = 'background: #f5f5f5; color: #616161; padding: 2px 6px; border-radius: 4px;';
                        }
                        
                        html += `<tr>
                                    <td><strong>${key}</strong></td>
                                    <td><span style="${badgeClass}; min-width: 25px; display: inline-block; text-align: center;">${val}</span></td>
                                    <td style="color: var(--text-muted);">${textReason}</td>
                                 </tr>`;
                    }
                    
                    html += '</tbody></table>';
                    featuresTableDiv.innerHTML = html;
                    featuresContainer.style.display = "block";
                }
            })
            .catch(err => {
                btn.innerText = "Check Now";
                btn.disabled = false;
                resultBox.style.display = "block";
                document.getElementById('resultIcon').innerText = "⚠️";
                document.getElementById('resultText').innerText = "Server Error";
                document.getElementById('resultText').style.color = "var(--text-muted)";
                resultReasons.innerHTML = "<li>Could not connect to the Prediction API. Is app.py running?</li>";
            });
        }

        // Modal Logic
        let trainingTimer;
        let isTraining = false;
        let isTrained = false;
        let trainingStartTime = null;

        function closeModal(id) {
            document.getElementById(id).style.display = 'none';
        }

        function runPipeline() {
            const modal = document.getElementById('trainModal');
            modal.style.display = 'flex';
            
            if (isTraining) {
                document.getElementById('trainStatus').innerText = 'Model training is already running in the background. Please wait...';
                let currentSeconds = Math.floor((Date.now() - trainingStartTime) / 1000);
                document.getElementById('trainTimer').innerText = `Time Elapsed: ${currentSeconds}s`;
                return;
            }
            
            if (isTrained) {
                return; // Already finished training in this session, keep the success modal.
            }

            isTraining = true;
            isTrained = false;
            trainingStartTime = Date.now();
            
            document.getElementById('trainSpinner').style.display = 'block';
            document.getElementById('trainTitle').innerText = 'Training Models...';
            document.getElementById('trainStatus').innerText = 'Please wait while the ML pipeline trains on the local dataset. This could take a few moments.';
            document.getElementById('trainStatus').style.color = 'var(--text-main)';
            document.getElementById('btnTestNew').style.display = 'none';

            document.getElementById('trainTimer').innerText = `Time Elapsed: 0s`;
            
            trainingTimer = setInterval(() => {
                let currentSeconds = Math.floor((Date.now() - trainingStartTime) / 1000);
                document.getElementById('trainTimer').innerText = `Time Elapsed: ${currentSeconds}s`;
            }, 1000);

            // Trigger the backend API
            fetch('/api/v1/train')
                .then(response => {
                    isTraining = false;
                    clearInterval(trainingTimer);
                    document.getElementById('trainSpinner').style.display = 'none';
                    if (response.ok) {
                        isTrained = true;
                        document.getElementById('trainTitle').innerText = '✅ Training Complete!';
                        document.getElementById('trainStatus').innerText = 'All machine learning models have been successfully trained on the dataset!';
                        document.getElementById('trainStatus').style.color = 'var(--success-green)';
                        document.getElementById('btnTestNew').style.display = 'block';

                        const modelsBreakdown = document.getElementById('modelsBreakdown');
                        modelsBreakdown.style.filter = 'none';
                        modelsBreakdown.style.opacity = '1';
                        modelsBreakdown.style.pointerEvents = 'auto';
                        modelsBreakdown.style.userSelect = 'auto';
                    } else {
                        document.getElementById('trainTitle').innerText = '❌ Training Failed';
                        document.getElementById('trainStatus').innerText = 'An error occurred during the pipeline execution.';
                        document.getElementById('trainStatus').style.color = 'var(--danger-red)';
                    }
                })
                .catch(err => {
                    isTraining = false;
                    clearInterval(trainingTimer);
                    document.getElementById('trainSpinner').style.display = 'none';
                    document.getElementById('trainTitle').innerText = '❌ Network Error';
                    document.getElementById('trainStatus').innerText = 'Could not contact the server.';
                    document.getElementById('trainStatus').style.color = 'var(--danger-red)';
                });
        }

        function openPredictModal() {
            closeModal('trainModal');
            document.getElementById('predictModal').style.display = 'flex';
            document.getElementById('predictResult').innerHTML = '';
            document.getElementById('predictForm').reset();
        }

        function submitPrediction(e) {
            e.preventDefault();
            const resultDiv = document.getElementById('predictResult');
            resultDiv.innerHTML = '<div class="spinner"></div><p style="text-align:center;">Processing data through models...</p>';
            
            let formData = new FormData(document.getElementById('predictForm'));
            fetch('/api/v1/predict', { method: 'POST', body: formData })
                .then(res => {
                    const contentType = res.headers.get("content-type");
                    if (contentType && contentType.indexOf("application/json") !== -1) {
                        return res.json().then(data => {
                            if (data.status === 'error') {
                                resultDiv.innerHTML = `<div style="text-align:center; padding: 1rem; background: #fafafa; border-radius: var(--radius-sm); border: 1px solid var(--border-light);"><span style="font-size:2.5rem;">⚠️</span><h3 style="color:var(--danger-red); margin: 0.5rem 0;">Models Not Trained</h3><p style="color:var(--text-muted); font-size: 0.95rem;">Please close this modal and click <strong>"Run Complete Pipeline"</strong> first.</p></div>`;
                            } else {
                                resultDiv.innerHTML = `<p>${JSON.stringify(data)}</p>`;
                            }
                        });
                    } else {
                        return res.text().then(html => {
                            if (html.includes('<table')) {
                                resultDiv.innerHTML = '<h3 style="margin-bottom: 1rem;">Prediction Results:</h3><div class="table-wrap">' + html + '</div>';
                            } else {
                                resultDiv.innerHTML = html;
                            }
                        });
                    }
                })
                .catch(err => {
                    resultDiv.innerHTML = '<p style="color:var(--danger-red); text-align:center;">Error processing prediction. Please check your connection.</p>';
                });
        }



        // Table Filtering Logic
        function filterFeatures() {
            let input = document.getElementById("featureSearch");
            let filter = input.value.toLowerCase();
            let table = document.getElementById("featureTable");
            let tr = table.getElementsByTagName("tr");

            for (let i = 1; i < tr.length; i++) {
                let tdName = tr[i].getElementsByTagName("td")[0];
                let tdDesc = tr[i].getElementsByTagName("td")[1];
                if (tdName || tdDesc) {
                    let txtValue = (tdName.textContent || tdName.innerText) + " " + (tdDesc.textContent || tdDesc.innerText);
                    if (txtValue.toLowerCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }

        // Initialize Chart.js
        document.addEventListener('DOMContentLoaded', function() {
            Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
            Chart.defaults.color = '#86868b';

            // 1. Model Accuracy Chart
            const ctxAccuracy = document.getElementById('accuracyChart').getContext('2d');
            new Chart(ctxAccuracy, {
                type: 'bar',
                data: {
                    labels: ['Random Forest', 'Gradient Boosting', 'AdaBoost', 'Decision Tree', 'KNN', 'Logistic Regression'],
                    datasets: [{
                        label: 'Accuracy (%)',
                        data: [97.3, 96.8, 95.4, 94.2, 93.9, 92.7],
                        backgroundColor: [
                            '#0071e3', '#4facfe', '#88c5f7', '#aod8f7', '#c0e0f7', '#e1effa'
                        ],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(29, 29, 31, 0.9)',
                            padding: 12,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) { return context.raw + '%'; }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            min: 85,
                            max: 100,
                            grid: { color: '#f5f5f7' },
                            border: { display: false }
                        },
                        x: {
                            grid: { display: false },
                            border: { display: false }
                        }
                    }
                }
            });

            // 2. Feature Importance Chart
            const ctxImportance = document.getElementById('importanceChart').getContext('2d');
            new Chart(ctxImportance, {
                type: 'bar',
                data: {
                    labels: ['ssl_state', 'url_of_anchor', 'web_traffic', 'prefix_suffix', 'links_in_tags'],
                    datasets: [{
                        label: 'Relative Importance',
                        data: [0.35, 0.28, 0.15, 0.12, 0.08],
                        backgroundColor: '#34c759',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(29, 29, 31, 0.9)'
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            grid: { color: '#f5f5f7' },
                            border: { display: false }
                        },
                        y: {
                            grid: { display: false },
                            border: { display: false }
                        }
                    }
                }
            });
        });