document.addEventListener("DOMContentLoaded", function() {
    const user = JSON.parse(localStorage.getItem("user"));
    const departmentName = localStorage.getItem("department_name");

    if (!user) {
        alert("You are not logged in!");
        window.location.href = "/login/";
        return;
    }

    const usernameElement = document.getElementById("header-username");
    const departmentElement = document.getElementById("departments");

    if (usernameElement) usernameElement.textContent = user.username || "N/A";
    if (departmentElement) departmentElement.textContent = departmentName || "N/A";
});
// ຕົວແປເກັບ mapping ຂອງ departments
let departmentMap = {};

// ຕົວແປເກັບ Bootstrap Modal instance
let myModalInstance = null;

// ດຶງຂໍ້ມູນພະແນກຈາກ API
async function fetchDepartments() {
    try {
        const response = await fetch(`${DATABASE_URL}/api/list/departments/`, { method: 'GET' });
        if (!response.ok) {
            throw new Error('Error fetching departments');
        }
        const departments = await response.json();
        // ສ້າງ mapping object { id: { name } }
        departmentMap = departments.reduce((map, dept) => {
            map[dept.id] = { name: dept.name };
            return map;
        }, {});
        // console.log('Department Map:', departmentMap); // Debug: ເບິ່ງ mapping
    } catch (error) {
        console.error('Error fetching departments:', error);
        Swal.fire('ເກີດຂໍ້ຜິດພາດ!', 'ບໍ່ສາມາດດຶງຂໍ້ມູນພະແນກໄດ້', 'error');
    }
}

// ເອີ້ນ fetchDepartments ເມື່ອໜ້າ load
document.addEventListener('DOMContentLoaded', () => {
    fetchDepartments();
});
const DEFAULT_IMAGE = "{% static 'images/avatar.png' %}";
function logout() {
    localStorage.removeItem("user");
    localStorage.removeItem("department");
    localStorage.removeItem("department_name");
    window.location.href = "/login/";
}
    function viewProfile() {
            const empId = localStorage.getItem('employee'); // Get empId from localStorage
            if (!empId) {
                Swal.fire('ເກີດຂໍ້ຜິດພາດ!', 'ບໍ່ພົບ ID ພະນັກງານໃນ localStorage', 'error');
                return;
            }
            console.log('Employee ID:', empId); // Debug: Log empId
            const apiUrl = `${DATABASE_URL}/api/employee/${empId}/`; // Construct API URL
            console.log('Fetching from:', apiUrl); // Debug: Log the API URL

            fetch(apiUrl, { method: 'GET' })
                .then(response => {
                    console.log('Response Status:', response.status); // Debug: Log status code
                    if (!response.ok) {
                        return response.json().then(err => { 
                            throw new Error(err.error || 'Error fetching employee data'); 
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Response Data:', data); // Debug: Log response data

                    // Handle both array and object responses
                    const employee = Array.isArray(data) && data.length > 0 ? data[0].employee : data.employee || data;

                    if (!employee) {
                        throw new Error('ບໍ່ພົບຂໍ້ມູນພະນັກງານ');
                    }

                    // Create image URL
                    const imageUrl = employee.pic ? `${DATABASE_URL}${employee.pic}` : DEFAULT_IMAGE;

                    // Map Department ID to name
                    const dept = departmentMap[employee.Department] || { name: '-' };
                    const departmentName = dept.name;

                    // Calculate work duration
                    function calculateWorkDuration(yearEntry) {
                        if (!yearEntry || yearEntry === '-') {
                            return '-';
                        }

                        const startDate = new Date(yearEntry);
                        const currentDate = new Date();

                        if (isNaN(startDate.getTime())) {
                            return '-';
                        }

                        let years = currentDate.getFullYear() - startDate.getFullYear();
                        if (
                            currentDate.getMonth() < startDate.getMonth() ||
                            (currentDate.getMonth() === startDate.getMonth() && currentDate.getDate() < startDate.getDate())
                        ) {
                            years--;
                        }

                        return years >= 0 ? `${years} ປີ` : 'ໜ້ອຍກວ່າ 1 ປີ';
                    }
                    const dateObj = new Date(employee.birth_date);
                    const formattedDate = dateObj.toLocaleDateString('en-TH', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    });

                    const dateIn = new Date(employee.year_entry);
                    const formatdateIn = dateIn.toLocaleDateString('en-TH', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit'
                    });
                    // Create HTML for employee detail
                    const employeeDetail = `
                        <div class="row">
                            <div class="col-md-4 text-center">
                                <img src="${imageUrl}" alt="Employee Image" class="img-fluid rounded" 
                                    style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #007bff;">
                            </div>
                            <div class="col-md-4">                              
                                <p><strong>ຊື່ພາສາລາວ:</strong> ${employee.lao_name || '-'}</p>
                                <p><strong>ຊື່ພາສາອັງກິດ:</strong> ${employee.eng_name || '-'}</p>
                                <p><strong>ຊື່ຫຼີ້ນ:</strong> ${employee.nickname || '-'}</p>
                                <p><strong>ເພດ:</strong> ${employee.Gender || '-'}</p>
                                <p><strong>ພະແນກ:</strong> ${departmentName}</p>
                            </div>
                            <div class="col-md-4">
                                <p><strong>ວັນເດືອນປີເກີດ:</strong> ${formattedDate || '-'}</p>
                                <p><strong>ສະຖານະ:</strong> ${employee.status || '-'}</p>
                                <p><strong>ຕຳແໜ່ງ:</strong> ${employee.position || '-'}</p>
                                <p><strong>ວັນທີ່ເຂົ້າວຽກ:</strong> ${formatdateIn || '-'}</p>
                                <p><strong>ອາຍຸການ:</strong> ${calculateWorkDuration(employee.year_entry)}</p>
                                <p><strong>ລະດັບເງິນເດືອນ:</strong> ${employee.salary_level || '-'}</p>
                                <p><strong>ເບີໂທ:</strong> ${employee.phone || '-'}</p>
                            </div>
                        </div>
                    `;

                    // Insert HTML into modal body
                    const modalBody = document.getElementById('employee_detail');
                    if (!modalBody) {
                        throw new Error('ບໍ່ພົບ element employee_detail');
                    }
                    modalBody.innerHTML = employeeDetail;

                    // Show modal
                    const modalElement = document.getElementById('myModal');
                    if (!modalElement) {
                        throw new Error('ບໍ່ພົບ modal element');
                    }
                    const myModalInstance = new bootstrap.Modal(modalElement);
                    myModalInstance.show();
                })
                .catch(error => {
                    console.error('Error fetching employee:', error);
                    Swal.fire('ເກີດຂໍ້ຜິດພາດ!', error.message, 'error');
                });
        }