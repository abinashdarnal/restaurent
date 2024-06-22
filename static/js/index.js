// JavaScript code for pagination
let currentPage = 1;
const itemsPerPage = 8; // Change this value as needed

function displayPage(page) {
   const rows = document.querySelectorAll(".data-list tr");
   const start = (page - 1) * itemsPerPage;
   const end = start + itemsPerPage;

   rows.forEach((row, index) => {
      if (index >= start && index < end) {
         row.style.display = "";
      } else {
         row.style.display = "none";
      }
   });
}

function prevPage() {
   if (currentPage > 1) {
      currentPage--;
      displayPage(currentPage);
      updatePagination();
   }
}

function nextPage() {
   const totalRows = document.querySelectorAll(".data-list tr").length;
   const totalPages = Math.ceil(totalRows / itemsPerPage);

   if (currentPage < totalPages) {
      currentPage++;
      displayPage(currentPage);
      updatePagination();
   }
}

function updatePagination() {
   const pagination = document.getElementById("pagination");
   pagination.innerHTML = ""; // Clear existing buttons

   const totalRows = document.querySelectorAll(".data-list tr").length;
   const totalPages = Math.ceil(totalRows / itemsPerPage);

   let startPage = 1;
   let endPage = totalPages;

   if (totalPages > 5) {
      if (currentPage <= 3) {
         endPage = 5;
      } else if (currentPage >= totalPages - 2) {
         startPage = totalPages - 4;
      } else {
         startPage = currentPage - 2;
         endPage = currentPage + 2;
      }
   }

   for (let i = startPage; i <= endPage; i++) {
      const button = document.createElement("button");
      button.textContent = i;
      button.classList.add("pagination-button");
      button.onclick = () => {
         currentPage = i;
         displayPage(currentPage);
         updatePagination();
      };
      pagination.appendChild(button);
   }
}

// Initial display
displayPage(currentPage);
updatePagination();

const displayImage = document.getElementById("displayImage");
const fileInput = document.getElementById("fileInput");
const addImageText = document.getElementById("addImageText");

// Make the img tag clickable to open the file input
displayImage.onclick = () => {
   fileInput.click();
};
addImageText.onclick = () => {
   fileInput.click();
};

// Update the img tag with the selected image
fileInput.onchange = (event) => {
   const file = event.target.files[0];
   if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
         displayImage.src = e.target.result;
         addImageText.classList.add("hidden");
      };
      reader.readAsDataURL(file);
   }
};

// Show "Add Image" text if no image is selected
displayImage.onload = () => {
   if (!displayImage.src) {
      addImageText.classList.remove("hidden");
   }
};

document.getElementById("add").addEventListener("click", function () {
   document.getElementById("add_container").classList.remove("hidden");
});
function closeAdd() {
   document.getElementById("add_container").classList.add("hidden");
}



function togglePasswordVisibility() {
   const passwordInput = document.getElementById("passwordInput");
   const toggleIcon = document.getElementById("togglePassword");

   if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
   } else {
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
   }
}

function toggleConfirmPasswordVisibility() {
   const passwordInput = document.getElementById("confirmPasswordInput");
   const toggleIcon = document.getElementById("toggleConfirmPassword");

   if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
   } else {
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
   }
}

// const checkinInput = document.getElementById('check_in');
// const checkoutInput = document.getElementById('check_out');
// const totalDaysSpan = document.getElementById('total_days');

// // Function to calculate the day difference
// function calculateDayDifference() {
//    const checkinDate = new Date(checkinInput.value);
//    const checkoutDate = new Date(checkoutInput.value);
//    const timeDiff = checkoutDate.getTime() - checkinDate.getTime();
//    const dayDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

//    // Update the total days span
//    totalDaysSpan.textContent = dayDiff;
// }

// // Add event listeners to the input fields
// checkinInput.addEventListener('change', calculateDayDifference);
// checkoutInput.addEventListener('change', calculateDayDifference);


// function enableField() {
//    document.getElementById('total_cost').disabled = false;
// }





