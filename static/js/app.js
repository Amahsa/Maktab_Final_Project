input = document.getElementById('title');
ul_tag = document.querySelector("ul.list-group");

document.getElementById('add_task').addEventListener('click',add_task)
$("label").click( function(event) {
  alert("You clicked me! ouch!");
});
function add_task(event)
  {
   
    // console.log('aaaaaa')
    // event.preventDefault()
    // if (input.value != '')
    // {
    //   li_tag = document.createElement("li");
    //   li_tag.className = 'list-group-item d-flex justify-content-between'; 
    //   li_tag.textContent = input.value;
    //   i_tag = document.createElement("i");
    //   i_tag.addEventListener("click", delete_one_task)
    //   i_tag.className = 'fas fa-times text-danger mr-auto delete-item';
    //   li_tag.appendChild(i_tag);
    //   ul_tag.appendChild(li_tag);
    //   input.value = "";
    //   function delete_one_task()
    //   {
    //   if (confirm("آیا مطمئنید؟")) {
    //     this.parentNode.remove() }
    //  }
    // }
    // else
    // {
    //   alert("تسک را وارد کنید")
    // }
  }

function delete_all_tasks(event)
  {
  if (confirm("آیا مطمئنید که میخواهید همه ی تسک ها را پاک کنید؟"))
    {
      
      // approach 1

      li_tag = document.querySelectorAll("ul li")
      li_tag.forEach(remove_task)
      function remove_task(item)
      {
        item.remove();
      }

      // approach 2

      // while(ul_tag.hasChildNodes())
      // {
      //   ul_tag.removeChild(ul_tag.firstChild);
      // }
    } 
  }

