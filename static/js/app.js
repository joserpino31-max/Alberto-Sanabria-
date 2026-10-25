// JavaScript utilities for Escuela Alberto Sanabria Staff Management System

document.addEventListener('DOMContentLoaded', function () {
    initCourseRepeater();
    initYearsCalculator();
    initConfirmations();
});

// Dynamic course addition and removal
function initCourseRepeater() {
    const addBtn = document.getElementById('addCourseBtn');
    const container = document.getElementById('coursesContainer');
    const noCoursesMsg = document.getElementById('noCoursesMessage');

    if (!addBtn || !container) return;

    addBtn.addEventListener('click', function () {
        if (noCoursesMsg) {
            noCoursesMsg.style.display = 'none';
        }

        const template = document.getElementById('courseRowTemplate');
        if (!template) return;

        const clone = template.content.cloneNode(true);
        container.appendChild(clone);
        updateCourseIndices();
    });

    // Event delegation for deleting course cards
    container.addEventListener('click', function (e) {
        const removeBtn = e.target.closest('.remove-course-btn');
        if (removeBtn) {
            const courseCard = removeBtn.closest('.course-card');
            if (courseCard) {
                courseCard.remove();
                updateCourseIndices();

                const remaining = container.querySelectorAll('.course-card');
                if (remaining.length === 0 && noCoursesMsg) {
                    noCoursesMsg.style.display = 'block';
                }
            }
        }
    });
}

function updateCourseIndices() {
    const container = document.getElementById('coursesContainer');
    if (!container) return;
    const cards = container.querySelectorAll('.course-card');
    cards.forEach((card, idx) => {
        const numberSpan = card.querySelector('.course-index');
        if (numberSpan) {
            numberSpan.textContent = `#${idx + 1}`;
        }
    });
}

// Calculate and show years of service live when date changes
function initYearsCalculator() {
    const mppeInput = document.getElementById('mppe_entry_date');
    const badgeSpan = document.getElementById('yearsBadge');

    if (mppeInput && badgeSpan) {
        function calculate() {
            const val = mppeInput.value;
            if (!val) {
                badgeSpan.textContent = '';
                return;
            }
            const parts = val.split('-');
            if (parts.length === 3) {
                const entry = new Date(parts[0], parts[1] - 1, parts[2]);
                const now = new Date();
                let years = now.getFullYear() - entry.getFullYear();
                const m = now.getMonth() - entry.getMonth();
                if (m < 0 || (m === 0 && now.getDate() < entry.getDate())) {
                    years--;
                }
                if (years >= 0) {
                    badgeSpan.textContent = `(${years} años de servicio)`;
                }
            }
        }

        mppeInput.addEventListener('change', calculate);
        mppeInput.addEventListener('input', calculate);
        calculate(); // initial calculation
    }
}

// Delete confirmation modal / prompt
function initConfirmations() {
    document.querySelectorAll('.delete-confirm-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            const name = this.getAttribute('data-name') || 'este registro';
            if (!confirm(`¿Está seguro de que desea eliminar a "${name}"?\nEsta acción no se puede deshacer y borrará también sus cursos registrados.`)) {
                e.preventDefault();
            }
        });
    });
}
