document.addEventListener('DOMContentLoaded', () => {
    // Initial view can be set here if desired, e.g., loadClientsView();
    setupEventListeners();
});

const mainContent = document.getElementById('main-content');
const addProgramModal = new bootstrap.Modal(document.getElementById('addProgramModal'));
const addClientModal = new bootstrap.Modal(document.getElementById('addClientModal'));
const clientProfileModal = new bootstrap.Modal(document.getElementById('clientProfileModal'));
const enrollClientModal = new bootstrap.Modal(document.getElementById('enrollClientModal'));

function setupEventListeners() {
    // Program form submission
    document.getElementById('add-program-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('program-name').value;
        const description = document.getElementById('program-description').value;
        const status = document.getElementById('program-status').value;
        try {
            await createProgram({ name, description, status });
            addProgramModal.hide();
            loadProgramsView(); // Refresh the list
            document.getElementById('add-program-form').reset();
        } catch (error) {
            console.error("Failed to add program:", error);
            // Optionally display an error message to the user
        }
    });

    // Client form submission
    document.getElementById('add-client-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const clientData = {
            first_name: document.getElementById('client-first-name').value,
            last_name: document.getElementById('client-last-name').value,
            date_of_birth: document.getElementById('client-dob').value,
            gender: document.getElementById('client-gender').value,
            phone_number: document.getElementById('client-phone').value,
            email: document.getElementById('client-email').value,
            address: document.getElementById('client-address').value,
        };
        try {
            await createClient(clientData);
            addClientModal.hide();
            loadClientsView(); // Refresh the list
            document.getElementById('add-client-form').reset();
        } catch (error) {
            console.error("Failed to add client:", error);
        }
    });

    // Enrollment form submission
    document.getElementById('enroll-client-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const clientId = document.getElementById('enroll-client-id').value;
        const programId = document.getElementById('enroll-program-id').value;
        try {
            await enrollClient(clientId, programId);
            enrollClientModal.hide();
            // Optionally, refresh the client profile view if it's open
            // Or show a success message
            alert('Client enrolled successfully!');
            // Refresh profile if open
            const openProfileClientId = document.getElementById('client-profile-content')?.dataset.clientId;
            if (openProfileClientId && openProfileClientId === clientId) {
                loadClientProfile(clientId);
            }
        } catch (error) {
            console.error("Failed to enroll client:", error);
            // Error is likely handled by fetchAPI, but specific handling can go here
        }
    });
}

function renderLoading() {
    mainContent.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
}

