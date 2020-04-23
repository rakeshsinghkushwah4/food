$(document).ready(function () {
    $('#search').on('submit', function (event) {
        event.preventDefault();
        // console.log("form submitted!")  // sanity check
        // console.log('i side ajax')
        // create_post();
        search();
        // console.log('rakesh')
        // $('#hide_data').hide(100,function(){
        //             console.log('inside of hide')
        // });
        // $('#show_data').show(100,function(){
        //     console.log('inside of show')
        // })
       
        console.log('singh')

    });
});
// blog-menu
// $('ul#blog-menu').slicknav({
//   prependTo: ".blog_menu"
// });

// show data on html
// $(document).ready(function(){
//     $('#customer').hide(function(){
//         $.ajax(
//             {

//             }
//         )
//     });
// });


//};

// Ajax for Search

function search(){
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    var product_data,status_data;
    // always we define id first then action or other attributes
    var url = document.getElementById('search').getAttribute('action');
    product_data = $('#id_products').val();
    status_data = $('#id_status').val();
    console.log(product_data,status_data)
    $.ajax({
        type:"POST",
        url: url,
        headers:{"X-CSRFToken":$crf_token},
        data : {'products':product_data,'status':status_data},
        success : function(data){
            $('#product_d').remove();
            var data = JSON.parse(data) ;
            var table='';
            // $.each(data,function(index,value){
            // console.log(data[index].product__name)
            // console.log(data[index].product__Category)

            // });

            table = '<table class="table table-sm" id="product_d"><tr><th>Product</th><th>Category</th><th>Date Ordered</th><th>Status</th><th>Update</th></tr>'
            $.each(data,function(index, value) {
                table += '<tr>';
                table += '<td>'+value.product__name+'</td>';
                table += '<td>'+value.product__Category+'</td>';
                table += '<td>'+value.cr_date+'</td>';
                table += '<td>'+value.status+'</td>';
                table += '<td><a class="btn btn-sm btn-info" href="/accounts/update_order/'+value.id+'">Update</a></td>';
                table += '</tr>';

            });
            table += '</table>';
            $('#search_p').append(table)

            // var table = '';
            // var data = JSON.parse(data) ;
            // console.log(data) 
            // $.each(data,function(index, value) {
            //     // console.log('modle',value.model);
            //     // console.log('pk',value.pk);
            //     // console.log('fields name',value.fields.product);
            //     // console.log('fields text',value.fields.status);
            //     console.log(value.pk)
            //     table += '<tr>';
            //     table += '<td>{{'+value.pk+'.product}}</td>';
            //     // simple += '<td>'+value.fields.status+'</td>';
            //     // simple += '<td>'+value.fields.cr_date+'</td>';
            //     // simple += '<td>'+value.fields.product+'</td>';
            //     table += '</tr>';
            // });
            // $('#search-product').append(table);          

            // console.log('SUCCESS');
            // console.log(data);
            // // var data = JSON.parse(data);
            // console.log(data)                
            // $.each(data,function(index, value) {
            //     simple += '<h2>'+value.fields.name+'</h2>'
            //     simple += '<h5>'+value.fields.text+'</h5>'
            //     // console.log('modle',value.model);
            //     // console.log('pk',value.pk);
            //     // console.log('fields name',value.fields.name);
            //     // console.log('fields text',value.fields.text);
            // });
            // $('#customer').append(simple);
        },
        
    });
};

// // AJAX for posting
function create_post() {
    var title, text;
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    var strs =
        title = $('#i1').val()
    text = $('#i2').val()
    $.ajax(
        {
            type: "POST",
            url: $(this).data('url'),
            headers: { "X-CSRFToken": $crf_token },
            data: {
                name: title, text: text
            },
            // // handle a successful response
            // success: function (data) {
            //     $('#i1').val(''); // remove the value from the input
            //     $('#i2').val('');
            //     //console.log(data); // log the returned json to the console
            //     console.log("success"); // another sanity check  
                
            // },
            success : function(data){
                var simple = ' ';
                var data = JSON.parse(data);
                console.log(data)                
                $.each(data,function(index, value) {
                    simple += '<h2>'+value.fields.name+'</h2>'
                    simple += '<h5>'+value.fields.text+'</h5>'
                    // console.log('modle',value.model);
                    // console.log('pk',value.pk);
                    // console.log('fields name',value.fields.name);
                    // console.log('fields text',value.fields.text);
                });
                $('#customer').append(simple);

                
            } ,
            error: function (data) {
                console.log('error');

            },

        })
        
};
// function json_html(data){
//     var html_data = document.getElementById('customer')
//     for(var i=0;i<data.length; i++){
//         console.log('rkaehs')
//     }
// }
