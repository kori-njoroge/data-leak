// Get references to the password input field and the eye icon
const passwordInput = document.getElementById('password');
const togglePasswordIcon = document.getElementById('togglePassword');

// Function to toggle the visibility of the password
function togglePasswordVisibility() {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        togglePasswordIcon.classList.remove('fa-eye');
        togglePasswordIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        togglePasswordIcon.classList.remove('fa-eye-slash');
        togglePasswordIcon.classList.add('fa-eye');
    }
}

// Add click event listener to the eye icon
togglePasswordIcon.addEventListener('click', togglePasswordVisibility);
