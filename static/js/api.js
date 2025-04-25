const API_BASE_URL = '/api'; // Adjust if your API is hosted elsewhere

async function fetchAPI(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // CSRF token needed for Django
            'X-CSRFToken': getCookie('csrftoken'),
        },
    };

    const config = { ...defaultOptions, ...options };

    if (config.body) {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        if (response.status === 403 || response.status === 401) {
            // Authentication error
            window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
            return null;
        }

        if (!response.ok) {
            // Attempt to parse error details from response body
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) {
                errorData = { detail: response.statusText };
            }
            console.error('API Error:', response.status, errorData);
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        // Handle cases where response might be empty (e.g., DELETE requests)
        if (response.status === 204) {
            return null; // Or return an empty object/success indicator
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch API failed:', error);
        alert(`Error: ${error.message}`); // Basic error feedback
        throw error; // Re-throw to allow caller handling
    }
}

// Function to get CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- Program API Calls ---
const getPrograms = () => fetchAPI('/programs/');
const createProgram = (data) => fetchAPI('/programs/', { method: 'POST', body: data });
const getProgram = (id) => fetchAPI(`/programs/${id}/`);
const updateProgram = (id, data) => fetchAPI(`/programs/${id}/`, { method: 'PATCH', body: data });
const deleteProgram = (id) => fetchAPI(`/programs/${id}/`, { method: 'DELETE' });

// --- Client API Calls ---
const getClients = (searchQuery = '') => {
    const endpoint = searchQuery ? `/clients/?search=${encodeURIComponent(searchQuery)}` : '/clients/';
    return fetchAPI(endpoint);
};
const createClient = (data) => fetchAPI('/clients/', { method: 'POST', body: data });
const getClientProfile = (id) => fetchAPI(`/clients/${id}/profile/`);
const updateClient = (id, data) => fetchAPI(`/clients/${id}/`, { method: 'PATCH', body: data });
const deleteClient = (id) => fetchAPI(`/clients/${id}/`, { method: 'DELETE' });

// --- Enrollment API Calls ---
const enrollClient = (clientId, programId) => fetchAPI(`/clients/${clientId}/enroll/`, { method: 'POST', body: { program_id: programId } });
const getEnrollments = (clientId = null, programId = null) => {
    let endpoint = '/enrollments/';
    const params = new URLSearchParams();
    if (clientId) params.append('client_id', clientId);
    if (programId) params.append('program_id', programId);
    if (params.toString()) endpoint += `?${params.toString()}`;
    return fetchAPI(endpoint);
};
const updateEnrollment = (enrollmentId, data) => fetchAPI(`/enrollments/${enrollmentId}/`, { method: 'PATCH', body: data });
const deleteEnrollment = (enrollmentId) => fetchAPI(`/enrollments/${enrollmentId}/`, { method: 'DELETE' }); 