async function loadProgramsView() {
    renderLoading();
    try {
        const programs = await getPrograms();

        // Count programs by status
        const statusCounts = {
            ACTIVE: 0,
            COMPLETED: 0,
            DISCONTINUED: 0
        };

        programs.forEach(program => {
            if (statusCounts.hasOwnProperty(program.status)) {
                statusCounts[program.status]++;
            }
        });

        let programsHtml = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2>Health Programs</h2>
                <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addProgramModal">+ Add Program</button>
            </div>
            <div class="mb-3">
                <div class="btn-group" role="group" aria-label="Program status filter">
                    <button type="button" class="btn btn-outline-primary active" data-status="all">All Programs <span class="badge bg-primary">${programs.length}</span></button>
                    <button type="button" class="btn btn-outline-success" data-status="ACTIVE">Active <span class="badge bg-success">${statusCounts.ACTIVE}</span></button>
                    <button type="button" class="btn btn-outline-info" data-status="COMPLETED">Completed <span class="badge bg-info">${statusCounts.COMPLETED}</span></button>
                    <button type="button" class="btn btn-outline-secondary" data-status="DISCONTINUED">Discontinued <span class="badge bg-secondary">${statusCounts.DISCONTINUED}</span></button>
                </div>
            </div>
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" id="programs-list">
        `;

        if (programs.length === 0) {
            programsHtml += '<div class="col"><div class="alert alert-info">No programs found.</div></div>';
        } else {
            programs.forEach(program => {
                // Add data-status attribute for filtering and use card layout for better presentation
                programsHtml += `
                    <div class="col" data-status="${program.status}">
                        <div class="card h-100 border-${getBorderClass(program.status)}">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">${program.name}</h5>
                                <span class="badge ${getBadgeClass(program.status)}">${getStatusLabel(program.status)}</span>
                            </div>
                            <div class="card-body">
                                <p class="card-text">${program.description}</p>
                            </div>
                            <div class="card-footer">
                                <small class="text-muted">Created: ${new Date(program.created_at).toLocaleDateString()}</small>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        programsHtml += '</div>';
        mainContent.innerHTML = programsHtml;

        // Add event listeners for status filter buttons
        document.querySelectorAll('.btn-group[aria-label="Program status filter"] button').forEach(button => {
            button.addEventListener('click', function () {
                // Toggle active class
                document.querySelectorAll('.btn-group[aria-label="Program status filter"] button').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');

                // Filter programs
                const status = this.getAttribute('data-status');
                const programItems = document.querySelectorAll('#programs-list > div');

                // Show/hide based on filter and update count
                let visibleCount = 0;
                programItems.forEach(item => {
                    if (status === 'all' || item.getAttribute('data-status') === status) {
                        item.style.display = '';
                        visibleCount++;
                    } else {
                        item.style.display = 'none';
                    }
                });

                // Show message if no results
                const noResultsElem = document.getElementById('no-filter-results');
                if (visibleCount === 0 && !noResultsElem) {
                    const alert = document.createElement('div');
                    alert.id = 'no-filter-results';
                    alert.className = 'col-12 mt-3';
                    alert.innerHTML = `<div class="alert alert-info">No ${status === 'all' ? '' : status.toLowerCase()} programs found.</div>`;
                    document.getElementById('programs-list').appendChild(alert);
                } else if (visibleCount > 0 && noResultsElem) {
                    noResultsElem.remove();
                }
            });
        });

    } catch (error) {
        mainContent.innerHTML = '<div class="alert alert-danger">Failed to load programs.</div>';
    }
}

// Helper function to get appropriate badge class based on status
function getBadgeClass(status) {
    switch (status) {
        case 'ACTIVE':
            return 'bg-success';
        case 'COMPLETED':
            return 'bg-info';
        case 'DISCONTINUED':
            return 'bg-secondary';
        default:
            return 'bg-primary';
    }
}

// Helper function to get border class for cards
function getBorderClass(status) {
    switch (status) {
        case 'ACTIVE':
            return 'success';
        case 'COMPLETED':
            return 'info';
        case 'DISCONTINUED':
            return 'secondary';
        default:
            return 'primary';
    }
}

// Helper function to get user-friendly status label
function getStatusLabel(status) {
    switch (status) {
        case 'ACTIVE':
            return 'Active';
        case 'COMPLETED':
            return 'Completed';
        case 'DISCONTINUED':
            return 'Discontinued';
        default:
            return status;
    }
}

