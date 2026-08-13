/* =========================================================
   ICT DEVICES MANAGEMENT SYSTEM
   ADMIN.JS

   Backend:
   Flask

   API:
   http://127.0.0.1:5000/api/admin
========================================================= */


/* =========================================================
   API CONFIGURATION
========================================================= */

const API_URL = "http://127.0.0.1:5000/api";


/* =========================================================
   PAGE LOAD
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    loadAdminData();

});


/* =========================================================
   API HELPER
========================================================= */

async function apiRequest(endpoint, options = {}) {

    try {

        const response = await fetch(
            API_URL + endpoint,
            {
                ...options,

                headers: {
                    "Content-Type": "application/json",
                    ...(options.headers || {})
                }
            }
        );


        const data =
            await response.json().catch(() => ({}));


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Request failed."
            );

        }


        return data;

    }

    catch (error) {

        console.error(
            "API Error:",
            error
        );

        throw error;

    }

}


/* =========================================================
   LOAD ADMIN DATA
========================================================= */

async function loadAdminData() {

    await Promise.allSettled([

        loadStats(),

        loadUsers(),

        loadDevices(),

        loadBorrowings(),

        loadFeedback()

    ]);

}


/* =========================================================
   MODULE NAVIGATION
========================================================= */

function openModule(
    moduleId,
    clickedMenu
) {

    document
        .querySelectorAll(".module")
        .forEach(function (module) {

            module.classList.remove(
                "active"
            );

        });


    const selectedModule =
        document.getElementById(
            moduleId
        );


    if (selectedModule) {

        selectedModule.classList.add(
            "active"
        );

    }


    document
        .querySelectorAll(".menu-item")
        .forEach(function (item) {

            item.classList.remove(
                "active"
            );

        });


    if (clickedMenu) {

        clickedMenu.classList.add(
            "active"
        );

    }


    const titles = {

        dashboard:
            "Admin Dashboard",

        users:
            "Registered Users",

        devices:
            "ICT Devices",

        borrowings:
            "Borrowing Management",

        feedback:
            "User Feedback",

        reports:
            "Reports",

        settings:
            "System Settings"

    };


    const subtitles = {

        dashboard:
            "System overview",

        users:
            "Manage registered users",

        devices:
            "Manage ICT devices",

        borrowings:
            "Monitor device borrowing",

        feedback:
            "Review user feedback",

        reports:
            "System reports and statistics",

        settings:
            "Manage system settings"

    };


    const pageTitle =
        document.getElementById(
            "pageTitle"
        );


    const pageSubtitle =
        document.getElementById(
            "pageSubtitle"
        );


    if (pageTitle) {

        pageTitle.textContent =
            titles[moduleId] || "";

    }


    if (pageSubtitle) {

        pageSubtitle.textContent =
            subtitles[moduleId] || "";

    }


    /* -----------------------------------------
       LOAD MODULE DATA WHEN OPENED
    ----------------------------------------- */

    if (moduleId === "users") {

        loadUsers();

    }


    if (moduleId === "devices") {

        loadDevices();

    }


    if (moduleId === "borrowings") {

        loadBorrowings();

    }


    if (moduleId === "feedback") {

        loadFeedback();

    }


    if (moduleId === "reports") {

        loadReports();

    }

}


/* =========================================================
   DASHBOARD STATISTICS
========================================================= */

