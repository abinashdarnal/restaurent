//edit table
document.addEventListener("DOMContentLoaded", function () {
   const editTable = document.querySelectorAll(".edit-table");
   console.log(editTable);
   editTable.forEach((button) => {
      button.addEventListener("click", function () {
         const tableId = this.getAttribute("table-edit");
         fetch(`/restaurent/table/${tableId}`)
            .then((response) => response.json())
            .then((data) => {
               "";
               showPopup(data);
               console.log(data);
            })
            .catch((error) =>
               console.error("Error fetching table details:", error)
            );
      });
   });

   function showPopup(data) {
      const popup = document.createElement("div");
      popup.className =
         "fixed top-0 inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50";

      popup.innerHTML = `
       <div class="bg-white rounded-lg overflow-hidden w-[650px]">
           <div class="flex justify-center p-3 bg-gray-300">
               <h1>Edit Table ${data.name}</h1>
           </div>
           <form method="POST">
             {% csrf_token %}

               <div class="px-4 py-2 flex flex-col">
                 <input type="hidden" name="table_id" value="${data.id}">

                 <div class="grid grid-cols-2 gap-2">
                   <input
                     type="text"
                     name="update_name"
                     class="bg-gray-100 p-2 rounded-lg focus:outline-none"
                     placeholder="${data.name}"
                   />


                 </div>
               </div>
               <div class="flex justify-end gap-4 items-center bg-gray-300 p-2">
                 <div
                   class="border-2 border-primary px-4 py-2 text-sm font-bold rounded-lg close-out-popup cursor-pointer"
                 >
                   Cancel
                 </div>
                 <button
                   type="Submit"
                   class="bg-primary px-4 py-2 text-sm font-bold rounded-lg text-white cursor-pointer"
                 >
                   Submit
                 </button>
               </div>
           </form>
       </div>
   `;

      document.body.appendChild(popup);

      popup
         .querySelector(".close-out-popup")
         .addEventListener("click", () => {
            document.body.removeChild(popup);
         });
   }
});
//delete desingation
document.addEventListener("DOMContentLoaded", function () {
   const deleteContent = document.querySelectorAll(".delete-table");

   deleteContent.forEach((button) => {
      console.log("tableId");
      button.addEventListener("click", function () {
         const tableId = this.getAttribute("table-delete");
         fetch(`/restaurent/table/${tableId}`)
            .then((response) => response.json())
            .then((data) => {
               console.log(data);
               showPopup(data);
            })
            .catch((error) =>
               console.error("Error fetching reservation details:", error)
            );
      });
   });

   function showPopup(data) {
      const popup = document.createElement("div");
      popup.className =
         "fixed top-0 inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50";

      popup.innerHTML = `
       <div class="bg-white rounded-lg overflow-hidden w-[650px]">
           <div class="flex justify-center p-3 bg-gray-300">
               <h1>Do you really want to delete ${data.name} ?</h1>
           </div>
           <form  method="POST" >
             {% csrf_token %}
                <div class="py-3">
                   <ul>
                       <li class="flex justify-between border-b-[1px] border-black/60 px-4 py-1">
                           <h1>Designation Name</h1>
                           <h1>${data.name}</h1>
                       </li>

                   </ul>
               </div>
               <div class="px-4 py-2 flex flex-col">
                 <input type="hidden" name="table_id" value="${data.id}">
               </div>
               <div class="flex justify-end gap-4 items-center bg-gray-300 p-2">
                 <div
                   class="border-2 border-primary px-4 py-2 text-sm font-bold rounded-lg close-room-edit cursor-pointer"
                 >
                   No
                 </div>
                 <a
                 href="/delete_table/${data.id}"

                   class="bg-primary px-4 py-2 text-sm font-bold rounded-lg text-white cursor-pointer"
                 >
                   Yes
                 </a>
               </div>
           </form>
       </div>
   `;

      document.body.appendChild(popup);

      popup
         .querySelector(".close-room-edit")
         .addEventListener("click", () => {
            document.body.removeChild(popup);
         });
   }
});



function openPopupFloor(id) {
   console.log("Hello world");
}