async function loadClientsView(searchQuery = '') {
    renderLoading();
    try {
        const clients = await getClients(searchQuery);
        let clientsHtml = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2>Clients</h2>
                <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#addClientModal">+ Register Client</button>
            </div>
            <div class="input-group mb-3">
                <input type="text" id="client-search-input" class="form-control" placeholder="Search by name, phone, or email" value="${searchQuery}">
                <button class="btn btn-outline-secondary" type="button" id="client-search-button">Search</button>
            </div>
             <div class="list-group">
        `;
        if (clients.length === 0) {
            clientsHtml += '<div class="list-group-item">No clients found.</div>';
        } else {
            clients.forEach(client => {
                clientsHtml += `
                    <a href="#" class="list-group-item list-group-item-action client-card" onclick="loadClientProfile(${client.id})">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${client.first_name} ${client.last_name}</h5>
                            <small>ID: ${client.id}</small>
                        </div>
                        <p class="mb-1">DOB: ${client.date_of_birth}</p>
                        <small>Phone: ${client.phone_number || 'N/A'}</small>
                    </a>
                `;
            });
        }
        clientsHtml += '</div>';
        mainContent.innerHTML = clientsHtml;

        // Add event listener for the search button *after* it's added to the DOM
        document.getElementById('client-search-button').addEventListener('click', () => {
            const query = document.getElementById('client-search-input').value;
            loadClientsView(query);
        });
        // Add event listener for Enter key in search input
        document.getElementById('client-search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const query = document.getElementById('client-search-input').value;
                loadClientsView(query);
            }
        });

    } catch (error) {
        mainContent.innerHTML = '<div class="alert alert-danger">Failed to load clients.</div>';
    }
}

async function loadClientProfile(clientId) {
    const profileContent = document.getElementById('client-profile-content');
    profileContent.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>'; // Loading state
    profileContent.dataset.clientId = clientId; // Store client ID for potential refresh
    clientProfileModal.show();

    try {
        const client = await getClientProfile(clientId);
        const allPrograms = await getPrograms(); // Fetch all programs for enrollment dropdown

        let profileHtml = `
            <h4>${client.first_name} ${client.last_name} <small class="text-muted">(ID: ${client.id})</small></h4>
            <hr>
            <p><strong>Date of Birth:</strong> ${client.date_of_birth} (Age: ${client.age})</p>
            <p><strong>Gender:</strong> ${client.gender}</p>
            <p><strong>Phone:</strong> ${client.phone_number || 'N/A'}</p>
            <p><strong>Email:</strong> ${client.email || 'N/A'}</p>
            <p><strong>Address:</strong> ${client.address}</p>
            <p><strong>Registered On:</strong> ${new Date(client.registration_date).toLocaleString()}</p>
            <hr>
            <h5>Enrollments</h5>
        `;

        if (client.enrollments && client.enrollments.length > 0) {
            profileHtml += '<ul class="list-group list-group-flush">';
            client.enrollments.forEach(enrollment => {
                profileHtml += `
                    <li class="list-group-item">
                        <strong>${enrollment.program_name}</strong> (${enrollment.status})
                        <br>
                        <small>Enrolled: ${new Date(enrollment.enrollment_date).toLocaleDateString()}</small>
                        ${enrollment.notes ? `<br><small>Notes: ${enrollment.notes}</small>` : ''}
                        <!-- Add options to update/remove enrollment later -->
                    </li>
                `;
            });
            profileHtml += '</ul>';
        } else {
            profileHtml += '<p>Not enrolled in any programs.</p>';
        }

        // Only show the enroll button if there are active programs available
        const activePrograms = allPrograms.filter(p => p.status === 'ACTIVE');
        if (activePrograms.length > 0) {
            profileHtml += `
                <hr>
                <button class="btn btn-primary btn-sm" onclick="openEnrollmentModal(${client.id})">Enroll in New Program</button>
            `;
        } else {
            profileHtml += `
                <hr>
                <p class="text-muted">No active programs available for enrollment.</p>
            `;
        }

        profileContent.innerHTML = profileHtml;

        // Populate enrollment modal dropdown with only ACTIVE programs
        const enrollSelect = document.getElementById('enroll-program-id');
        enrollSelect.innerHTML = '<option selected disabled value="">Choose...</option>'; // Reset
        const enrolledProgramIds = client.enrollments.map(e => e.program);

        // Filter for active programs that the client is not already enrolled in
        activePrograms
            .filter(program => !enrolledProgramIds.includes(program.id))
            .forEach(program => {
                const option = document.createElement('option');
                option.value = program.id;
                option.textContent = program.name;
                enrollSelect.appendChild(option);
            });

        document.getElementById('enroll-client-id').value = clientId;
    } catch (error) {
        profileContent.innerHTML = '<div class="alert alert-danger">Failed to load client profile.</div>';
    }
}

function openEnrollmentModal(clientId) {
    // Ensure the client profile modal is closed if it's the trigger
    // clientProfileModal.hide(); // May not be needed depending on UX preference

    // The programs should have been populated when the profile was loaded
    // If called from somewhere else, might need to populate programs here
    document.getElementById('enroll-client-id').value = clientId;
    enrollClientModal.show();
} 