async function loadStats() {

    try {

        /*
         * We calculate statistics from the
         * existing backend endpoints.
         *
         * This avoids depending on a missing
         * /admin/stats endpoint.
         */

        const results =
            await Promise.allSettled([

                apiRequest(
                    "/admin/users"
                ),

                apiRequest(
                    "/admin/devices"
                ),

                apiRequest(
                    "/admin/borrowings"
                ),

                apiRequest(
                    "/admin/feedback"
                )

            ]);


        const users =
            results[0].status === "fulfilled"
                ? results[0].value.users || []
                : [];


        const devices =
            results[1].status === "fulfilled"
                ? results[1].value.devices || []
                : [];


        const borrowings =
            results[2].status === "fulfilled"
                ? results[2].value.borrowings || []
                : [];


        const feedback =
            results[3].status === "fulfilled"
                ? results[3].value.feedback || []
                : [];


        /* -----------------------------------------
           TOTAL USERS
        ----------------------------------------- */

        const totalUsers =
            document.getElementById(
                "totalUsers"
            );


        if (totalUsers) {

            totalUsers.textContent =
                users.length;

        }


        /* -----------------------------------------
           TOTAL DEVICES
        ----------------------------------------- */

        const totalDevices =
            document.getElementById(
                "totalDevices"
            );


        if (totalDevices) {

            totalDevices.textContent =
                devices.reduce(
                    function (total, device) {

                        return total +
                            Number(
                                device.total_quantity || 0
                            );

                    },
                    0
                );

        }


        /* -----------------------------------------
           BORROWED DEVICES
        ----------------------------------------- */

        const borrowedDevices =
            document.getElementById(
                "borrowedDevices"
            );


        if (borrowedDevices) {

            const borrowed =
                borrowings
                    .filter(function (item) {

                        return String(
                            item.status || ""
                        ).toLowerCase() ===
                            "borrowed";

                    })
                    .reduce(
                        function (total, item) {

                            return total +
                                Number(
                                    item.quantity || 0
                                );

                        },
                        0
                    );


            borrowedDevices.textContent =
                borrowed;

        }


        /* -----------------------------------------
           TOTAL FEEDBACK
        ----------------------------------------- */

        const totalFeedback =
            document.getElementById(
                "totalFeedback"
            );


        if (totalFeedback) {

            totalFeedback.textContent =
                feedback.length;

        }


        /* -----------------------------------------
           BADGES
        ----------------------------------------- */

        updateBadge(
            "borrowingBadge",
            borrowings.filter(
                function (item) {

                    return String(
                        item.status || ""
                    ).toLowerCase() ===
                        "borrowed";

                }
            ).length
        );


        updateBadge(
            "feedbackBadge",
            feedback.length
        );

    }

    catch (error) {

        console.error(
            "Statistics error:",
            error
        );

    }

}


/* =========================================================
   USERS
========================================================= */

let allUsers = [];


async function loadUsers() {

    try {

        const data =
            await apiRequest(
                "/admin/users"
            );


        allUsers =
            data.users || [];


        renderUsers(
            allUsers
        );


    }

    catch (error) {

        console.error(
            "Loading users failed:",
            error
        );


        const body =
            document.getElementById(
                "usersTableBody"
            );


        if (body) {

            body.innerHTML =
                emptyRow(
                    7,
                    "Unable to load users."
                );

        }

    }

}


/* =========================================================
   RENDER USERS
========================================================= */

function renderUsers(users) {

    const body =
        document.getElementById(
            "usersTableBody"
        );


    if (!body) return;


    if (!users.length) {

        body.innerHTML =
            emptyRow(
                7,
                "No users registered yet."
            );

        return;

    }


    body.innerHTML =
        users.map(function (user) {

            /*
             * IMPORTANT:
             * Backend may return user_id,
             * not id.
             */

            const userId =
                user.user_id ??
                user.id ??
                "";


            return `

                <tr>

                    <td>
                        ${escapeHtml(
                            userId
                        )}
                    </td>


                    <td>
                        ${escapeHtml(
                            user.full_name ??
                            ""
                        )}
                    </td>


                    <td>
                        ${escapeHtml(
                            user.phone ??
                            ""
                        )}
                    </td>


                    <td>
                        ${escapeHtml(
                            user.email ??
                            ""
                        )}
                    </td>


                    <td>
                        ${escapeHtml(
                            user.registered_at ??
                            user.created_at ??
                            ""
                        )}
                    </td>


                    <td>

                        <span
                            class="status active-status"
                        >
                            Active
                        </span>

                    </td>


                    <td>

                        <button
                            type="button"
                            class="view-btn"
                            onclick="viewUser(${Number(userId) || 0})"
                        >
                            View
                        </button>

                    </td>

                </tr>

            `;

        }).join("");

}


