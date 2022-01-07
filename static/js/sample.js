$( document ).ready(function() {

// {{test}} error
// console.log(test) error
// console.log(URL) 
// console.log(CSRF_TOKEN) 


    $("#last_tasks").on("click", function(e) {
        e.preventDefault();
        send_ajax($(this).val())
    });

    $("#expired_tasks").on("click", function(e) {
        e.preventDefault();
        console.log('inside expired_tasks func')
        epired_tasks_send_ajax($(this).val())
    });


    $("#unexpired_tasks").on("click", function(e) {
        e.preventDefault();
        console.log('inside not expired_tasks func')
        unexpired_tasks_send_ajax($(this).val())
    });


    function send_ajax(input_data){
        $('#Tasks_listt').empty()
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            'textt':input_data
            };
        data['text'] = input_data

        $.ajax({
            type: 'GET',
            // url: "http://127.0.0.1:8000/main/db_temp/",
            // url: "/main/db_temp/",
            url: URL,
            dataType: 'json',
            data:data,
            success: function(res) {
                console.log(res);
                show_persons(res)
            }
        });
    }

    function epired_tasks_send_ajax(input_data){
        console.log('inside epired_tasks_send_ajax ')
        $('#Tasks_listt').empty()
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            'textt':input_data
            };

        $.ajax({
            type: 'GET',
            // url: "http://127.0.0.1:8000/main/db_temp/",
            // url: "todo/expired_tasks/",
            url: EXPIRE_TASKS_URL,
            dataType: 'json',
            data:data,
            success: function(res) {
                console.log(res);
                show_persons(res)
            }
        });
    }


    function unexpired_tasks_send_ajax(input_data){
        console.log('inside not expired_tasks_send_ajax ')
        $('#Tasks_listt').empty()
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            'textt':input_data
            };

        $.ajax({
            type: 'GET',
            url: NOT_EXPIRE_TASKS_URL,
            dataType: 'json',
            data:data,
            success: function(res) {
                console.log('success, go to show_persons function ');
                show_persons(res)
            }
        });
    }

    function show_persons(data){
        console.log('inside show_persons function')
        my_ul_tag = $('#Tasks_list')
        $('#Tasks_listt').empty()
        if ( data['tasks'] ){
            console.log('dataaaaa : ', data['tasks'])
            // for (item in data['last_Tasks']) {
            //     console.log('item :',  item)
            for (const [key, value] of Object.entries(data['tasks'])) {

                // console.log("from sample.js *", key, value);
                console.log(key);
                // console.log(value);
                // console.log(value[5]);

                var div1= document.createElement("div");
                div1.classList= "col-md-10"
                div1.style = "margin:0 auto;"
                
                var div2= document.createElement("div");
                div2.classList= "card container-fluid"
                div2.style = "margin-top: 1rem;"

                var div3= document.createElement("div");
                div3.classList= "card-body"


                var h5 = document.createElement("h5");
                h5.classList= "card-title"
                var span1 = document.createElement("span");   
                span1.append(value[3])//value[3]
                span1.append(value[1])
                h5.append(span1)
                
                var p1 = document.createElement("p")
                p1.classList = "card-text";
                var span2 = document.createElement("span");   
                span2.append(value[6])  
                console.log('wwwwww,' , value[6])
                // console.log(type(value[6]))
                p1.innerHTML = value[6]

                var a1 = document.createElement("a")
                a1.classList = "btn btn-danger"
                a1.href= "todo/delete/{{eachtodo.id}}"
                a1.innerHTML='Delete'
                a1.style="margin-lef:1rem; margin-right:1rem"
                // a1.append(document.createElement("span").append('Delete'))

                var a2 = document.createElement("a")
                a2.classList = "btn btn-warning";
                a2.href = "todo/edit/{{eachtodo.id}}"
                a2.innerHTML = 'Edit'
                a2.style="margin-lef:1rem; margin-right:1rem"
                // a2.append(document.createElement("span").append('Edit'))

                var a3 = document.createElement("a")
                a3.classList = "btn btn-info";
                a3.href = "{% url 'todo/todo_detail' eachtodo.pk %}"
                a3.innerHTML = 'Details'
                // a2.val('Details')

                // div3.append('[h5,p1,a1,a2,a3]')
                div3.append(h5)
                div3.append(p1)
                div3.append(a1)
                div3.append(a2)
                div3.append(a3)
                div2.append(div3)
                div1.append(div2)
                $('#Tasks_listt').append(div1)
                // ---------------------------------------
                var li = document.createElement("li");  
                var span1 = document.createElement("span");   
                span1.append(value)
                li.append(span1)
                my_ul_tag.append(li)
                // ---------------------------------------


                // 
                // my_ul_tag.append(key)
              }
            
        }else{
            $('#Tasks_listt').empty()
            console.log('empty list')
            my_ul_tag.append()
        }
        
    }
    // ------------------------------------------------------------------------

  });




//   <div class="row mb-1" id='Tasks_list'>

//     <div class="col-md-10" style="margin:0 auto;"> 1
//         <div class="card container-fluid" style="margin-top: 1rem;"> 2
//             <div class="card-body"> 3
//               <h5 class="card-title">{{eachtodo.priority}}  {{eachtodo.title}}</h5>
//               <p class="card-text">{{eachtodo.Scheduling}}</p>
              
//               <a href="/delete/{{eachtodo.id}}" class="btn btn-danger">Delete</a>
//               <a href="/edit/{{eachtodo.id}}" class="btn btn-warning">Edit</a>
//               <a href="{% url 'todo_detail' eachtodo.pk %}" class="btn btn-info">Details</a>
//             </div>
//           </div>
//     </div>
// </div>