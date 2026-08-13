/* =====================================================
   ICT DEVICE MANAGEMENT SYSTEM
   scripts.js

   Frontend:
   home.html

   Backend:
   Flask

   Registration endpoint:
   /api/auth/register
   ===================================================== */


/* =====================================================
   FLASK API URL
   ===================================================== */

const API_URL = "http://127.0.0.1:5000";


/* =====================================================
   USER REGISTRATION
   ===================================================== */

async function register() {

    /* -----------------------------------------
       GET VALUES FROM home.html
       ----------------------------------------- */

    const fullName =
        document.getElementById(
            "registerFullName"
        ).value.trim();


    const phone =
        document.getElementById(
            "registerPhone"
        ).value.trim();


    const email =
        document.getElementById(
            "registerEmail"
        ).value.trim();


    const password =
        document.getElementById(
            "registerPassword"
        ).value;


    const confirmPassword =
        document.getElementById(
            "confirmPassword"
        ).value;


    /* -----------------------------------------
       CHECK EMPTY FIELDS
       ----------------------------------------- */

    if (
        fullName === "" ||
        phone === "" ||
        email === "" ||
        password === "" ||
        confirmPassword === ""
    ) {

        alert(
            "Please fill in all registration fields."
        );

        return;
    }


    /* -----------------------------------------
       CHECK EMAIL
       ----------------------------------------- */

    const emailPattern =
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailPattern.test(email)) {

        alert(
            "Please enter a valid email address."
        );

        return;
    }


    /* -----------------------------------------
       CHECK PASSWORD LENGTH
       ----------------------------------------- */

    if (password.length < 6) {

        alert(
            "Password must be at least 6 characters."
        );

        return;
    }


    /* -----------------------------------------
       CHECK PASSWORD CONFIRMATION
       ----------------------------------------- */

    if (password !== confirmPassword) {

        alert(
            "Password and Confirm Password do not match."
        );

        return;
    }


    /* -----------------------------------------
       SEND DATA TO FLASK
       ----------------------------------------- */

    try {

        const response = await fetch(
            `${API_URL}/api/auth/register`,
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    full_name: fullName,

                    phone: phone,

                    email: email,

                    password: password

                })

            }
        );


        /* -----------------------------------------
           GET FLASK RESPONSE
           ----------------------------------------- */

        const data =
            await response.json();


        /* -----------------------------------------
           REGISTRATION SUCCESS
           ----------------------------------------- */

        if (response.ok && data.success) {

            alert(
                "Registration successful!"
            );


            /*
             * Save basic user information temporarily.
             * This will help us identify the logged-in
             * user on the next step.
             */

            localStorage.setItem(
                "user_id",
                data.user_id
            );

            localStorage.setItem(
                "user_full_name",
                fullName
            );

            localStorage.setItem(
                "user_email",
                email
            );


            /* -------------------------------------
               GO TO INDEX.HTML
               ------------------------------------- */

            window.location.href =
                "index.html";

        }

        /* -----------------------------------------
           REGISTRATION FAILED
           ----------------------------------------- */

        else {

            alert(
                data.message ||
                "Registration failed."
            );

        }


    } catch (error) {

        console.error(
            "Registration error:",
            error
        );


        alert(
            "Unable to connect to the server. " +
            "Please make sure Flask is running."
        );

    }

}