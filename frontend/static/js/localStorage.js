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

    const userPic = localStorage.getItem("user_pic");
        const userImageElement = document.getElementById("userImage");

        // ກວດສອບວ່າ userImage element ມີຢູ່
        if (userImageElement) {
            if (userPic) {
                userImageElement.src = `${DATABASE_URL}${userPic}`; // ໃຊ້ຮູບພາບຈາກ localStorage
            } else {
                userImageElement.src = DEFAULT_IMAGE; // ໃຊ້ຮູບພາບຄ່າເລີ່ມຕົ້ນຈາກ Django static
            }
        } else {
            console.warn("Element with ID 'userImage' not found in the DOM.");
        }

        // ພິມລອກຂໍ້ມູນທີ່ຖືກຕ້ອງ

});
function setupModalCloseBehavior(myModal, modalElement) {
    // กำหนดให้ปุ่ม close ปิด modal
    const closeBtn = modalElement.querySelector('.btn-close');
    closeBtn.addEventListener('click', function () {
      myModal.hide();
    });
  
    // คลิกนอก modal เพื่อปิด
    modalElement.addEventListener('click', function (event) {
      if (!event.target.closest('.modal-dialog')) {
        myModal.hide();
      }
    });
  }
  
  async function viewProfile() {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
      alert("ບໍ່ພົບ ID ຂອງຜູ້ໃຊ້!");
      return;
    }
  
    try {
      const [userResponse, depResponse] = await Promise.all([
        fetch(`${DATABASE_URL}/api/users/${userId}/`),
        fetch(`${DATABASE_URL}/api/list/departments/`)
      ]);
  
      if (!userResponse.ok || !depResponse.ok) {
        throw new Error("ການດຶງຂໍ້ມູນບໍ່ສຳເລັດ");
      }
  
      const userData = await userResponse.json();
      const departments = await depResponse.json();
  
      const employee = userData.Employee;
      const departmentId = userData.Department;
      const status = userData.status;
      const pic = userData.pic;
  
      const statusMap = {
        1: "Admin",
        2: "User MM",
        3: "User IT",
        4: "User OP",
        5: "User DQ"
      };
      const statusName = statusMap[status] || "Unknown";
  
      const department = departments.find(d => d.id === departmentId);
      const departmentName = department ? department.name : "N/A";
  
      const profileHTML = `
        <div class="text-center">
            
            <img src="${DATABASE_URL}${pic}" onerror="this.onerror=null;this.src='/static/images/avatar.png';" ... 
            alt="Profile Picture" class="img-thumbnail" style="width: 150px; height: 150px; border-radius: 50%;">

        </div>
        <p><strong>ຊື່ຜູ້ໃຊ້:</strong> ${userData.username}</p>
        <p><strong>ພະແນກ:</strong> ${departmentName}</p>   
        <p><strong>ສະຖານະ:</strong> ${statusName}</p>                     
      `;
  
      document.getElementById('profile_body').innerHTML = profileHTML; 
  
      const modalElement = document.getElementById('exampleModalToggle');
      const myModal = new bootstrap.Modal(modalElement);
  
      setupModalCloseBehavior(myModal, modalElement);
  
      myModal.show();
  
    } catch (error) {
      console.error("ຜິດພາດ:", error);
      alert("ມີຂໍ້ຜິດພາດໃນການດຶງຂໍ້ມູນ!");
    }
  }
  
  document.getElementById('openModalBtn').addEventListener('click', viewProfile);

function Forget() {
    // Close the profile modal first
    $('#exampleModalToggle').modal('hide');
    
    // Create a modal for changing password if it doesn't exist
    if (!document.getElementById('changePasswordModal')) {
        const modalHTML = `
        <div class="modal fade" id="changePasswordModal" tabindex="-1" aria-hidden="true" style="font-family: 'Noto Sans Lao', sans-serif;">
            <div class="modal-dialog">
                <div class="modal-content" style="border-radius: 15px; border: 1px solid #007bff; box-shadow: 0 0 15px rgba(0,0,0,0.1);">    
                    <div class="modal-body pt-0">
                        <button type="button" class="btn-close position-absolute top-0 end-0 m-3" data-bs-dismiss="modal" aria-label="Close"></button>
                            <h5 class="float-none w-auto p-2 h5 text-primary fw-bold">ປ່ຽນລະຫັດຜ່ານ</h5>
                            <form id="changePasswordForm">
                                <div class="mb-4">
                                    <div class="input-group-custom">
                                      <input type="password" class="form-control" id="newPassword" required>
                                      <label for="newPassword" >ລະຫັດຜ່ານໃໝ່</label>
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <div class="input-group-custom">
                                      <input type="password" class="form-control" id="confirmPassword" required>
                                      <label for="confirmPassword">ຢືນຢັນລະຫັດຜ່ານໃໝ່</label>
                                    </div>
                                    <div class="d-grid mt-4">
                                        <button type="submit" class="btn btn-primary btn-lg fw-bold" style="border-radius: 10px; padding: 12px;">ຢືນຢັນ</button>
                                    </div>
                                </div>
                            </form>
                    </div>
                </div>
            </div>
        </div>`;
        
        // Append the modal to the body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add event listener for form submission
        document.getElementById('changePasswordForm').addEventListener('submit', function(e) {
            e.preventDefault();
            changePassword();
        });
    }
    
    // Show the change password modal
    const changePasswordModal = new bootstrap.Modal(document.getElementById('changePasswordModal'));
    changePasswordModal.show();
}
async function changePassword() {
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const userId = localStorage.getItem('user_id');

    console.log('user:', userId);
    console.log('newPassword:', newPassword);

    // Validate passwords
    if (newPassword !== confirmPassword) {
        await Swal.fire({
            icon: 'error',
            title: 'ຜິດພາດ',
            text: 'ລະຫັດຜ່ານໃໝ່ບໍ່ກົງກັນ. ກະລຸນາລອງໃໝ່ອີກຄັ້ງ.',
            confirmButtonText: 'ຕົກລົງ'
        });
        return;
    }
    if (newPassword.length < 4) {
        await Swal.fire({
            icon: 'error',
            title: 'ຜິດພາດ',
            text: 'ລະຫັດຜ່ານຄວນມີຢ່າງນ້ອຍ 4 ຕົວອັກສອນ.',
            confirmButtonText: 'ຕົກລົງ'
        });
        return;
    }
    try {
        const response = await fetch(`${DATABASE_URL}/api/users/${userId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                password: newPassword
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        const data = await response.json();
console.log('response from server:', data);

if (data.message?.includes('ສຳເລັດ')) {
    await Swal.fire({
        icon: 'success',
        title: 'ສຳເລັດ',
        text: 'ປ່ຽນລະຫັດຜ່ານສຳເລັດແລ້ວ!',
        timer: 2000
    });
    document.getElementById('changePasswordForm').reset();
    const changePasswordModal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
    changePasswordModal.hide();
} else {
    await Swal.fire({
        icon: 'error', // เปลี่ยน icon ให้เหมาะ
        title: 'ຜິດພາດ',
        text: data.message || 'ເກີດຂໍ້ຜິດພາດໃນການປ່ຽນລະຫັດຜ່ານ.',
       timer: 2000
    });
}
    } catch (error) {
        console.error('Error details:', error.message);
        await Swal.fire({
            icon: 'error',
            title: 'ຜິດພາດ',
            text: 'ເກີດຂໍ້ຜິດພາດ: ' + error.message,
            timer: 2000
        });
    }
}