/* =========================================================
   SEARCH USERS
========================================================= */

function searchUsers() {

    const input =
        document.getElementById(
            "userSearch"
        );


    if (!input) return;


    const search =
        input.value
            .toLowerCase()
            .trim();


    const filtered =
        allUsers.filter(
            function (user) {

                const text = `

                    ${user.full_name || ""}

                    ${user.email || ""}

                    ${user.phone || ""}

                `.toLowerCase();


                return text.includes(
                    search
                );

            }
        );


    renderUsers(
        filtered
    );

}


/* =========================================================
   VIEW USER
========================================================= */

function viewUser(userId) {

    const user =
        allUsers.find(
            function (item) {

                return Number(
                    item.user_id ??
                    item.id
                ) ===
                    Number(userId);

            }
        );


    if (!user) {

        alert(
            "User information not found."
        );

        return;

    }


    const detailName =
        document.getElementById(
            "detailName"
        );


    const detailPhone =
        document.getElementById(
            "detailPhone"
        );


    const detailEmail =
        document.getElementById(
            "detailEmail"
        );


    const detailDate =
        document.getElementById(
            "detailDate"
        );


    if (detailName) {

        detailName.textContent =
            user.full_name || "-";

    }


    if (detailPhone) {

        detailPhone.textContent =
            user.phone || "-";

    }


    if (detailEmail) {

        detailEmail.textContent =
            user.email || "-";

    }


    if (detailDate) {

        detailDate.textContent =
            user.registered_at ??
            user.created_at ??
            "-";

    }


    const details =
        document.getElementById(
            "userDetails"
        );


    if (details) {

        details.style.display =
            "block";


        details.scrollIntoView({
            behavior: "smooth"
        });

    }

}


/* =========================================================
   CLOSE USER DETAILS
========================================================= */

function closeUserDetails() {

    const details =
        document.getElementById(
            "userDetails"
        );


    if (details) {

        details.style.display =
            "none";

    }

}


/* =========================================================
   DEVICES
========================================================= */

let allDevices = [];


async function loadDevices() {

    try {

        const data =
            await apiRequest(
                "/admin/devices"
            );


        allDevices =
            data.devices || [];


        renderDevices(
            allDevices
        );


    }

    catch (error) {

        console.error(
            "Loading devices failed:",
            error
        );


        const body =
            document.getElementById(
                "devicesTableBody"
            );


        if (body) {

            body.innerHTML =
                emptyRow(
                    7,
                    "Unable to load devices."
                );

        }

    }

}


/* =========================================================
   RENDER DEVICES
========================================================= */

function renderDevices(devices) {

    const body =
        document.getElementById(
            "devicesTableBody"
        );


    if (!body) return;


    if (!devices.length) {

        body.innerHTML =
            emptyRow(
                7,
                "No devices added yet."
            );

        return;

    }


    body.innerHTML =
        devices.map(function (device) {

            const deviceId =
                device.device_id ??
                device.id ??
                "";


            const total =
                Number(
                    device.total_quantity ?? 0
                );


            const available =
                Number(
                    device.available_quantity ?? 0
                );


            const borrowed =
                Math.max(
                    total - available,
                    0
                );


            let status =
                "Available";


            let statusClass =
                "available-status";


            if (available <= 0) {

                status =
                    "Out of Stock";

                statusClass =
                    "out-status";

            }

            else if (
                available <=
                Math.max(
                    1,
                    Math.floor(
                        total * 0.2
                    )
                )
            ) {

                status =
                    "Low Stock";

                statusClass =
                    "low-status";

            }


            return `

                <tr>

                    <td>
                        ${escapeHtml(
                            deviceId
                        )}
                    </td>


                    <td>
                        ${escapeHtml(
                            device.device_name ||
                            ""
                        )}
                    </td>


                    <td>
                        ${total}
                    </td>


                    <td>
                        ${available}
                    </td>


                    <td>
                        ${borrowed}
                    </td>


                    <td>

                        <span
                            class="status ${statusClass}"
                        >
                            ${escapeHtml(status)}
                        </span>

                    </td>


                    <td>

                        <button
                            type="button"
                            class="view-btn"
                            onclick="viewDevice(${Number(deviceId) || 0})"
                        >
                            View
                        </button>

                    </td>

                </tr>

            `;

        }).join("");

}


