$( document ).ready(function() {


    $("#empty_categories").on("click", function(e) {
        e.preventDefault();
        empty_categories_send_ajax()
    });


    function empty_categories_send_ajax(){
        $('#categories_list').empty()
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };

        $.ajax({
            type: 'GET',
            url: EMPTY_CATEGORY_URL,
            dataType: 'json',
            data:data,
            success: function(res) {
                show_categories(res)
            }
        });
    }

// -----------------------------------------------------------------------
    $("#popular_categories").on("click", function(e) {
        e.preventDefault();
        popular_send_ajax($(this).val())
    });

    function popular_send_ajax(){
        $('#categories_list').empty()
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };
        console.log('inside send_ajax ')
        $.ajax({
            type: 'GET',
            url: POPULAR_CATEGORIES_URL,
            dataType: 'json',
            data:data,
            success: function(res) {
                console.log('res : ',res);
                show_categories(res)
            }
        });
    }

// -----------------------------------------------------------------------

    function show_categories(data){
        $('#categories_list').empty()
        if ( data['categories'] ){
            for (const [key, value] of Object.entries(data['categories'])) {


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
                span1.append(value[1])
                h5.append(span1)               

                var a1 = document.createElement("a")
                a1.classList = "btn btn-danger"
                a1.href= "{% url 'category_delete' $(this).id %}"
                a1.innerHTML='Delete'
                a1.style="margin-right:5px"

                var a2 = document.createElement("a")
                a2.classList = "btn btn-warning";
                a2.method = 'post'
                a2.href = "{% url 'category_edit' $(this).id %}"
                a2.innerHTML = 'Edit'
                a2.style="margin-right:5px"

                var a3 = document.createElement("a")
                a3.classList = "btn btn-info";
                a3.method = 'post'
                a3.href = "{% url 'category_edit' $(this).id %}"
                a3.style="margin-right:5px"
                a3.innerHTML = 'Details'

                var a4 = document.createElement("a")
                a4.classList = "btn btn-success";
                a4.href = "{% url 'category_tasks' $(this).id %}"
                a4.innerHTML = 'Category Tasks'

                div3.append(h5)
                div3.append(a1)
                div3.append(a2)
                div3.append(a3)
                div3.append(a4)
                div2.append(div3)
                div1.append(div2)
                $('#categories_list').append(div1)
              }
            
        }else{
            $('#categories_list').empty()
        }
        
    }
    // ------------------------------------------------------------------------

  });
