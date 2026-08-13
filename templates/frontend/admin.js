const API_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
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

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                data.message || "Request failed"
            );
        }

        return data;

    } catch (error) {

        console.error(
            "API Error:",
            error
        );

        throw error;
    }
}


/* =========================================================
   LOAD ALL ADMIN DATA
========================================================= */

async function loadAdminData() {

    await Promise.allSettled([

        loadStats(),

        loadUsers(),

        loadDevices(),

        loadBorrowings(),

        loadFeedback(),

        loadNotifications()

    ]);
}


/* =========================================================
   MODULE NAVIGATION
========================================================= */

function openModule(moduleId, clickedMenu) {

    document
        .querySelectorAll(".module")
        .forEach(module => {

            module.classList.remove("active");

        });


    const selectedModule =
        document.getElementById(moduleId);


    if (selectedModule) {

        selectedModule.classList.add("active");

    }


    document
        .querySelectorAll(".menu-item")
        .forEach(item => {

            item.classList.remove("active");

        });


    if (clickedMenu) {

        clickedMenu.classList.add("active");

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


    document.getElementById(
        "pageTitle"
    ).textContent =
        titles[moduleId] || "";


    document.getElementById(
        "pageSubtitle"
    ).textContent =
        subtitles[moduleId] || "";
}


/* =========================================================
   DASHBOARD STATISTICS
========================================================= */

async function loadStats() {

    try {

        const data =
            await apiRequest(
                "/admin/stats"
            );


        document.getElementById(
            "totalUsers"
        ).textContent =
            data.total_users ?? 0;


        document.getElementById(
            "totalDevices"
        ).textContent =
            data.total_devices ?? 0;


        document.getElementById(
            "borrowedDevices"
        ).textContent =
            data.borrowed_devices ?? 0;


        document.getElementById(
            "totalFeedback"
        ).textContent =
            data.total_feedback ?? 0;


    } catch (error) {

        console.error(
            "Loading statistics failed:",
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


        renderUsers(allUsers);


    } catch (error) {

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
        users.map(user => {

            return `

                <tr>

                    <td>
                        ${escapeHtml(
                            user.id ?? ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            user.full_name ?? ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            user.phone ?? ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            user.email ?? ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            user.registered_at ?? ""
                        )}
                    </td>

                    <td>

                        <span
                            class="status active-status"
                        >
                            ${escapeHtml(
                                user.status || "Active"
                            )}
                        </span>

                    </td>

                    <td>

                        <button
                            class="view-btn"
                            onclick="viewUser(
                                ${Number(user.id) || 0}
                            )"
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
        allUsers.filter(user => {

            const text = `

                ${user.full_name || ""}

                ${user.email || ""}

                ${user.phone || ""}

            `.toLowerCase();


            return text.includes(search);

        });


    renderUsers(filtered);
}


/* =========================================================
   VIEW USER
========================================================= */

function viewUser(userId) {

    const user =
        allUsers.find(
            item =>
                Number(item.id) ===
                Number(userId)
        );


    if (!user) return;


    document.getElementById(
        "detailName"
    ).textContent =
        user.full_name || "-";


    document.getElementById(
        "detailPhone"
    ).textContent =
        user.phone || "-";


    document.getElementById(
        "detailEmail"
    ).textContent =
        user.email || "-";


    document.getElementById(
        "detailDate"
    ).textContent =
        user.registered_at || "-";


    document.getElementById(
        "userDetails"
    ).style.display = "block";


    document.getElementById(
        "userDetails"
    ).scrollIntoView({
        behavior: "smooth"
    });
}


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


    } catch (error) {

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
        devices.map(device => {

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

            } else if (
                available <=
                Math.max(
                    1,
                    Math.floor(total * 0.2)
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
                            device.device_id ??
                            device.id ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            device.device_name ??
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
                            ${status}
                        </span>

                    </td>

                    <td>

                        <button
                            class="view-btn"
                            onclick="viewDevice(
                                ${Number(
                                    device.device_id ??
                                    device.id
                                ) || 0}
                            )"
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


    document.getElementById(
        "addDeviceModal"
    ).style.display =
        "flex";
}


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


async function submitAddDevice(event) {

    event.preventDefault();


    const message =
        document.getElementById(
            "deviceFormMessage"
        );


    const payload = {

        device_name:
            document.getElementById(
                "deviceName"
            ).value.trim(),

        total_quantity:
            Number(
                document.getElementById(
                    "deviceTotal"
                ).value
            ),

        category:
            document.getElementById(
                "deviceCategory"
            ).value.trim(),

        description:
            document.getElementById(
                "deviceDescription"
            ).value.trim()

    };


    if (
        !payload.device_name ||
        payload.total_quantity < 1
    ) {

        message.textContent =
            "Please enter valid device information.";

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


        message.textContent =
            data.message ||
            "Device added successfully.";


        await loadDevices();

        await loadStats();


        setTimeout(
            closeAddDevice,
            700
        );


    } catch (error) {

        message.textContent =
            error.message;

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


        updateBadge(
            "borrowingBadge",
            allBorrowings.filter(
                item =>
                    String(
                        item.status || ""
                    ).toLowerCase() ===
                    "borrowed"
            ).length
        );


    } catch (error) {

        console.error(
            "Loading borrowings failed:",
            error
        );

    }
}


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
        borrowings.map(item => {

            const status =
                item.status ||
                "Borrowed";


            let statusClass =
                "borrowed-status";


            if (
                status.toLowerCase() ===
                "returned"
            ) {

                statusClass =
                    "returned-status";

            } else if (
                status.toLowerCase() ===
                "overdue"
            ) {

                statusClass =
                    "overdue-status";

            }


            return `

                <tr>

                    <td>
                        ${escapeHtml(
                            item.borrow_id ??
                            item.id ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            item.user ??
                            item.user_name ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            item.device ??
                            item.device_name ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            item.quantity ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            item.borrowed_date ??
                            ""
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            item.return_date ??
                            "-"
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
                            class="view-btn"
                            onclick="viewBorrowing(
                                ${Number(
                                    item.borrow_id ??
                                    item.id
                                ) || 0}
                            )"
                        >
                            View
                        </button>

                    </td>

                </tr>

            `;

        }).join("");
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


        const unread =
            allFeedback.filter(
                item =>
                    !item.is_read
            ).length;


        updateBadge(
            "feedbackBadge",
            unread
        );


        updateBadge(
            "totalFeedback",
            allFeedback.length
        );


    } catch (error) {

        console.error(
            "Loading feedback failed:",
            error
        );

    }
}


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
        feedback.map(item => {

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
                                initials(
                                    item.user_name ||
                                    "User"
                                )
                            )}
                        </div>

                        <div>

                            <div
                                class="feedback-name"
                            >
                                ${escapeHtml(
                                    item.user_name ||
                                    "Unknown User"
                                )}
                            </div>

                            <div
                                class="feedback-date"
                            >
                                ${escapeHtml(
                                    item.created_at ||
                                    ""
                                )}
                            </div>

                        </div>

                    </div>


                    <div
                        class="feedback-message"
                    >
                        ${escapeHtml(
                            item.message ||
                            ""
                        )}
                    </div>


                    <span
                        class="feedback-category"
                    >
                        ${escapeHtml(
                            item.category ||
                            "Other"
                        )}
                    </span>

                </div>

            `;

        }).join("");
}


/* =========================================================
   NOTIFICATIONS
========================================================= */

async function loadNotifications() {

    try {

        const data =
            await apiRequest(
                "/admin/notifications"
            );


        const notifications =
            data.notifications || [];


        const unread =
            notifications.filter(
                item =>
                    !item.is_read
            ).length;


        updateBadge(
            "notificationBadge",
            unread
        );


        const list =
            document.getElementById(
                "notificationList"
            );


        if (!list) return;


        if (!notifications.length) {

            list.innerHTML = `

                <div
                    style="
                        padding:20px;
                        text-align:center;
                        color:#94a3b8;
                    "
                >
                    No new notifications.
                </div>

            `;

            return;
        }


        list.innerHTML =
            notifications.map(item => {

                return `

                    <div
                        class="notification-item"
                        onclick="markNotificationRead(
                            ${Number(item.id) || 0}
                        )"
                    >

                        <strong>
                            ${escapeHtml(
                                item.title ||
                                "Notification"
                            )}
                        </strong>

                        <p>
                            ${escapeHtml(
                                item.message ||
                                ""
                            )}
                        </p>

                        <small>
                            ${escapeHtml(
                                item.created_at ||
                                ""
                            )}
                        </small>

                    </div>

                `;

            }).join("");


    } catch (error) {

        console.error(
            "Notifications:",
            error
        );

    }
}


function showNotifications() {

    const panel =
        document.getElementById(
            "notificationPanel"
        );


    if (!panel) return;


    if (
        panel.style.display ===
        "none"
    ) {

        panel.style.display =
            "block";


        loadNotifications();

    } else {

        panel.style.display =
            "none";

    }
}


function closeNotifications() {

    const panel =
        document.getElementById(
            "notificationPanel"
        );


    if (panel) {

        panel.style.display =
            "none";

    }
}


async function markNotificationRead(
    id
) {

    if (!id) return;


    try {

        await apiRequest(
            `/admin/notifications/${id}/read`,
            {
                method: "PATCH"
            }
        );


        await loadNotifications();


    } catch (error) {

        console.error(
            "Notification:",
            error
        );

    }
}


/* =========================================================
   REPORTS
========================================================= */

async function loadReports() {

    try {

        const data =
            await apiRequest(
                "/admin/reports"
            );


        const deviceReport =
            document.getElementById(
                "deviceUsageReport"
            );


        const borrowingReport =
            document.getElementById(
                "borrowingReport"
            );


        if (
            data.device_usage &&
            deviceReport
        ) {

            deviceReport.innerHTML =
                renderReportRows(
                    data.device_usage
                );

        }


        if (
            data.borrowing_summary &&
            borrowingReport
        ) {

            borrowingReport.innerHTML =
                renderReportRows(
                    data.borrowing_summary
                );

        }


    } catch (error) {

        console.error(
            "Reports:",
            error
        );

    }
}


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


    return rows.map(row => {

        const values =
            Object.values(row);


        return `

            <div class="report-row">

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

    }).join("");
}


/* =========================================================
   VIEW FUNCTIONS
========================================================= */

function viewDevice(deviceId) {

    const device =
        allDevices.find(
            item =>
                Number(
                    item.device_id ??
                    item.id
                ) ===
                Number(deviceId)
        );


    if (!device) return;


    alert(

        `Device: ${
            device.device_name || ""
        }\n\n` +

        `Total: ${
            device.total_quantity ?? 0
        }\n` +

        `Available: ${
            device.available_quantity ?? 0
        }`

    );
}


function viewBorrowing(
    borrowingId
) {

    const item =
        allBorrowings.find(
            borrowing =>
                Number(
                    borrowing.borrow_id ??
                    borrowing.id
                ) ===
                Number(borrowingId)
        );


    if (!item) return;


    alert(

        `Borrow ID: ${
            item.borrow_id ??
            item.id ??
            ""
        }\n\n` +

        `User: ${
            item.user ??
            item.user_name ??
            ""
        }\n` +

        `Device: ${
            item.device ??
            item.device_name ??
            ""
        }\n` +

        `Quantity: ${
            item.quantity ?? ""
        }\n` +

        `Status: ${
            item.status ?? ""
        }`

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
        document.getElementById(id);


    if (!badge) return;


    badge.textContent =
        count;


    if (Number(count) > 0) {

        badge.style.display =
            "inline-flex";

    } else {

        badge.style.display =
            "none";

    }
}


/* =========================================================
   HELPERS
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
                ${escapeHtml(text)}
            </td>

        </tr>

    `;
}


function initials(name) {

    return String(name)
        .trim()
        .split(/\s+/)
        .slice(0, 2)
        .map(
            part =>
                part
                    .charAt(0)
                    .toUpperCase()
        )
        .join("");
}


function escapeHtml(value) {

    return String(value ?? "")
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


    if (!confirmed) return;


    localStorage.removeItem(
        "loggedInUser"
    );

    localStorage.removeItem(
        "user"
    );

    localStorage.removeItem(
        "admin"
    );


    window.location.href =
        "home.html";
}


/* =========================================================
   CLOSE MODAL WHEN CLICKING OUTSIDE
========================================================= */

window.addEventListener(
    "click",
    function(event) {

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