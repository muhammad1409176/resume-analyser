// ================= CONFIG =================
const API_BASE = 'http://127.0.0.1:5000/api';
let reportData = null;

console.log("=== RESUME ANALYZER INITIALIZED ===");


// ================= MAIN =================
window.analyzeResume = function (event) {
    if (event) event.preventDefault();

    const fileInput = document.getElementById("resumeFile");
    const resultsDiv = document.getElementById("results");

    if (!fileInput.files.length) {
        alert("Select a file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    resultsDiv.innerHTML = "Analyzing...";

    fetch(API_BASE + '/resume/analyze', {
        method: "POST",
        credentials: "include",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = "Error: " + data.error;
                return;
            }
            displayResults(data);
        })
        .catch(() => resultsDiv.innerHTML = "Error occurred");
};


// ================= DISPLAY =================
function displayResults(data) {
    const resultsDiv = document.getElementById("results");

    // store data globally for PDF
    reportData = data;

    const skills = data.detected_skills || [];
    const missing = data.missing_skills || [];
    const strengths = data.strengths || [];
    const weaknesses = data.weaknesses || [];
    const roles = data.recommended_jobs || [];
    const summary = data.summary || "";
    const resumeScore = data.resume_score || 0;

    let html = "";

    // ===== STRENGTH LABEL =====
    let strengthLabel = "";
    let strengthColor = "";

    if (resumeScore >= 80) {
        strengthLabel = "🟢 Strong";
        strengthColor = "#4caf50";
    } else if (resumeScore >= 50) {
        strengthLabel = "🟡 Average";
        strengthColor = "#ff9800";
    } else {
        strengthLabel = "🔴 Needs Improvement";
        strengthColor = "#f44336";
    }

    // ===== SCORE =====
    html += `
    <div class="result-section">
        <h3>📊 Resume Score: ${resumeScore}%</h3>
        <div style="background:#eee; border-radius:10px; overflow:hidden; height:12px;">
            <div style="width:${resumeScore}%; background: linear-gradient(90deg,#667eea,#764ba2); height:100%;"></div>
        </div>
        <p style="font-weight:bold; color:${strengthColor};">${strengthLabel}</p>
    </div>`;

    // ===== TOP SKILLS =====
    const topSkills = skills.slice(0, 3);
    if (topSkills.length) {
        html += `<div class="result-section">
            <h3>🔥 Top Skills</h3>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">`;

        topSkills.forEach(skill => {
            html += `<span style="padding:8px 14px; background:linear-gradient(135deg,#ff9800,#ff5722); color:white; border-radius:20px; font-weight:bold;">
                ${escapeHtml(skill)}
            </span>`;
        });

        html += `</div></div>`;
    }

    // ===== SUMMARY =====
    if (summary) {
        html += `<div class="result-section">
            <h3>🤖 Summary</h3>
            <p>${escapeHtml(summary)}</p>
        </div>`;
    }

    // ===== SKILLS =====
    html += `<div class="result-section"><h3>✔ Skills</h3>`;
    skills.forEach(s => html += `<span class="skill-badge">${escapeHtml(s)}</span>`);
    html += `</div>`;

    // ===== MISSING =====
    html += `<div class="result-section"><h3>⚠ Missing</h3>`;
    missing.forEach(s => html += `<span class="skill-badge">${escapeHtml(s)}</span>`);
    html += `</div>`;

    // ===== STRENGTHS =====
    if (strengths.length) {
        html += `<div class="result-section"><h3>💪 Strengths</h3><ul>`;
        strengths.forEach(s => html += `<li>${escapeHtml(s)}</li>`);
        html += `</ul></div>`;
    }

    // ===== WEAKNESSES =====
    if (weaknesses.length) {
        html += `<div class="result-section"><h3>⚠ Weaknesses</h3><ul>`;
        weaknesses.forEach(s => html += `<li>${escapeHtml(s)}</li>`);
        html += `</ul></div>`;
    }

    // ===== JOBS (LINKEDIN) =====
    if (roles.length) {
        html += `<div class="result-section"><h3>💼 Job Recommendations</h3>`;

        roles.forEach(role => {
            const title = typeof role === "object" ? role.title : role;
            const link = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(title)}`;

            html += `
            <div style="margin:10px 0;">
                <a href="${link}" target="_blank" style="color:#0a66c2; text-decoration:none;">
                    <strong>${escapeHtml(title)}</strong>
                </a>
                <a href="${link}" target="_blank" style="margin-left:10px;">View Jobs</a>
            </div>`;
        });

        html += `</div>`;
    }

    // ===== GRAPH =====
    html += `<div class="result-section">
        <h3>📊 Skill Chart</h3>
        <canvas id="chart"></canvas>
    </div>`;

    // ===== DOWNLOAD BUTTON =====
    html += `
    <div class="result-section" style="text-align:center;">
        <button onclick="downloadReport()" 
            style="padding:12px 20px; background:#667eea; color:white; border:none; border-radius:8px; cursor:pointer;">
            📄 Download Report
        </button>
    </div>`;

    resultsDiv.innerHTML = html;

    // GRAPH
    new Chart(document.getElementById("chart"), {
        type: "bar",
        data: {
            labels: ["Detected", "Missing"],
            datasets: [{
                label: "Skills Analysis",
                data: [skills.length, missing.length]
            }]
        }
    });
}


// ================= PDF DOWNLOAD =================
function downloadReport() {
    if (!reportData) {
        alert("No report data available");
        return;
    }

    if (!window.jspdf) {
        alert("PDF library not loaded");
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let y = 10;

    doc.setFontSize(16);
    doc.text("AI Resume Analysis Report", 10, y);

    y += 10;

    doc.setFontSize(12);
    doc.text(`Score: ${reportData.resume_score}%`, 10, y);
    y += 8;

    doc.text(`Domain: ${reportData.domain}`, 10, y);
    y += 10;

    doc.text("Skills:", 10, y);
    y += 6;
    doc.text((reportData.detected_skills || []).join(", "), 10, y, { maxWidth: 180 });

    y += 10;

    doc.text("Missing Skills:", 10, y);
    y += 6;
    doc.text((reportData.missing_skills || []).join(", "), 10, y, { maxWidth: 180 });

    y += 10;

    doc.text("Strengths:", 10, y);
    y += 6;
    (reportData.strengths || []).forEach(s => {
        doc.text("- " + s, 10, y);
        y += 6;
    });

    y += 4;

    doc.text("Weaknesses:", 10, y);
    y += 6;
    (reportData.weaknesses || []).forEach(w => {
        doc.text("- " + w, 10, y);
        y += 6;
    });

    doc.save("AI_Resume_Report.pdf");
}


// ================= UTIL =================
function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, m => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    })[m]);
}


// ================= LOGOUT =================
function logoutUser() {
    fetch('/api/logout')
        .then(() => window.location.href = "/");
}
document.addEventListener("DOMContentLoaded", () => {
    const name = localStorage.getItem("userName");
    const el = document.getElementById("userNameDisplay");

    if (name && el) {
        el.innerText = "👋 " + name;
    }
});
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");

    // Save preference
    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}
    document.addEventListener("DOMContentLoaded", () => {
    const theme = localStorage.getItem("theme");

    if (theme === "dark") {
        document.body.classList.add("dark-mode");
    }
});
document.getElementById("resumeFile").addEventListener("change", function () {
    const fileName = this.files[0]?.name;

    if (fileName) {
        document.getElementById("fileLabel").innerText = "📁 " + fileName;
    }
});