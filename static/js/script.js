document.addEventListener('DOMContentLoaded', () => {
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    togglePassword.addEventListener('click', function () {
        // Toggle the type attribute
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
});



// Sign up password
document.addEventListener('DOMContentLoaded', () => {
    const togglePasswords = document.querySelector('#togglePasswords');
    const passwords = document.querySelector('#passwords');

    togglePasswords.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwords.getAttribute('type') === 'password' ? 'text' : 'password';
        passwords.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
});


// Sign up confirm password
document.addEventListener('DOMContentLoaded', () => {
    const togglePasswords = document.querySelector('#togglePasswords1');
    const passwords = document.querySelector('#passwords1');

    togglePasswords.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwords.getAttribute('type') === 'password' ? 'text' : 'password';
        passwords.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
});


// Reset password
document.addEventListener('DOMContentLoaded', () => {
    const togglePasswords = document.querySelector('#togglePasswordr');
    const passwords = document.querySelector('#passwordr');

    togglePasswords.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwords.getAttribute('type') === 'password' ? 'text' : 'password';
        passwords.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
});


// Reset confirm password
document.addEventListener('DOMContentLoaded', () => {
    const togglePasswords = document.querySelector('#togglePasswordr1');
    const passwords = document.querySelector('#passwordr1');

    togglePasswords.addEventListener('click', function () {
        // Toggle the type attribute
        const type = passwords.getAttribute('type') === 'password' ? 'text' : 'password';
        passwords.setAttribute('type', type);

        // Toggle the eye icon (optional)
        this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
    });
});