$( document ).ready(function() {

    $("#all_orders").on("click", function(e) {
        e.preventDefault();
        all_orders_send_ajax()
    });
    function all_orders_send_ajax(){
        console.log('eeeeeeeeeee')
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };
        console.log(data)
        $.ajax({
            type: 'GET',
            url: '/branche/order/all',
            dataType: 'json',
            data:data,
            beforeSend:function(e){
                $('#order_list').html('loading....')
            },
            success: function(res) {
                console.log(res.data)
                $('#order_list').html(res.data)
            }
        });
    }

// -----------------------------------------------------------------------

    $("#sent_orders").on("click", function(e) {
            e.preventDefault();
            sent_orders_send_ajax()
        });
        function sent_orders_send_ajax(){
            console.log('eeeeeeeeeee')
            data={
                'csrfmiddlewaretoken':CSRF_TOKEN,
                };
            console.log(data)
            $.ajax({
                type: 'GET',
                url: '/branche/order/sent',
                dataType: 'json',
                data:data,
                beforeSend:function(e){
                    $('#order_list').html('loading....')
                },
                success: function(res) {
                    console.log(res.data)
                    $('#order_list').html(res.data)
                }
            });
        }

// -----------------------------------------------------------------------
    $("#delivered_orders").on("click", function(e) {
        e.preventDefault();
        delivered_orders_send_ajax()
    });
    function delivered_orders_send_ajax(){
        console.log('eeeeeeeeeee')
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };
        console.log(data)
        $.ajax({
            type: 'GET',
            url: '/branche/order/delivered',
            dataType: 'json',
            data:data,
            beforeSend:function(e){
                $('#order_list').html('loading....')
            },
            success: function(res) {
                console.log(res.data)
                $('#order_list').html(res.data)
            }
        });
    }

// -----------------------------------------------------------------------
    $("#ordered_orders").on("click", function(e) {
        e.preventDefault();
        ordered_orders_send_ajax()
    });
    function ordered_orders_send_ajax(){
        console.log('eeeeeeeeeee')
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };
        console.log(data)
        $.ajax({
            type: 'GET',
            url: '/branche/order/ordered',
            dataType: 'json',
            data:data,
            beforeSend:function(e){
                $('#order_list').html('loading....')
            },
            success: function(res) {
                console.log(res.data)
                $('#order_list').html(res.data)
            }
        });
    }
// ------------------------------------------------------------

    $("#orders_date_sort").on("click", function(e) {
        e.preventDefault();
        sort_orders_send_ajax()
    });
    function sort_orders_send_ajax(){
        console.log('eeeeeeeeeee')
        data={
            'csrfmiddlewaretoken':CSRF_TOKEN,
            };
        console.log(data)
        $.ajax({
            type: 'GET',
            url: '/branche/order/date_sort',
            dataType: 'json',
            data:data,
            beforeSend:function(e){
                $('#order_list').html('loading....')
            },
            success: function(res) {
                console.log(res.data)
                $('#order_list').html(res.data)
            }
        });
    }


  });
