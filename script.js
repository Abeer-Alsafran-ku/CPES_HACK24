let sections = [];

function createSections() {
    const count = document.getElementById('sectionCount').value;
    const errorElement = document.getElementById('sectionCountError');
    
    // Check if input is empty
    if (!count) {
        errorElement.style.display = 'block';
        return;
    }
    
    // Hide error message if input is valid
    errorElement.style.display = 'none';
    
    const parsedCount = parseInt(count);
    if (parsedCount < 1) return;

    const container = document.getElementById('sectionsContainer');
    container.innerHTML = '';
    sections = [];

    for (let i = 0; i < count; i++) {
        const section = document.createElement('div');
        section.className = 'section';
        section.innerHTML = `
            <input type="text" placeholder="Section Title" class="form-control sectionTitle mb-2">
            <input type="number" placeholder="Percentage Weight" class="form-control sectionWeight mb-2" min="0" max="100">
            <input type="number" placeholder="Score" class="form-control sectionScore mb-2" min="0" max="100">
        `;
        container.appendChild(section);
    }

    document.getElementById('calculateBtn').style.display = 'block';
}

function calculateGrade() {
    const sectionElements = document.getElementsByClassName('section');
    const titles = new Set();
    let totalPercentage = 0;
    let totalGrade = 0;

    // Reset errors
    document.getElementById('percentageError').style.display = 'none';
    document.getElementById('titleError').style.display = 'none';
    document.getElementById('scoreError').style.display = 'none';

    // Check for empty score fields
    for (let section of sectionElements) {
        const score = section.querySelector('.sectionScore').value;
        if (!score) {
            alert('Please fill in all score fields before calculating');
            return;
        }
    }

    // Collect and validate data
    for (let section of sectionElements) {
        const title = section.querySelector('.sectionTitle').value;
        const weight = parseFloat(section.querySelector('.sectionWeight').value);
        const score = parseFloat(section.querySelector('.sectionScore').value);

        if (titles.has(title)) {
            document.getElementById('titleError').style.display = 'block';
            return;
        }
        titles.add(title);
        if (score>weight){
            document.getElementById('scoreError').style.display = 'block';
            return;
        }
        totalPercentage += weight;
        // totalGrade += (score * weight / 100);
        totalGrade += (score );
    }

    if (Math.round(totalPercentage) !== 100) {
        document.getElementById('percentageError').style.display = 'block';
        return;
    }

    // Calculate letter grade
    let letterGrade;
    if (totalGrade >= 90) {
        letterGrade = 'A';
    } else if (totalGrade >= 80) {
        letterGrade = 'B';
    } else {
        letterGrade = 'C';
    }

    // Display result
    document.getElementById('result').innerHTML = 
        `Final Grade: ${totalGrade.toFixed(2)}% (${letterGrade})`;
}

function resetCalculator() {
    // Clear the section count input
    document.getElementById('sectionCount').value = '';
    
    // Clear the sections container
    document.getElementById('sectionsContainer').innerHTML = '';
    
    // Hide the calculate button
    document.getElementById('calculateBtn').style.display = 'none';
    
    // Clear the result
    document.getElementById('result').innerHTML = '';
    
    // Hide error messages
    document.getElementById('percentageError').style.display = 'none';
    document.getElementById('titleError').style.display = 'none';
    document.getElementById('scoreError').style.display = 'none';
}