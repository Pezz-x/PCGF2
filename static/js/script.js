// DARK MODE TOGGLE
let darkmode = localStorage.getItem('darkmode')
const themeSwitch = document.getElementById('theme-switch')

const enableDarkmode = () => {
    document.body.classList.add('darkmode')
    localStorage.setItem('darkmode', 'active')
}

const disableDarkmode = () => {
    document.body.classList.remove('darkmode')
    localStorage.setItem('darkmode', 'null')
}

if(darkmode === "active") enableDarkmode()

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode')
    if(darkmode !== "active") {
        enableDarkmode()
     }
     else{
        disableDarkmode()
     }
})

// LIKE BUTTON AJAX TOGGLE
// Function to get CSRF token from cookie
function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
}

document.addEventListener('DOMContentLoaded', function () {
    // Select all like forms (action contains /like/)
    const likeForms = document.querySelectorAll('form[action*="/like/"]');

    likeForms.forEach(form => {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();

            // Get CSRF token (cookie or hidden input)
            let csrftoken = getCookie('csrftoken');
            if (!csrftoken) {
                const input = form.querySelector('input[name="csrfmiddlewaretoken"]');
                csrftoken = input ? input.value : '';
            }

            try {
                const resp = await fetch(form.action, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    credentials: 'same-origin'
                });

                if (!resp.ok) throw new Error('Network error');
                const data = await resp.json();

                // Update the button text
                const btn = form.querySelector('button');
                if (btn) {
                    const heart = data.liked ? '❤️' : '🤍';
                    btn.innerHTML = `${heart} likes (${data.likes_count})`;
                }

            } catch (err) {
                console.error('Like request failed:', err);
            }
        });
    });
});