/* =========================================================
   ADD DEVICE
========================================================= */

function addDevice() {

    const form =
        document.getElementById(
            "addDeviceForm"
        );


    if (form) {

        form.reset();

    }


    const message =
        document.getElementById(
            "deviceFormMessage"
        );


    if (message) {

        message.textContent =
            "";

    }


    const modal =
        document.getElementById(
            "addDeviceModal"
        );


    if (modal) {

        modal.style.display =
            "flex";

    }

}


/* =========================================================
   CLOSE ADD DEVICE
========================================================= */

function closeAddDevice() {

    const modal =
        document.getElementById(
            "addDeviceModal"
        );


    if (modal) {

        modal.style.display =
            "none";

    }

}


/* =========================================================
   SUBMIT ADD DEVICE
========================================================= */

async function submitAddDevice(
    event
) {

    event.preventDefault();


    const message =
        document.getElementById(
            "deviceFormMessage"
        );


    const deviceName =
        document.getElementById(
            "deviceName"
        );


    const deviceTotal =
        document.getElementById(
            "deviceTotal"
        );


    const deviceCategory =
        document.getElementById(
            "deviceCategory"
        );


    const deviceDescription =
        document.getElementById(
            "deviceDescription"
        );


    if (
        !deviceName ||
        !deviceTotal
    ) {

        return;

    }


    const payload = {

        device_name:
            deviceName.value.trim(),

        total_quantity:
            Number(
                deviceTotal.value
            ),

        category:
            deviceCategory
                ? deviceCategory.value.trim()
                : "",

        description:
            deviceDescription
                ? deviceDescription.value.trim()
                : ""

    };


    if (
        !payload.device_name ||
        payload.total_quantity < 1
    ) {

        if (message) {

            message.textContent =
                "Please enter valid device information.";

        }

        return;

    }


    try {

        const data =
            await apiRequest(
                "/admin/devices",
                {
                    method: "POST",

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        if (message) {

            message.textContent =
                data.message ||
                "Device added successfully.";

        }


        await loadDevices();

        await loadStats();


        setTimeout(
            function () {

                closeAddDevice();

            },
            700
        );

    }

    catch (error) {

        if (message) {

            message.textContent =
                error.message;

        }

    }

}


/* =========================================================
   BORROWINGS
========================================================= */

let allBorrowings = [];


async function loadBorrowings() {

    try {

        const data =
            await apiRequest(
                "/admin/borrowings"
            );


        allBorrowings =
            data.borrowings || [];


        renderBorrowings(
            allBorrowings
        );


        const borrowedCount =
            allBorrowings.filter(
                function (item) {

                    return String(
                        item.status || ""
                    ).toLowerCase() ===
                        "borrowed";

                }
            ).length;


        updateBadge(
            "borrowingBadge",
            borrowedCount
        );

    }

    catch (error) {

        console.error(
            "Loading borrowings failed:",
            error
        );


        const body =
            document.getElementById(
                "borrowingsTableBody"
            );


        if (body) {

            body.innerHTML =
                emptyRow(
                    8,
                    "Unable to load borrowing records."
                );

        }

    }

}


/* =========================================================
   RENDER BORROWINGS
========================================================= */

function renderBorrowings(
    borrowings
) {

    const body =
        document.getElementById(
            "borrowingsTableBody"
        );


    if (!body) return;


    if (!borrowings.length) {

        body.innerHTML =
            emptyRow(
                8,
                "No borrowing records yet."
            );

        return;

    }


    body.innerHTML =
        borrowings.map(
            function (item) {

                const borrowingId =
                    item.borrowing_id ??
                    item.borrow_id ??
                    item.id ??
                    "";


                const userName =
                    item.full_name ??
                    item.user ??
                    item.user_name ??
                    "Unknown User";


                const deviceName =
                    item.device_name ??
                    item.device ??
                    "";


                const quantity =
                    item.quantity ??
                    0;


                const borrowDate =
                    item.borrow_date ??
                    item.borrowed_date ??
                    item.date ??
                    "";


                const borrowTime =
                    item.borrow_time ??
                    item.time ??
                    "";


                const status =
                    item.status ||
                    "Borrowed";


                let statusClass =
                    "borrowed-status";


                if (
                    String(status)
                        .toLowerCase() ===
                    "returned"
                ) {

                    statusClass =
                        "returned-status";

                }

                else if (
                    String(status)
                        .toLowerCase() ===
                    "overdue"
                ) {

                    statusClass =
                        "overdue-status";

                }


                return `

                    <tr>

                        <td>
                            ${escapeHtml(
                                borrowingId
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                userName
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                deviceName
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                quantity
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                borrowDate
                            )}
                        </td>


                        <td>
                            ${escapeHtml(
                                borrowTime
                            )}
                        </td>


                        <td>

                            <span
                                class="status ${statusClass}"
                            >
                                ${escapeHtml(
                                    status
                                )}
                            </span>

                        </td>


                        <td>

                            <button
                                type="button"
                                class="view-btn"
                                onclick="viewBorrowing(${Number(borrowingId) || 0})"
                            >
                                View
                            </button>

                        </td>

                    </tr>

                `;

            }
        ).join("");

}


/* =========================================================
   FEEDBACK
========================================================= */

let allFeedback = [];


async function loadFeedback() {

    try {

        const data =
            await apiRequest(
                "/admin/feedback"
            );


        allFeedback =
            data.feedback || [];


        renderFeedback(
            allFeedback
        );


        updateBadge(
            "feedbackBadge",
            allFeedback.length
        );


        const totalFeedback =
            document.getElementById(
                "totalFeedback"
            );


        if (totalFeedback) {

            totalFeedback.textContent =
                allFeedback.length;

        }

    }

    catch (error) {

        console.error(
            "Loading feedback failed:",
            error
        );


        const container =
            document.getElementById(
                "feedbackContainer"
            );


        if (container) {

            container.innerHTML = `

                <div class="empty-feedback">

                    Unable to load feedback.

                </div>

            `;

        }

    }

}


/* =========================================================
   RENDER FEEDBACK
========================================================= */

function renderFeedback(
    feedback
) {

    const container =
        document.getElementById(
            "feedbackContainer"
        );


    if (!container) return;


    if (!feedback.length) {

        container.innerHTML = `

            <div class="empty-feedback">

                No feedback received yet.

            </div>

        `;

        return;

    }


    container.innerHTML =
        feedback.map(
            function (item) {

                /*
                 * IMPORTANT:
                 * Backend feedback.py returns:
                 *
                 * full_name
                 * email
                 * description
                 * submitted_at
                 *
                 * NOT:
                 * user_name
                 * message
                 * created_at
                 */

                const name =
                    item.full_name ||
                    "Unknown User";


                const email =
                    item.email ||
                    "";


                const description =
                    item.description ||
                    "";


                const submittedAt =
                    item.submitted_at ||
                    "";


                return `

                    <div
                        class="feedback-card"
                    >

                        <div
                            class="feedback-user"
                        >

                            <div
                                class="feedback-avatar"
                            >

                                ${escapeHtml(
                                    initials(name)
                                )}

                            </div>


                            <div>

                                <div
                                    class="feedback-name"
                                >
                                    ${escapeHtml(
                                        name
                                    )}
                                </div>


                                <div
                                    class="feedback-date"
                                >
                                    ${escapeHtml(
                                        email
                                    )}
                                </div>


                                <div
                                    class="feedback-date"
                                >
                                    ${escapeHtml(
                                        submittedAt
                                    )}
                                </div>

                            </div>

                        </div>


                        <div
                            class="feedback-message"
                        >
                            ${escapeHtml(
                                description
                            )}
                        </div>

                    </div>

                `;

            }
        ).join("");

}


/* =========================================================
   REPORTS
========================================================= */

async function loadReports() {

    /*
     * The current admin.py you provided does not yet
     * have /admin/reports.
     *
     * Therefore we generate reports from the data
     * already available.
     */

    try {

        if (!allDevices.length) {

            const deviceData =
                await apiRequest(
                    "/admin/devices"
                );


            allDevices =
                deviceData.devices || [];

        }


        if (!allBorrowings.length) {

            const borrowingData =
                await apiRequest(
                    "/admin/borrowings"
                );


            allBorrowings =
                borrowingData.borrowings || [];

        }


        const deviceReport =
            document.getElementById(
                "deviceUsageReport"
            );


        const borrowingReport =
            document.getElementById(
                "borrowingReport"
            );


        /* -----------------------------------------
           DEVICE REPORT
        ----------------------------------------- */

        if (deviceReport) {

            const deviceRows =
                allDevices.map(
                    function (device) {

                        const total =
                            Number(
                                device.total_quantity ||
                                0
                            );


                        const available =
                            Number(
                                device.available_quantity ||
                                0
                            );


                        const borrowed =
                            Math.max(
                                total -
                                available,
                                0
                            );


                        return {

                            name:
                                device.device_name,

                            borrowed:
                                borrowed

                        };

                    }
                );


            deviceReport.innerHTML =
                renderReportRows(
                    deviceRows
                );

        }


        /* -----------------------------------------
           BORROWING REPORT
        ----------------------------------------- */

        if (borrowingReport) {

            const totalBorrowings =
                allBorrowings.length;


            const totalQuantity =
                allBorrowings.reduce(
                    function (total, item) {

                        return total +
                            Number(
                                item.quantity || 0
                            );

                    },
                    0
                );


            const currentlyBorrowed =
                allBorrowings.filter(
                    function (item) {

                        return String(
                            item.status || ""
                        ).toLowerCase() ===
                            "borrowed";

                    }
                ).length;


            borrowingReport.innerHTML =
                renderReportRows([

                    {
                        name:
                            "Total Borrowing Records",

                        value:
                            totalBorrowings

                    },

                    {
                        name:
                            "Total Devices Borrowed",

                        value:
                            totalQuantity

                    },

                    {
                        name:
                            "Currently Borrowed",

                        value:
                            currentlyBorrowed

                    }

                ]);

        }

    }

    catch (error) {

        console.error(
            "Reports error:",
            error
        );

    }

}


/* =========================================================
   RENDER REPORT ROWS
========================================================= */

function renderReportRows(
    rows
) {

    if (
        !rows ||
        !Array.isArray(rows) ||
        !rows.length
    ) {

        return `

            <p
                style="
                    color:#94a3b8;
                    font-size:12px;
                "
            >
                No report data yet.
            </p>

        `;

    }


    return rows.map(
        function (row) {

            const values =
                Object.values(row);


            return `

                <div
                    class="report-row"
                >

                    <span>
                        ${escapeHtml(
                            values[0] ?? ""
                        )}
                    </span>


                    <strong>
                        ${escapeHtml(
                            values[1] ?? ""
                        )}
                    </strong>

                </div>

            `;

        }
    ).join("");

}


/* =========================================================
   VIEW DEVICE
========================================================= */

function viewDevice(
    deviceId
) {

    const device =
        allDevices.find(
            function (item) {

                return Number(
                    item.device_id ??
                    item.id
                ) ===
                    Number(deviceId);

            }
        );


    if (!device) {

        alert(
            "Device information not found."
        );

        return;

    }


    alert(

        "Device: " +
        (device.device_name || "") +

        "\n\n" +

        "Device Code: " +
        (device.device_code || "-") +

        "\n" +

        "Category: " +
        (device.category || "-") +

        "\n" +

        "Total Quantity: " +
        (device.total_quantity ?? 0) +

        "\n" +

        "Available Quantity: " +
        (device.available_quantity ?? 0)

    );

}


/* =========================================================
   VIEW BORROWING
========================================================= */

function viewBorrowing(
    borrowingId
) {

    const item =
        allBorrowings.find(
            function (borrowing) {

                return Number(
                    borrowing.borrowing_id ??
                    borrowing.borrow_id ??
                    borrowing.id
                ) ===
                    Number(borrowingId);

            }
        );


    if (!item) {

        alert(
            "Borrowing information not found."
        );

        return;

    }


    alert(

        "Borrowing ID: " +
        (
            item.borrowing_id ??
            item.borrow_id ??
            item.id ??
            ""
        ) +

        "\n\n" +

        "User: " +
        (
            item.full_name ??
            item.user ??
            item.user_name ??
            ""
        ) +

        "\n" +

        "Email: " +
        (
            item.email ??
            ""
        ) +

        "\n" +

        "Device: " +
        (
            item.device_name ??
            item.device ??
            ""
        ) +

        "\n" +

        "Quantity: " +
        (
            item.quantity ??
            ""
        ) +

        "\n" +

        "Borrow Date: " +
        (
            item.borrow_date ??
            ""
        ) +

        "\n" +

        "Borrow Time: " +
        (
            item.borrow_time ??
            ""
        ) +

        "\n" +

        "Status: " +
        (
            item.status ??
            ""
        )

    );

}


/* =========================================================
   BADGES
========================================================= */

function updateBadge(
    id,
    count
) {

    const badge =
        document.getElementById(
            id
        );


    if (!badge) return;


    badge.textContent =
        count;


    if (
        Number(count) > 0
    ) {

        badge.style.display =
            "inline-flex";

    }

    else {

        badge.style.display =
            "none";

    }

}


/* =========================================================
   EMPTY TABLE ROW
========================================================= */

function emptyRow(
    columns,
    text
) {

    return `

        <tr>

            <td
                colspan="${columns}"
                class="empty-state"
            >

                ${escapeHtml(
                    text
                )}

            </td>

        </tr>

    `;

}


/* =========================================================
   INITIALS
========================================================= */

function initials(
    name
) {

    return String(name)
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(
            function (part) {

                return part
                    .charAt(0)
                    .toUpperCase();

            }
        )
        .join("");

}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHtml(
    value
) {

    return String(
        value ?? ""
    )

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );

}


/* =========================================================
   LOGOUT
========================================================= */

function adminLogout() {

    const confirmed =
        confirm(
            "Are you sure you want to logout?"
        );


    if (!confirmed) {

        return;

    }


    localStorage.removeItem(
        "loggedInUser"
    );


    localStorage.removeItem(
        "user"
    );


    localStorage.removeItem(
        "admin"
    );


    localStorage.removeItem(
        "user_id"
    );


    localStorage.removeItem(
        "user_full_name"
    );


    localStorage.removeItem(
        "user_email"
    );


    window.location.href =
        "home.html";

}


/* =========================================================
   CLOSE ADD DEVICE MODAL WHEN CLICKING OUTSIDE
========================================================= */

window.addEventListener(
    "click",
    function (event) {

        const modal =
            document.getElementById(
                "addDeviceModal"
            );


        if (
            modal &&
            event.target === modal
        ) {

            closeAddDevice();

        }

    }
);